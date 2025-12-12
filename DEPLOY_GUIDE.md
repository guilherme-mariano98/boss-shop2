# 🚀 Guia de Deploy - Boss Shop

Este guia te ajudará a colocar o Boss Shop online usando GitHub e Render.

## 📋 Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta no [Render](https://render.com) (gratuita)
- Git instalado no seu computador

## 🔧 Passo 1: Configurar o Repositório GitHub

### 1.1 Execute o script de configuração
```bash
setup_github.bat
```

### 1.2 Crie o repositório no GitHub
1. Acesse [https://github.com/new](https://github.com/new)
2. Nome do repositório: `boss-shop`
3. Deixe público ou privado conforme preferir
4. **NÃO** marque "Add a README file" (já temos um)
5. Clique em "Create repository"

### 1.3 Conecte o repositório local ao GitHub
```bash
git remote add origin git@github.com:guilherme-mariano98/boss-shop2.git
git push -u origin main
```

## 🌐 Passo 2: Deploy no Render

### 2.1 Acesse o Render
1. Vá para [https://render.com](https://render.com)
2. Faça login ou crie uma conta gratuita
3. Conecte sua conta GitHub

### 2.2 Crie o Web Service
1. Clique em "New +" no dashboard
2. Selecione "Web Service"
3. Conecte ao seu repositório `boss-shop`
4. Configure:
   - **Name**: boss-shop
   - **Environment**: Python 3
   - **Build Command**: (deixe vazio, usaremos o render.yaml)
   - **Start Command**: (deixe vazio, usaremos o render.yaml)

### 2.3 Configurações Automáticas
O Render detectará automaticamente:
- ✅ `render.yaml` - Configurações de build e deploy
- ✅ `requirements.txt` - Dependências Python
- ✅ `runtime.txt` - Versão do Python

### 2.4 Variáveis de Ambiente (Opcional)
No painel do Render, adicione:
- `SECRET_KEY`: Uma chave secreta para o Django
- `DEBUG`: False (para produção)

## 🎉 Passo 3: Verificar o Deploy

### 3.1 Acompanhe o Build
- O Render mostrará os logs de build em tempo real
- O processo pode levar 5-10 minutos na primeira vez

### 3.2 Acesse sua aplicação
- Após o deploy, você receberá uma URL como: `https://boss-shop.onrender.com`
- A aplicação estará disponível globalmente!

## 🔄 Atualizações Automáticas

Toda vez que você fizer push para o branch `main`:
```bash
git add .
git commit -m "Suas alterações"
git push origin main
```

O Render fará o deploy automático das mudanças!

## 🛠️ Estrutura do Projeto

```
boss-shop/
├── BOSS-SHOP1/          # Código principal
│   ├── backend/         # Django backend
│   └── frontend/        # Frontend files
├── render.yaml          # Configuração Render
├── requirements.txt     # Dependências Python
├── production_start.py  # Script de produção
├── setup_github.bat     # Script de configuração
└── README.md           # Documentação
```

## 🆘 Solução de Problemas

### Build falha?
- Verifique os logs no Render
- Confirme que todas as dependências estão no `requirements.txt`

### Aplicação não carrega?
- Verifique se o `production_start.py` está funcionando
- Confirme as variáveis de ambiente

### Erro de banco de dados?
- O Render usa SQLite por padrão
- Para PostgreSQL, adicione a variável `DATABASE_URL`

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no Render
2. Consulte a documentação do [Render](https://render.com/docs)
3. Abra uma issue no repositório GitHub

---

🎊 **Parabéns!** Seu Boss Shop agora está online e acessível para o mundo todo!