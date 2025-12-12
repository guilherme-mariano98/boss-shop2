#!/usr/bin/env python3
"""
Flask application to start the entire Boss Shopp website.
This script coordinates the startup of both the frontend (Node.js) and backend (Django) services.
"""

import os
import sys
import subprocess
import threading
import time
import signal
import psutil
import webbrowser
import socket
from flask import Flask, jsonify

# Create Flask app
app = Flask(__name__)

# Global variables to track processes
frontend_process = None
backend_process = None
running = True

def kill_process_tree(pid):
    """Kill a process and all its child processes"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        parent.kill()
    except psutil.NoSuchProcess:
        pass

def start_frontend():
    """Start the Node.js frontend server"""
    global frontend_process
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'src', 'frontend')
    
    try:
        print("Starting frontend server...")
        frontend_process = subprocess.Popen(
            ['node', 'server.js'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Frontend server started with PID {frontend_process.pid}")
        
        # Monitor frontend output
        def monitor_frontend():
            if frontend_process.stdout:
                for line in iter(frontend_process.stdout.readline, b''):
                    try:
                        print(f"[FRONTEND] {line.decode('utf-8', errors='replace').strip()}")
                    except Exception:
                        pass
        
        threading.Thread(target=monitor_frontend, daemon=True).start()
        
    except Exception as e:
        print(f"Error starting frontend: {e}")

def start_backend():
    """Start the Django backend server"""
    global backend_process
    
    backend_dir = os.path.join(os.path.dirname(__file__), 'src', 'backend')
    
    try:
        print("Starting backend server...")
        backend_process = subprocess.Popen(
            [sys.executable, 'run_server.py'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Backend server started with PID {backend_process.pid}")
        
        # Monitor backend output
        def monitor_backend():
            if backend_process.stdout:
                for line in iter(backend_process.stdout.readline, b''):
                    try:
                        print(f"[BACKEND] {line.decode('utf-8', errors='replace').strip()}")
                    except Exception:
                        pass
        
        threading.Thread(target=monitor_backend, daemon=True).start()
        
    except Exception as e:
        print(f"Error starting backend: {e}")

def get_local_ip():
    """Detect local network IP address for LAN access"""
    ip = 'localhost'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass
    return ip

def open_website():
    """Open the website locally and show LAN URL"""
    time.sleep(8)  # Wait for servers to start
    try:
        local_ip = get_local_ip()
        # Prefer opening the LAN URL
        webbrowser.open(f"http://{local_ip}:8000")
        print("Website opened in your default browser!")
        print(f"Network access (LAN): http://{local_ip}:8000")
        print("Local access: http://localhost:8000")
        print("The website is now optimized for mobile devices!")
    except Exception as e:
        print(f"Could not open browser: {e}")

def stop_servers():
    """Stop all running servers"""
    global frontend_process, backend_process, running
    
    print("\nShutting down servers...")
    running = False
    
    if frontend_process and frontend_process.poll() is None:
        print("Stopping frontend server...")
        kill_process_tree(frontend_process.pid)
        frontend_process.wait()
    
    if backend_process and backend_process.poll() is None:
        print("Stopping backend server...")
        kill_process_tree(backend_process.pid)
        backend_process.wait()
    
    print("All servers stopped.")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\nReceived interrupt signal')
    stop_servers()
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.route('/')
def index():
    """Health check endpoint"""
    local_ip = get_local_ip()
    return jsonify({
        "status": "OK",
        "message": "Boss Shopp main coordinator is running",
        "services": {
            "frontend_local": "http://localhost:8000",
            "frontend_network": f"http://{local_ip}:8000",
            "backend_api": "http://localhost:8000/api/",
            "backend_admin": "http://localhost:8000/admin/"
        },
        "mobile_support": "Enabled - Website optimized for mobile devices"
    })

@app.route('/health')
def health():
    """Detailed health check endpoint"""
    frontend_status = "running" if frontend_process and frontend_process.poll() is None else "stopped"
    backend_status = "running" if backend_process and backend_process.poll() is None else "stopped"
    local_ip = get_local_ip()
    
    return jsonify({
        "status": "OK",
        "frontend": {
            "status": frontend_status,
            "pid": frontend_process.pid if frontend_process else None
        },
        "backend": {
            "status": backend_status,
            "pid": backend_process.pid if backend_process else None
        },
        "urls": {
            "frontend_local": "http://localhost:8000",
            "frontend_network": f"http://{local_ip}:8000",
            "backend_api": "http://localhost:8000/api/",
            "backend_admin": "http://localhost:8000/admin/"
        },
        "mobile_support": "enabled"
    })

def main():
    """Main function to start all services"""
    print("=" * 50)
    print("BOSS SHOPP - Website Coordinator")
    print("=" * 50)
    print("Mobile support: ENABLED")
    print("Optimizations for touch devices and small screens")
    local_ip = get_local_ip()
    
    # Start services
    start_backend()
    time.sleep(5)  # Give backend time to initialize
    start_frontend()
    
    # Open website in browser
    browser_thread = threading.Thread(target=open_website, daemon=True)
    browser_thread.start()
    
    # Wait a moment for services to start
    time.sleep(3)
    
    print("\nServices started:")
    print("- Frontend (local): http://localhost:8000")
    print(f"- Frontend (network): http://{local_ip}:8000")
    print("- Backend API: http://localhost:8000/api/")
    print("- Backend Admin: http://localhost:8000/admin/")
    print("\nThe website should now be open in your browser!")
    print("Mobile optimizations are enabled for all devices!")
    print("If not, please manually visit: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services")
    
    # Keep the main thread alive
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_servers()

if __name__ == "__main__":
    # Check if running on Render or other cloud platform
    port = os.environ.get('PORT')
    if port:
        # Running on cloud platform - start Django directly
        print(f"Running on cloud platform - starting Django on port {port}")
        
        # Try different possible backend directories
        possible_dirs = [
            os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend'),
            os.path.join(os.path.dirname(__file__), 'src', 'backend'),
            os.path.join(os.path.dirname(__file__), 'backend'),
        ]
        
        backend_dir = None
        for dir_path in possible_dirs:
            print(f"Checking directory: {dir_path}")
            if os.path.exists(dir_path):
                print(f"Directory exists: {dir_path}")
                manage_py_path = os.path.join(dir_path, 'manage.py')
                run_server_path = os.path.join(dir_path, 'run_server.py')
                print(f"Looking for manage.py at: {manage_py_path}")
                print(f"Looking for run_server.py at: {run_server_path}")
                if os.path.exists(manage_py_path) or os.path.exists(run_server_path):
                    backend_dir = dir_path
                    print(f"Found backend directory: {backend_dir}")
                    break
            else:
                print(f"Directory does not exist: {dir_path}")
        
        if backend_dir:
            os.chdir(backend_dir)
            print(f"Changed to directory: {backend_dir}")
            
            # Check if run_server.py exists and use it, otherwise use manage.py
            run_server_path = os.path.join(backend_dir, 'run_server.py')
            manage_py_path = os.path.join(backend_dir, 'manage.py')
            
            if os.path.exists(run_server_path):
                print(f"Using run_server.py for startup")
                os.system(f"python run_server.py")
            elif os.path.exists(manage_py_path):
                print(f"Using manage.py for startup")
                # Set Django settings
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
                os.environ.setdefault('DEBUG', 'False')
                
                # Run migrations and collect static files
                print("Running migrations...")
                os.system("python manage.py migrate --noinput")
                
                print("Collecting static files...")
                os.system("python manage.py collectstatic --noinput")
                
                # Start Django server
                print(f"Starting Django server on 0.0.0.0:{port}")
                os.system(f"python manage.py runserver 0.0.0.0:{port}")
            else:
                print("Error: Neither run_server.py nor manage.py found!")
                sys.exit(1)
        else:
            print("Error: No valid Django backend directory found!")
            print("Searched in:")
            for dir_path in possible_dirs:
                print(f"  - {dir_path}")
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "flask":
        # Local Flask mode
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        # Local coordinator mode
        main()
