from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config, Config
from models import db
from routes.auth import init_auth_routes
from routes.analyze import analyze_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['development']))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    db.init_app(app)
    JWTManager(app)
    mail = Mail(app)
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    with app.app_context():
        db.create_all()
    auth_bp = init_auth_routes(app, mail, serializer)
    app.register_blueprint(auth_bp)
    app.register_blueprint(analyze_bp)

    @app.route('/')
    def home():
        return (jsonify({'message': 'Mhenga Crop Bot API v2.0 - Running on Vercel', 'version': '2.0', 'status': 'healthy'}), 200)
    
    @app.route('/api/health')
    def health():
        return (jsonify({'status': 'healthy', 'service': 'Mhenga Crop Bot API'}), 200)
    
    return app

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run(debug=False)
