#!/usr/bin/env python3
"""
Script para inicializar o banco de dados SQLite do Boss Shop
"""
import os
import sys
import subprocess

def main():
    print("🗄️  INICIALIZANDO BANCO DE DADOS BOSS SHOP")
    print("=" * 50)
    
    # Navegar para o diretório do backend
    backend_dir = os.path.join(os.path.dirname(__file__), 'BOSS-SHOP1', 'backend')
    
    if not os.path.exists(backend_dir):
        print(f"❌ Diretório backend não encontrado: {backend_dir}")
        return False
    
    print(f"📁 Mudando para diretório: {backend_dir}")
    os.chdir(backend_dir)
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_shopp.settings')
    
    try:
        # 1. Executar migrações
        print("\n1️⃣  Executando migrações do Django...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrações executadas com sucesso!")
        else:
            print(f"❌ Erro nas migrações: {result.stderr}")
            return False
        
        # 2. Criar superusuário (se não existir)
        print("\n2️⃣  Verificando superusuário...")
        try:
            import django
            django.setup()
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            if not User.objects.filter(is_superuser=True).exists():
                print("Criando superusuário admin...")
                User.objects.create_superuser(
                    username='admin',
                    email='admin@bossshopp.com',
                    password='admin123'
                )
                print("✅ Superusuário criado: admin / admin123")
            else:
                print("✅ Superusuário já existe")
        except Exception as e:
            print(f"⚠️  Aviso ao criar superusuário: {e}")
        
        # 3. Popular dados iniciais
        print("\n3️⃣  Populando dados iniciais...")
        result = subprocess.run([sys.executable, 'populate_data.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dados iniciais populados com sucesso!")
            print(result.stdout)
        else:
            print(f"❌ Erro ao popular dados: {result.stderr}")
            return False
        
        # 4. Verificar banco de dados
        print("\n4️⃣  Verificando banco de dados...")
        db_path = os.path.join(backend_dir, 'db.sqlite3')
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"✅ Banco de dados criado: {db_path}")
            print(f"📊 Tamanho: {size:,} bytes")
        else:
            print("❌ Arquivo do banco de dados não encontrado!")
            return False
        
        # 5. Mostrar estatísticas
        print("\n5️⃣  Estatísticas do banco de dados:")
        try:
            from api.models import Category, Product, User
            
            categories_count = Category.objects.count()
            products_count = Product.objects.count()
            users_count = User.objects.count()
            
            print(f"👥 Usuários: {users_count}")
            print(f"📂 Categorias: {categories_count}")
            print(f"🛍️  Produtos: {products_count}")
            
        except Exception as e:
            print(f"⚠️  Erro ao obter estatísticas: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 BANCO DE DADOS INICIALIZADO COM SUCESSO!")
        print("\n📋 Informações de acesso:")
        print("   🌐 Admin: http://localhost:8000/admin/")
        print("   👤 Usuário: admin")
        print("   🔑 Senha: admin123")
        print("\n🚀 Para iniciar o servidor:")
        print("   python run_local.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a inicialização: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)