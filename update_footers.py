#!/usr/bin/env python3
"""
Script para atualizar o rodapé em todas as páginas HTML do Boss Shop
"""
import os
import re
import glob

def get_new_footer():
    """Retorna o HTML do novo rodapé"""
    return '''    <!-- Footer Moderno e Responsivo -->
    <footer class="modern-footer">
        <div class="container">
            <!-- Seção Principal do Footer -->
            <div class="footer-main">
                <div class="footer-grid">
                    <!-- Coluna 1: Sobre a Empresa -->
                    <div class="footer-column">
                        <div class="footer-logo">
                            <img src="boss-shop-logo.png" alt="BOSS SHOPP" class="footer-logo-img">
                            <h3>BOSS SHOPP</h3>
                        </div>
                        <p class="footer-description">
                            Sua loja online de confiança, oferecendo produtos de qualidade com preços competitivos e entrega rápida em todo o Brasil.
                        </p>
                        <div class="footer-social">
                            <a href="#" class="social-link" aria-label="Facebook">
                                <i class="fab fa-facebook-f"></i>
                            </a>
                            <a href="#" class="social-link" aria-label="Instagram">
                                <i class="fab fa-instagram"></i>
                            </a>
                            <a href="#" class="social-link" aria-label="Twitter">
                                <i class="fab fa-twitter"></i>
                            </a>
                            <a href="#" class="social-link" aria-label="WhatsApp">
                                <i class="fab fa-whatsapp"></i>
                            </a>
                        </div>
                    </div>

                    <!-- Coluna 2: Links Rápidos -->
                    <div class="footer-column">
                        <h4 class="footer-title">Links Rápidos</h4>
                        <ul class="footer-links">
                            <li><a href="index.html">Início</a></li>
                            <li><a href="categorias.html">Categorias</a></li>
                            <li><a href="sobre.html">Sobre Nós</a></li>
                            <li><a href="como-comprar.html">Como Comprar</a></li>
                            <li><a href="frete-entrega.html">Frete e Entrega</a></li>
                            <li><a href="devolucoes.html">Trocas e Devoluções</a></li>
                        </ul>
                    </div>

                    <!-- Coluna 3: Categorias -->
                    <div class="footer-column">
                        <h4 class="footer-title">Categorias</h4>
                        <ul class="footer-links">
                            <li><a href="categoria-moda.html">Moda</a></li>
                            <li><a href="categoria-eletronicos.html">Eletrônicos</a></li>
                            <li><a href="categoria-casa.html">Casa e Decoração</a></li>
                            <li><a href="categoria-esportes.html">Esportes</a></li>
                            <li><a href="categoria-games.html">Games</a></li>
                            <li><a href="categoria-infantil.html">Infantil</a></li>
                        </ul>
                    </div>

                    <!-- Coluna 4: Atendimento -->
                    <div class="footer-column">
                        <h4 class="footer-title">Atendimento</h4>
                        <div class="contact-info">
                            <div class="contact-item">
                                <i class="fas fa-phone"></i>
                                <span>(11) 4002-8922</span>
                            </div>
                            <div class="contact-item">
                                <i class="fas fa-envelope"></i>
                                <span>contato@bossshopp.com</span>
                            </div>
                            <div class="contact-item">
                                <i class="fas fa-clock"></i>
                                <span>Seg-Sex: 8h às 18h</span>
                            </div>
                            <div class="contact-item">
                                <i class="fas fa-map-marker-alt"></i>
                                <span>São Paulo, SP</span>
                            </div>
                        </div>
                        <a href="central-ajuda.html" class="help-button">
                            <i class="fas fa-headset"></i>
                            Central de Ajuda
                        </a>
                    </div>
                </div>
            </div>

            <!-- Seção de Pagamento e Segurança -->
            <div class="footer-payment">
                <div class="payment-security">
                    <div class="payment-methods">
                        <h5>Formas de Pagamento</h5>
                        <div class="payment-icons">
                            <i class="fab fa-cc-visa" title="Visa"></i>
                            <i class="fab fa-cc-mastercard" title="Mastercard"></i>
                            <i class="fab fa-cc-amex" title="American Express"></i>
                            <i class="fab fa-pix" title="PIX"></i>
                            <i class="fas fa-barcode" title="Boleto"></i>
                        </div>
                    </div>
                    <div class="security-badges">
                        <h5>Segurança</h5>
                        <div class="security-icons">
                            <i class="fas fa-shield-alt" title="Site Seguro"></i>
                            <i class="fas fa-lock" title="SSL"></i>
                            <i class="fas fa-certificate" title="Certificado"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Rodapé Inferior -->
            <div class="footer-bottom">
                <div class="footer-bottom-content">
                    <div class="copyright">
                        <p>&copy; 2025 BOSS SHOPP. Todos os direitos reservados.</p>
                    </div>
                    <div class="footer-legal">
                        <a href="#" class="legal-link">Política de Privacidade</a>
                        <a href="#" class="legal-link">Termos de Uso</a>
                        <a href="#" class="legal-link">Cookies</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>'''

def update_footer_in_file(file_path):
    """Atualiza o rodapé em um arquivo HTML específico"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Padrão para encontrar o footer antigo
        footer_pattern = r'<!-- Footer -->\s*<footer class="footer">.*?</footer>'
        
        # Se não encontrar o padrão acima, tenta outros padrões
        if not re.search(footer_pattern, content, re.DOTALL):
            footer_pattern = r'<footer[^>]*>.*?</footer>'
        
        # Substitui o footer antigo pelo novo
        new_content = re.sub(footer_pattern, get_new_footer(), content, flags=re.DOTALL)
        
        # Se houve mudança, salva o arquivo
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Rodapé atualizado em: {file_path}")
            return True
        else:
            print(f"⚠️  Nenhum rodapé encontrado em: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def main():
    """Função principal"""
    print("🔄 Atualizando rodapés em todas as páginas HTML...")
    print("=" * 50)
    
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
    
    # Atualiza cada arquivo
    for html_file in html_files:
        if update_footer_in_file(html_file):
            updated_count += 1
    
    print("=" * 50)
    print(f"📊 Resumo:")
    print(f"   Total de arquivos: {total_files}")
    print(f"   Arquivos atualizados: {updated_count}")
    print(f"   Arquivos sem alteração: {total_files - updated_count}")
    print("✨ Processo concluído!")

if __name__ == "__main__":
    main()