import requests
import logging
from config import ROBOFLOW_API_KEY, ROBOFLOW_MODEL_ID, ROBOFLOW_MODEL_VERSION, ROBOFLOW_CROP_MODEL_ID, ROBOFLOW_CROP_MODEL_VERSION
from utils.disease_guide import get_disease_info, CROP_NAME_MAP, DISEASE_GUIDE
logger = logging.getLogger(__name__)

def validate_prediction(disease_name, confidence):
    if confidence < 0.3:
        return (False, confidence, 'Confidence too low (< 30%)')
    disease_key = disease_name.lower().replace(' ', '_').replace('-', '_')
    is_in_db = False
    for key in DISEASE_GUIDE.keys():
        if disease_key == key or disease_key in DISEASE_GUIDE[key].get('aliases', []):
            is_in_db = True
            break
    if is_in_db and confidence >= 0.6:
        return (True, confidence, 'Valid - in database with good confidence')
    elif is_in_db and confidence >= 0.4:
        return (True, confidence, 'Valid - in database but lower confidence')
    else:
        return (False, confidence, f'Not found in disease database')

def get_roboflow_raw_prediction(image_file):
    try:
        image_file.seek(0)
        response = requests.post(f'https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}', params={'api_key': ROBOFLOW_API_KEY}, files={'file': image_file.read()}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'Roboflow raw prediction error: {str(e)}', exc_info=True)
        return {'error': str(e)}

def get_all_predictions(image_file):
    try:
        image_file.seek(0)
        response = requests.post(f'https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}', params={'api_key': ROBOFLOW_API_KEY}, files={'file': image_file.read()}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'Error getting Roboflow predictions: {str(e)}', exc_info=True)
        return None


def identify_crop(image_file, min_confidence=0.5):
    if not ROBOFLOW_CROP_MODEL_ID:
        return {'success': False, 'error': 'Crop model not configured', 'requires_user_input': True}
    try:
        image_file.seek(0)
        response = requests.post(f'https://detect.roboflow.com/{ROBOFLOW_CROP_MODEL_ID}/{ROBOFLOW_CROP_MODEL_VERSION}', params={'api_key': ROBOFLOW_API_KEY}, files={'file': image_file.read()}, timeout=30)
        response.raise_for_status()
        result = response.json()
        predictions = result.get('predictions', [])
        if not predictions:
            return {'success': False, 'error': 'No crop predictions returned', 'raw': result}
        top = max(predictions, key=lambda p: p.get('confidence', 0))
        crop = str(top.get('class', '')).lower().strip()
        confidence = float(top.get('confidence', 0))
        success = confidence >= min_confidence
        return {'success': success, 'detected_crop': crop, 'confidence': confidence, 'raw': result}
    except Exception as e:
        logger.error(f'Roboflow crop identification error: {str(e)}', exc_info=True)
        return {'success': False, 'error': str(e), 'requires_user_input': True}

def detect_disease(image_file, min_confidence=0.5, expected_crop=None, return_all=False, require_crop_match=False):
    try:
        if not expected_crop and not require_crop_match:
            crop_result = identify_crop(image_file)
            if crop_result.get('requires_user_input'):
                logger.info('Crop model not available; proceeding without crop pre-filtering')
            elif not crop_result.get('success'):
                logger.warning(f'Crop identification failed: {crop_result.get("error")}')
            else:
                expected_crop = crop_result.get('detected_crop')
                logger.info(f'Auto-identified crop as {expected_crop}')
            image_file.seek(0)
        elif require_crop_match and not expected_crop:
            return {'success': False, 'error': 'Crop type is required when require_crop_match is True'}

        expected_key = expected_crop.lower().strip() if expected_crop else None
        image_file.seek(0)
        response = requests.post(f'https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}', params={'api_key': ROBOFLOW_API_KEY}, files={'file': image_file.read()}, timeout=30)
        response.raise_for_status()
        rf_result = response.json()
        logger.info(f'Roboflow API Response: {rf_result}')

        predictions = rf_result.get('predictions', [])
        structured = []
        for pred in predictions:
            name = pred.get('class', 'Unknown Disease')
            conf = pred.get('confidence', 0)
            info = get_disease_info(name)
            crop_matches = False
            if expected_key:
                crop_matches = expected_key in info.get('crop_name', '').lower() or expected_key in info.get('crop_scientific_name', '').lower()
            structured.append({'class': name, 'confidence': conf, 'disease_info': info, 'crop_matches': crop_matches})

        if return_all:
            return {'success': True, 'all_predictions': structured, 'raw': rf_result, 'expected_crop': expected_key}

        if expected_key:
            expected_matched = [p for p in structured if p.get('crop_matches')]
            if expected_matched:
                structured = expected_matched
            else:
                logger.warning(f'User specified crop {expected_key} but model did not detect any {expected_key} diseases. Looking for {expected_key} diseases in database.')
                crop_info = CROP_NAME_MAP.get(expected_key)
                if crop_info:
                    crop_name = crop_info['name']
                    scientific_name = crop_info['scientific']
                else:
                    crop_name = expected_key.capitalize()
                    scientific_name = ''
                
                crop_diseases = []
                for disease_key, disease_info in DISEASE_GUIDE.items():
                    disease_crop_name = disease_info.get('crop_name', '').lower()
                    if expected_key in disease_crop_name:
                        crop_diseases.append({
                            'disease_key': disease_key,
                            'disease_name': disease_key,
                            'description': disease_info.get('description', ''),
                            'prevention': disease_info.get('prevention', []),
                            'control': disease_info.get('control', []),
                            'disease_info': disease_info
                        })
                
                if crop_diseases:
                    selected_disease = crop_diseases[0]
                    logger.info(f'Found {len(crop_diseases)} diseases for {expected_key}. Returning: {selected_disease["disease_key"]}')
                    return {
                        'success': True,
                        'disease_name': selected_disease['disease_key'],
                        'confidence': 0,
                        'disease_info': selected_disease['disease_info'],
                        'disease_details': f'Showing {crop_name} disease information from database',
                        'all_predictions': structured,
                        'expected_crop': expected_key
                    }
                else:
                    disease_info = {
                        'crop_name': crop_name,
                        'crop_scientific_name': scientific_name,
                        'description': f'No disease detected for {crop_name}. The plant may be healthy or the image may not clearly show the affected area. Please provide a clearer image of the affected plant part.',
                        'prevention': ['Monitor plants regularly', 'Maintain good farming practices', 'Ensure proper irrigation'],
                        'control': ['Continue current crop management practices']
                    }
                    return {
                        'success': True,
                        'disease_name': 'No Disease Detected',
                        'confidence': 0,
                        'disease_info': disease_info,
                        'disease_details': f'No {crop_name} diseases detected in image',
                        'all_predictions': structured,
                        'expected_crop': expected_key
                    }


        chosen = None
        warning = None
        candidates = [p for p in structured if not expected_key or p.get('crop_matches')]
        for pred in sorted(candidates, key=lambda x: (not x.get('crop_matches'), -x['confidence'])):
            name = pred['class']
            conf = pred['confidence']
            if conf < min_confidence:
                continue
            is_valid, conf2, reason = validate_prediction(name, conf)
            logger.info(f"Evaluating prediction '{name}' ({conf:.2%}): {reason}")
            if is_valid:
                chosen = pred
                break
        if not chosen and candidates:
            chosen = candidates[0]
            warning = 'Model predictions did not meet validation criteria; using top result.'
        if chosen:
            disease_info = chosen['disease_info']
            return_val = {'success': True, 'disease_name': chosen['class'], 'confidence': chosen['confidence'], 'disease_info': disease_info, 'disease_details': str(chosen)}
            return_val['all_predictions'] = structured
            return return_val
        else:
            logger.warning('No predictions returned from Roboflow model')
            if expected_key:
                crop_info = CROP_NAME_MAP.get(expected_key)
                if crop_info:
                    crop_name = crop_info['name']
                    scientific_name = crop_info['scientific']
                else:
                    crop_name = expected_key.capitalize()
                    scientific_name = ''
            else:
                crop_name = 'Unable to Identify'
                scientific_name = 'Unknown'
            disease_info = {'crop_name': crop_name, 'crop_scientific_name': scientific_name, 'description': 'Could not identify any crop/disease. Please provide a clearer image showing the affected plant part or consult a local agricultural extension officer.', 'prevention': ['General good farming practices'], 'control': ['Consult local agricultural extension officer for identification and treatment']}
            return {'success': True, 'disease_name': 'No Disease Detected', 'confidence': 0, 'disease_info': disease_info, 'disease_details': 'No predictions from model.', 'all_predictions': structured, 'expected_crop': expected_key}
    except requests.exceptions.HTTPError as e:
        logger.error(f'Roboflow API HTTP Error: {e.response.status_code} - {e.response.text}')
        return {'success': False, 'error': f'Roboflow API HTTP Error: {e.response.status_code} - {e.response.text}'}
    except Exception as e:
        logger.error(f'Roboflow API failed: {str(e)}', exc_info=True)
        return {'success': False, 'error': f'Roboflow API failed: {str(e)}'}