@echo off
echo ========================================
echo CONFIGURANDO REPOSITORIO BOSS-SHOP2
echo ========================================

echo.
echo Removendo configuracao Git anterior...
rmdir /s /q .git 2>nul

echo.
echo Inicializando novo repositorio Git...
git init

echo.
echo Configurando repositorio remoto...
git remote add origin https://github.com/guilherme-mariano98/boss-shop2.git

echo.
echo Adicionando arquivos...
git add .

echo.
echo Fazendo commit inicial...
git commit -m "Initial commit: Boss Shop E-commerce Platform ready for Render deploy"

echo.
echo Configurando branch principal...
git branch -M main

echo.
echo Fazendo push para GitHub...
git push -u origin main

echo.
echo ========================================
echo REPOSITORIO CONFIGURADO COM SUCESSO!
echo ========================================
echo.
echo Proximo passo: Deploy no Render
echo 1. Acesse: https://render.com
echo 2. Clique em "New +" e "Web Service"
echo 3. Conecte ao repositorio: boss-shop2
echo 4. Render detectara automaticamente render.yaml
echo.
echo URL: https://github.com/guilherme-mariano98/boss-shop2
echo.

pause