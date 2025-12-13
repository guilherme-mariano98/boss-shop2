#!/usr/bin/env python3
"""
Script para adicionar a importação do footer-styles.css em todos os arquivos HTML
"""
import os
import glob
import re

def add_footer_css_to_file(file_path):
    """Adiciona a importação do footer-styles.css"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se já tem a importação do footer-styles.css
        if 'footer-styles.css' in content:
            return False
        
        # Procura por </head> para adicionar antes
        head_pattern = r'</head>'
        if not re.search(head_pattern, content):
            return False
        
        # Adiciona a importação do CSS do rodapé antes de </head>
        footer_css_line = '    <link rel="stylesheet" href="footer-styles.css">\n</head>'
        new_content = re.sub(head_pattern, footer_css_line, content)
        
        # Salva o arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {os.path.basename(file_path)} - footer-styles.css adicionado")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def main():
    """Função principal"""
    print("🔄 Adicionando footer-styles.css em todos os arquivos HTML...")
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
    
    # Processa cada arquivo
    for html_file in html_files:
        if add_footer_css_to_file(html_file):
            updated_count += 1
    
    print("=" * 60)
    print(f"📊 Total de arquivos atualizados: {updated_count}")
    print("✨ Processo concluído!")

if __name__ == "__main__":
    main()