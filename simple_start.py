#!/usr/bin/env python3
"""
Ultra-simple startup script for Boss Shop
"""
import os
import sys

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend')
os.chdir(backend_dir)

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
os.environ.setdefault('DEBUG', 'True')  # Enable debug for now to see errors

# Get port
port = os.environ.get('PORT', '10000')

# Import Django and start
import django
django.setup()

# Run migrations
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'migrate', '--noinput'])

# Collect static files
execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

# Start server
execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}', '--noreload'])