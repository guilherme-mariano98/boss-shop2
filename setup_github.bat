@echo off
echo ========================================
echo BOSS SHOP - Configuracao GitHub e Render
echo ========================================

echo.
echo 1. Inicializando repositorio Git...
git init

echo.
echo 2. Adicionando arquivos ao Git...
git add .

echo.
echo 3. Fazendo primeiro commit...
git commit -m "Initial commit: Boss Shop E-commerce Platform"

echo.
echo 4. Configurando branch principal...
git branch -M main

echo.
echo ========================================
echo PROXIMOS PASSOS:
echo ========================================
echo.
echo 1. Crie um repositorio no GitHub:
echo    - Va para https://github.com/new
echo    - Nome: boss-shop
echo    - Deixe publico ou privado conforme preferir
echo    - NAO inicialize com README (ja temos um)
echo.
echo 2. Conecte ao repositorio remoto:
echo    git remote add origin git@github.com:guilherme-mariano98/boss-shop2.git
echo    git push -u origin main
echo.
echo 3. Configure o deploy no Render:
echo    - Va para https://render.com
echo    - Clique em "New +" e selecione "Web Service"
echo    - Conecte sua conta GitHub
echo    - Selecione o repositorio boss-shop
echo    - O Render detectara automaticamente o render.yaml
echo    - Clique em "Create Web Service"
echo.
echo 4. Variaveis de ambiente no Render (opcional):
echo    - DEBUG=False
echo    - SECRET_KEY=sua-chave-secreta-aqui
echo.
echo ========================================
echo Repositorio Git configurado com sucesso!
echo ========================================

pause