from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import logging
import os
from config import config, Config
from models import db
from routes.auth import init_auth_routes
from routes.analyze import analyze_bp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='production'):
    try:
        logger.info(f"Creating Flask app with config: {config_name}")
        app = Flask(__name__)
        app.config.from_object(config.get(config_name, config['production']))
        
        # Configure CORS - MUST be before registering blueprints
        CORS(app, supports_credentials=False)
        logger.info("CORS configured")
        
        db.init_app(app)
        JWTManager(app)
        
        # Initialize mail without crashing if config is wrong
        mail = Mail()
        try:
            mail.init_app(app)
            logger.info("Mail initialized successfully")
        except Exception as e:
            logger.warning(f"Mail initialization failed (non-critical): {e}")
            mail = None
        
        serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
        
        with app.app_context():
            try:
                db.create_all()
                logger.info("✅ Database tables created/verified successfully")
            except Exception as e:
                logger.error(f"⚠️ Database initialization error: {e}")
        
        auth_bp = init_auth_routes(app, mail, serializer)
        app.register_blueprint(auth_bp, url_prefix='/api')
        app.register_blueprint(analyze_bp, url_prefix='/api')
        logger.info("Blueprints registered")

        @app.route('/')
        @app.route('/api')
        def home():
            return (jsonify({'message': 'Mhenga Crop Bot API v2.0 - Running on Railway', 'version': '2.0', 'status': 'healthy'}), 200)
        
        @app.route('/api/health')
        def health():
            return (jsonify({'status': 'healthy', 'service': 'Mhenga Crop Bot API'}), 200)
        
        logger.info(f"✅ Flask app created successfully")
        return app
    except Exception as e:
        logger.error(f"Failed to create Flask app: {e}", exc_info=True)
        raise

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)