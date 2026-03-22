import io
import pytest
import requests
from utils import ai_service

class DummyResponse:

    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(response=self)

def make_image():
    return io.BytesIO(b'dummy')

def test_detect_disease_return_all(monkeypatch):
    fake = {'predictions': [{'class': 'tomato_early_blight', 'confidence': 0.8}, {'class': 'maize_rust', 'confidence': 0.5}]}

    def fake_post(*args, **kwargs):
        return DummyResponse(fake)
    monkeypatch.setattr(requests, 'post', fake_post)
    result = ai_service.detect_disease(make_image(), return_all=True)
    assert result['success']
    assert 'all_predictions' in result
    assert len(result['all_predictions']) == 2
    assert result['raw'] == fake

def test_detect_disease_expected_crop_filters(monkeypatch):
    fake = {'predictions': [{'class': 'tomato_early_blight', 'confidence': 0.8}, {'class': 'maize_rust', 'confidence': 0.7}]}
    monkeypatch.setattr(requests, 'post', lambda *a, **k: DummyResponse(fake))
    result = ai_service.detect_disease(make_image(), expected_crop='maize')
    assert result['success']
    assert result['disease_name'] == 'maize_rust'
    assert result['confidence'] == 0.7
    assert any((p['crop_matches'] for p in result.get('all_predictions', [])))


def test_identify_crop_not_configured():
    result = ai_service.identify_crop(make_image())
    assert not result['success']
    assert result.get('requires_user_input') == True


def test_detect_disease_crop_mismatch_fallback_to_user_crop(monkeypatch):
    """Test that system returns a disease for the user's crop when model detects a different crop"""
    fake = {'predictions': [{'class': 'tomato_early_blight', 'confidence': 0.89}]}
    monkeypatch.setattr(requests, 'post', lambda *a, **k: DummyResponse(fake))
    result = ai_service.detect_disease(make_image(), expected_crop='maize')
    assert result['success']
    assert result['disease_info']['crop_name'].lower() in ['maize (corn)', 'maize', 'corn']
    assert result['expected_crop'] == 'maize'
    assert any(disease in result['disease_name'].lower() for disease in ['maize', 'corn'])


def test_detect_disease_crop_match_with_user_input(monkeypatch):
    """Test that system returns disease when model prediction matches user's specified crop"""
    fake = {'predictions': [{'class': 'maize_rust', 'confidence': 0.85}]}
    monkeypatch.setattr(requests, 'post', lambda *a, **k: DummyResponse(fake))
    result = ai_service.detect_disease(make_image(), expected_crop='maize')
    assert result['success']
    assert result['disease_name'] == 'maize_rust'
    assert result['confidence'] == 0.85
    assert 'maize' in result['disease_info']['crop_name'].lower()


def test_detect_disease_bean_mismatch_returns_bean_disease(monkeypatch):
    """Test that system returns a bean disease when user specifies bean but model detects tomato"""
    fake = {'predictions': [{'class': 'tomato_early_blight', 'confidence': 0.89}]}
    monkeypatch.setattr(requests, 'post', lambda *a, **k: DummyResponse(fake))
    result = ai_service.detect_disease(make_image(), expected_crop='bean')
    assert result['success']
    assert 'bean' in result['disease_info']['crop_name'].lower()
    assert result['expected_crop'] == 'bean'
    assert result['confidence'] == 0


def test_detect_disease_empty_image_no_predictions(monkeypatch):
    """Test that system handles images with no predictions by returning crop-specific disease"""
    fake = {'predictions': []}
    monkeypatch.setattr(requests, 'post', lambda *a, **k: DummyResponse(fake))
    result = ai_service.detect_disease(make_image(), expected_crop='maize')
    assert result['success']
    assert 'maize' in result['disease_info']['crop_name'].lower() or 'corn' in result['disease_info']['crop_name'].lower()
    assert result['expected_crop'] == 'maize'
