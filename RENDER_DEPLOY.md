# 🚀 Deploy Boss Shop no Render

## Passo 1: Executar Setup
Execute o arquivo `setup_repo.bat` para configurar o repositório.

## Passo 2: Deploy no Render

### 1. Acesse o Render
- Vá para [render.com](https://render.com)
- Faça login com GitHub

### 2. Criar Web Service
- Clique em **"New +"**
- Selecione **"Web Service"**
- Conecte ao repositório: `guilherme-mariano98/boss-shop2`

### 3. Configurações Automáticas
O Render detectará automaticamente:
- ✅ `render.yaml` (configuração completa)
- ✅ `requirements.txt` (dependências Python)
- ✅ `production_start.py` (script de inicialização)

### 4. Configurações do Service
- **Name**: boss-shop2
- **Environment**: Python 3
- **Build Command**: (automático via render.yaml)
- **Start Command**: (automático via render.yaml)

### 5. Deploy
- Clique em **"Create Web Service"**
- Aguarde o build (5-10 minutos)
- Sua aplicação estará online!

## 🌐 URL Final
Após o deploy: `https://boss-shop2.onrender.com`

## 🔄 Atualizações
Para atualizar a aplicação:
```bash
git add .
git commit -m "Update"
git push origin main
```

O Render fará deploy automático!

## ⚙️ Variáveis de Ambiente (Opcional)
No painel do Render, adicione:
- `SECRET_KEY`: chave secreta Django
- `DEBUG`: False

## 🆘 Problemas?
- Verifique logs no Render
- Confirme que `render.yaml` está correto
- Teste localmente com `python production_start.py`