#!/usr/bin/env python3
"""
Production startup script for Boss Shop on Render.
This script handles the Django application startup for production deployment.
"""

import os
import sys
import subprocess

def main():
    """Main function to start Django in production mode"""
    
    # Get port from environment (Render sets this automatically)
    port = os.environ.get('PORT', '8000')
    
    print("=" * 50)
    print("BOSS SHOP - Production Server")
    print("=" * 50)
    print(f"Starting Django server on port {port}")
    
    # Try different possible backend directories
    possible_dirs = [
        os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend'),
        os.path.join(os.path.dirname(__file__), 'src', 'backend'),
        os.path.join(os.path.dirname(__file__), 'backend'),
    ]
    
    backend_dir = None
    for dir_path in possible_dirs:
        if os.path.exists(dir_path) and os.path.exists(os.path.join(dir_path, 'manage.py')):
            backend_dir = dir_path
            break
    
    if backend_dir:
        os.chdir(backend_dir)
        print(f"Changed directory to: {backend_dir}")
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
        os.environ.setdefault('DEBUG', 'False')
        
        try:
            # Run Django migrations
            print("Running database migrations...")
            subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=False)
            
            # Collect static files
            print("Collecting static files...")
            subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=False)
            
            # Start Django server with gunicorn for production
            print(f"Starting Django server on 0.0.0.0:{port}")
            
            # Try to use gunicorn first, fallback to runserver
            try:
                subprocess.run([
                    'gunicorn', 'boss_shopp.wsgi:application',
                    '--bind', f'0.0.0.0:{port}',
                    '--workers', '3'
                ], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Gunicorn not available, using Django runserver...")
                subprocess.run([
                    sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}'
                ], check=True)
                
        except Exception as e:
            print(f"Error during startup: {e}")
            sys.exit(1)
        
    else:
        print("Error: No valid Django backend directory found!")
        print("Searched in:")
        for dir_path in possible_dirs:
            print(f"  - {dir_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()