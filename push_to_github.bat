@echo off
echo ========================================
echo BOSS SHOP - Push para GitHub
echo ========================================

echo.
echo Verificando status do Git...
git status

echo.
echo Adicionando todos os arquivos...
git add .

echo.
echo Fazendo commit das alteracoes...
set /p commit_msg="Digite a mensagem do commit (ou pressione Enter para usar padrao): "
if "%commit_msg%"=="" set commit_msg=Update: Boss Shop deployment configuration

git commit -m "%commit_msg%"

echo.
echo Fazendo push para o repositorio...
git push origin main

echo.
echo ========================================
echo Push concluido com sucesso!
echo ========================================
echo.
echo Proximo passo: Configure o deploy no Render
echo 1. Acesse: https://render.com
echo 2. Clique em "New +" e selecione "Web Service"
echo 3. Conecte ao repositorio: boss-shop2
echo 4. O Render detectara automaticamente o render.yaml
echo.
echo URL do repositorio: https://github.com/guilherme-mariano98/boss-shop2
echo.

pause