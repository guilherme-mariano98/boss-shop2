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
    
    # Set production environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
    os.environ.setdefault('DEBUG', 'False')
    
    # Copy production settings if needed
    production_settings_path = os.path.join(os.path.dirname(__file__), 'production_settings.py')
    if os.path.exists(production_settings_path):
        backend_dir = os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend', 'boss_shopp')
        if os.path.exists(backend_dir):
            import shutil
            shutil.copy2(production_settings_path, os.path.join(backend_dir, 'production_settings.py'))
    
    # Get port from environment (Render sets this automatically)
    port = os.environ.get('PORT', '8000')
    
    print("=" * 50)
    print("BOSS SHOP - Production Server")
    print("=" * 50)
    print(f"Starting Django server on port {port}")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend')
    
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
        print(f"Changed directory to: {backend_dir}")
        
        # Run Django migrations
        print("Running database migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        
        # Collect static files
        print("Collecting static files...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        
        # Start Django server
        print(f"Starting Django server on 0.0.0.0:{port}")
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}'
        ], check=True)
        
    else:
        print(f"Error: Backend directory not found at {backend_dir}")
        sys.exit(1)

if __name__ == "__main__":
    main()