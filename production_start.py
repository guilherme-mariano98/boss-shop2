#!/usr/bin/env python3
"""
Simple production startup script for Boss Shop on Render
"""
import os
import sys
import subprocess

def main():
    print("=== Boss Shop Production Startup ===")
    
    # Get port from environment (Render sets this)
    port = os.environ.get('PORT', '10000')
    print(f"Starting on port: {port}")
    
    # Set working directory to BOSS-SHOP1/backend
    backend_path = os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend')
    
    if not os.path.exists(backend_path):
        print(f"Error: Backend directory not found at {backend_path}")
        sys.exit(1)
    
    print(f"Changing to backend directory: {backend_path}")
    os.chdir(backend_path)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
    os.environ.setdefault('DEBUG', 'False')
    
    # Run migrations
    print("Running Django migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=True)
        print("Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
    
    # Collect static files
    print("Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("Static files collected successfully")
    except subprocess.CalledProcessError as e:
        print(f"Static collection failed: {e}")
    
    # Start Django server directly (more reliable for this deployment)
    print(f"Starting Django server on 0.0.0.0:{port}")
    try:
        # Use Django's runserver for simplicity and reliability
        subprocess.run([
            sys.executable, 
            'manage.py', 
            'runserver', 
            f'0.0.0.0:{port}',
            '--noreload'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Django server failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()