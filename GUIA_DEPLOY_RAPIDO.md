# 🚀 Guia Rápido de Deploy - Streamlit Cloud

## Método Mais Simples (5 minutos)

### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Crie um novo repositório (ex: `dashboard-zappa`)
3. **NÃO** inicialize com README (já temos um)

### Passo 2: Preparar Arquivos Localmente

```powershell
# No diretório do projeto
cd "c:\Users\vini\Desktop\dashboard zappa"

# Inicializar Git (se ainda não fez)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Dashboard Streamlit - Deploy inicial"

# Conectar ao GitHub (substitua SEU_USUARIO e SEU_REPOSITORIO)
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### Passo 3: Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Preencha:
   - **Repository**: Seu repositório (ex: `SEU_USUARIO/dashboard-zappa`)
   - **Branch**: `main`
   - **Main file path**: `app/main.py`
   - **App URL**: Escolha um nome (ex: `dashboard-zappa`)
5. Clique em **"Deploy!"**

### Passo 4: Aguardar Deploy

- O deploy leva 1-2 minutos
- Você verá o progresso na tela
- Quando terminar, clique em "View app"

### ✅ Pronto!

Seu dashboard estará em: `https://dashboard-zappa.streamlit.app`

---

## ⚠️ IMPORTANTE: Dados Sensíveis

**NÃO faça commit do arquivo Excel com dados reais!**

O arquivo `modelo Power BI .xlsx` está no `.gitignore` e não será enviado.

Para o deploy funcionar, você tem 2 opções:

### Opção A: Usar Arquivo de Exemplo (Recomendado)

```powershell
# Criar arquivo de exemplo
python script_criar_exemplo.py

# Este arquivo será versionado e usado no deploy
```

### Opção B: Upload Manual no Streamlit Cloud

1. Após o deploy, vá em **Settings** → **Secrets**
2. Adicione o arquivo Excel como secret (não recomendado para arquivos grandes)
3. Ou use um serviço de storage (S3, Google Drive, etc.)

---

## 🔄 Atualizar o Dashboard

Sempre que fizer mudanças:

```powershell
git add .
git commit -m "Descrição das mudanças"
git push
```

O Streamlit Cloud atualiza automaticamente!

---

## 📝 Checklist Antes do Deploy

- [ ] Código testado localmente
- [ ] `requirements.txt` completo
- [ ] `.gitignore` configurado
- [ ] Arquivo de exemplo criado (se necessário)
- [ ] Repositório GitHub criado
- [ ] Código enviado para GitHub

---

## 🆘 Problemas Comuns

### "Module not found"
- Verifique se todas as dependências estão em `requirements.txt`

### "File not found"
- O arquivo Excel precisa estar no repositório OU
- Use o arquivo de exemplo: `python script_criar_exemplo.py`

### Deploy falha
- Verifique os logs no Streamlit Cloud
- Certifique-se que `app/main.py` existe e está correto

---

**Dúvidas?** Consulte `DEPLOY.md` para mais detalhes.
