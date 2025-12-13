#!/usr/bin/env python3
"""
Script para adicionar a importação do enhanced-styles.css em todos os arquivos HTML
"""
import os
import glob
import re

def fix_css_import_in_file(file_path):
    """Adiciona a importação do enhanced-styles.css se não existir"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se já tem a importação do enhanced-styles.css
        if 'enhanced-styles.css' in content:
            print(f"✅ {file_path} - já tem enhanced-styles.css")
            return False
        
        # Verifica se tem outras importações CSS
        css_pattern = r'<link rel="stylesheet" href="[^"]*\.css">'
        css_matches = re.findall(css_pattern, content)
        
        if not css_matches:
            print(f"⚠️  {file_path} - nenhuma importação CSS encontrada")
            return False
        
        # Encontra a última importação CSS e adiciona enhanced-styles.css depois
        last_css = css_matches[-1]
        new_css_line = '    <link rel="stylesheet" href="enhanced-styles.css">'
        
        # Substitui a última importação CSS
        new_content = content.replace(last_css, last_css + '\n' + new_css_line)
        
        # Salva o arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {file_path} - enhanced-styles.css adicionado")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def main():
    """Função principal"""
    print("🔄 Adicionando enhanced-styles.css em todos os arquivos HTML...")
    print("=" * 60)
    
    # Diretório do frontend
    frontend_dir = os.path.join('BOSS-SHOP1', 'frontend')
    
    if not os.path.exists(frontend_dir):
        print(f"❌ Diretório não encontrado: {frontend_dir}")
        return
    
    # Encontra todos os arquivos HTML
    html_files = glob.glob(os.path.join(frontend_dir, '*.html'))
    
    if not html_files:
        print("❌ Nenhum arquivo HTML encontrado!")
        return
    
    updated_count = 0
    total_files = len(html_files)
    
    # Processa cada arquivo
    for html_file in html_files:
        if fix_css_import_in_file(html_file):
            updated_count += 1
    
    print("=" * 60)
    print(f"📊 Resumo:")
    print(f"   Total de arquivos: {total_files}")
    print(f"   Arquivos atualizados: {updated_count}")
    print(f"   Arquivos já corretos: {total_files - updated_count}")
    print("✨ Processo concluído!")

if __name__ == "__main__":
    main()