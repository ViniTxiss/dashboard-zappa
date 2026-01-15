# 🚀 Guia de Deploy - Dashboard Streamlit

Este guia mostra como fazer deploy do dashboard em diferentes plataformas.

## 📦 Opção 1: Streamlit Community Cloud (RECOMENDADO - GRATUITO)

A forma mais simples e rápida de fazer deploy!

### Pré-requisitos:
1. Conta no GitHub (gratuita)
2. Conta no Streamlit Cloud (gratuita)

### Passo a Passo:

#### 1. Preparar o Repositório GitHub

```bash
# Inicialize o Git (se ainda não fez)
git init

# Adicione todos os arquivos
git add .

# Faça o commit
git commit -m "Dashboard Streamlit - Deploy inicial"

# Crie um repositório no GitHub e adicione o remote
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANTE:** 
- NÃO faça commit do arquivo Excel com dados sensíveis!
- Adicione `modelo Power BI .xlsx` ao `.gitignore` se contiver dados confidenciais
- Ou crie um arquivo de exemplo para o repositório

#### 2. Fazer Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Preencha:
   - **Repository**: Seu repositório GitHub
   - **Branch**: `main` (ou `master`)
   - **Main file path**: `app/main.py`
   - **App URL**: Escolha um nome único (ex: `dashboard-zappa`)
5. Clique em "Deploy!"

#### 3. Configurar Variáveis (se necessário)

Se precisar de variáveis de ambiente:
- Vá em "Settings" → "Secrets"
- Adicione variáveis se necessário

### ✅ Pronto!
Seu dashboard estará disponível em: `https://SEU-APP-NAME.streamlit.app`

---

## 📦 Opção 2: Railway (Alternativa Moderna)

### Passo a Passo:

1. Acesse: https://railway.app/
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório
6. Railway detectará automaticamente que é um app Python
7. Configure:
   - **Start Command**: `streamlit run app/main.py --server.port $PORT`
8. Adicione o arquivo Excel como arquivo estático ou use variáveis de ambiente

---

## 📦 Opção 3: Render

### Passo a Passo:

1. Acesse: https://render.com/
2. Faça login com GitHub
3. Clique em "New" → "Web Service"
4. Conecte seu repositório
5. Configure:
   - **Name**: `dashboard-zappa`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0`
6. Clique em "Create Web Service"

---

## 📦 Opção 4: Docker + Servidor Próprio

### Criar Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build e Run:

```bash
docker build -t dashboard-zappa .
docker run -p 8501:8501 dashboard-zappa
```

---

## 🔒 Segurança e Boas Práticas

### 1. Proteger Dados Sensíveis

**NÃO faça commit de:**
- Arquivos Excel com dados reais
- Credenciais ou API keys
- Informações pessoais

**Solução:**
- Use `.gitignore` para excluir arquivos sensíveis
- Crie um arquivo de exemplo: `modelo Power BI - exemplo.xlsx`
- Use variáveis de ambiente para configurações sensíveis

### 2. Atualizar .gitignore

Certifique-se de que seu `.gitignore` inclui:

```
# Dados sensíveis
*.xlsx
*.xls
*.csv
!modelo Power BI - exemplo.xlsx  # Mantém apenas exemplo

# Secrets
.env
secrets.toml
```

### 3. Criar Arquivo de Exemplo

Crie um arquivo Excel de exemplo para o repositório:

```python
# script_criar_exemplo.py
import pandas as pd

# Dados de exemplo
dados_exemplo = {
    'Motorista': ['Motorista A', 'Motorista B', 'Motorista C'],
    'KM': [100.5, 150.2, 120.8],
    'SPR': [50, 75, 60],
    'Paradas': [10, 15, 12]
}

df = pd.DataFrame(dados_exemplo)
df.to_excel('modelo Power BI - exemplo.xlsx', index=False)
print("Arquivo de exemplo criado!")
```

---

## 📝 Checklist de Deploy

Antes de fazer deploy, verifique:

- [ ] Código testado localmente
- [ ] `requirements.txt` atualizado
- [ ] `.gitignore` configurado corretamente
- [ ] Dados sensíveis removidos do repositório
- [ ] Arquivo de exemplo criado (se necessário)
- [ ] README.md atualizado
- [ ] Caminho do arquivo Excel ajustado (se necessário)

---

## 🐛 Troubleshooting

### Erro: "Module not found"
**Solução:** Verifique se todas as dependências estão em `requirements.txt`

### Erro: "File not found"
**Solução:** 
- Verifique o caminho do arquivo Excel
- Use caminhos relativos
- Considere usar variáveis de ambiente para o caminho

### App não carrega
**Solução:**
- Verifique os logs no Streamlit Cloud
- Teste localmente primeiro
- Verifique se todas as importações estão corretas

### Erro de memória
**Solução:**
- Otimize o carregamento de dados
- Use `st.cache_data` adequadamente
- Considere limitar o tamanho dos dados

---

## 📚 Recursos Úteis

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Sharing](https://share.streamlit.io/)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

---

**Recomendação:** Comece com Streamlit Community Cloud - é a opção mais simples e gratuita!
