#!/usr/bin/env python
"""
Deployment validation and setup helper script
Checks if the project is ready for deployment to Vercel
"""

import os
import json
import secrets
from pathlib import Path

def check_file_exists(filepath):
    """Check if a critical file exists"""
    return Path(filepath).exists()

def check_environment_variables():
    """Check if important environment variables are set"""
    required_vars = [
        'ROBOFLOW_API_KEY',
        'JWT_SECRET_KEY',
        'AGROMONITORING_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    return missing

def generate_jwt_secret():
    """Generate a secure JWT secret"""
    return secrets.token_hex(32)

def main():
    print("🚀 Mhenga Crop Bot - Deployment Validation\n")
    print("=" * 50)
    
    # Check critical files
    print("\n✓ Checking deployment files...")
    files_to_check = [
        'vercel.json',
        'Procfile',
        'runtime.txt',
        '.env.example',
        'requirements.txt',
        'package.json',
        'VERCEL_DEPLOYMENT.md'
    ]
    
    missing_files = []
    for file in files_to_check:
        if check_file_exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing_files.append(file)
    
    # Check frontend files
    print("\n✓ Checking frontend configuration...")
    frontend_files = [
        'index.html',
        'js/config.js',
        'js/analyze.js',
        'js/auth.js',
        'js/utils.js'
    ]
    
    for file in frontend_files:
        if check_file_exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    # Check backend files
    print("\n✓ Checking backend configuration...")
    backend_files = [
        'app.py',
        'config.py',
        'models.py',
        'routes/auth.py',
        'routes/analyze.py'
    ]
    
    for file in backend_files:
        if check_file_exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file}")
    
    # Check .env file
    print("\n✓ Checking environment setup...")
    if os.path.exists('.env'):
        print("  ✅ .env file exists")
    else:
        print("  ⚠️  .env file not found (copy from .env.example)")
    
    # Check requirements.txt for deployment packages
    print("\n✓ Checking dependency configuration...")
    with open('requirements.txt', 'r') as f:
        reqs = f.read().lower()
        
    required_packages = {
        'flask': 'Flask',
        'gunicorn': 'Gunicorn (for production)',
        'flask-cors': 'Flask-CORS',
        'flask-jwt-extended': 'JWT Support'
    }
    
    for package, display_name in required_packages.items():
        if package in reqs:
            print(f"  ✅ {display_name}")
        else:
            print(f"  ❌ {display_name} (add to requirements.txt)")
    
    # Environment variables
    print("\n✓ Checking environment variables...")
    env_file_exists = os.path.exists('.env')
    
    if env_file_exists:
        # Load .env
        from dotenv import load_dotenv
        load_dotenv()
    
    critical_vars = [
        ('ROBOFLOW_API_KEY', 'Roboflow API Key'),
        ('JWT_SECRET_KEY', 'JWT Secret Key'),
        ('AGROMONITORING_API_KEY', 'AgroMonitoring API Key'),
        ('MAIL_USERNAME', 'Mail Server Username'),
        ('MAIL_PASSWORD', 'Mail Server Password')
    ]
    
    missing_env = []
    for var, display_name in critical_vars:
        if os.getenv(var):
            print(f"  ✅ {display_name}")
        else:
            print(f"  ❌ {display_name}")
            missing_env.append(var)
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT CHECKLIST\n")
    
    if missing_files:
        print(f"❌ Missing deployment files ({len(missing_files)}):")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("✅ All deployment files present")
    
    if missing_env:
        print(f"\n⚠️  Missing environment variables ({len(missing_env)}):")
        for var in missing_env:
            print(f"   - {var}")
        print("\n💡 Add these to your .env file before deployment")
    else:
        print("\n✅ All environment variables configured")
    
    # Helpful hints
    print("\n" + "=" * 50)
    print("💡 HELPFUL HINTS\n")
    
    if not os.getenv('JWT_SECRET_KEY'):
        print("Generate a secure JWT_SECRET_KEY:")
        print(f"  JWT_SECRET_KEY={generate_jwt_secret()}\n")
    
    print("Deployment Guide:")
    print("  1. Read VERCEL_DEPLOYMENT.md for detailed steps")
    print("  2. Read DEPLOYMENT_QUICKSTART.md for quick reference")
    print("  3. Review DEPLOYMENT_ARCHITECTURE.md for technical details")
    
    print("\n" + "=" * 50)
    print("\n🎯 Next Steps:\n")
    print("1. $ copy .env.example .env")
    print("2. Edit .env with your API keys and secrets")
    print("3. $ git add .")
    print("4. $ git commit -m 'Add deployment configuration'")
    print("5. $ git push origin main")
    print("6. Go to railway.app to deploy backend")
    print("7. Go to vercel.com to deploy frontend")
    
    return 0 if not missing_env else 1

if __name__ == '__main__':
    exit(main())
