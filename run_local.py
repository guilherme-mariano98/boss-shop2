#!/usr/bin/env python3
"""
Script simples para rodar o Boss Shop localmente
"""
import os
import sys
import subprocess

def main():
    print("=== BOSS SHOP - Servidor Local ===")
    
    # Navegar para o diretório do backend
    backend_dir = os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend')
    
    if not os.path.exists(backend_dir):
        print(f"Erro: Diretório backend não encontrado em {backend_dir}")
        return
    
    print(f"Mudando para diretório: {backend_dir}")
    os.chdir(backend_dir)
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
    os.environ.setdefault('DEBUG', 'True')
    
    # Executar migrações
    print("Executando migrações...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("Migrações concluídas!")
    except subprocess.CalledProcessError as e:
        print(f"Erro nas migrações: {e}")
    
    # Coletar arquivos estáticos
    print("Coletando arquivos estáticos...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("Arquivos estáticos coletados!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao coletar estáticos: {e}")
    
    # Iniciar servidor
    print("\n" + "="*50)
    print("SERVIDOR INICIADO!")
    print("Acesse: http://localhost:8000")
    print("Admin: http://localhost:8000/admin/")
    print("API: http://localhost:8000/api/health/")
    print("Pressione Ctrl+C para parar")
    print("="*50 + "\n")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\nServidor parado.")

if __name__ == "__main__":
    main()