# 🚀 Instruções Rápidas

## Como Executar o Dashboard

### No Windows (PowerShell):

```powershell
# Navegue até o diretório do projeto
cd "c:\Users\vini\Desktop\dashboard zappa"

# Execute o dashboard usando:
python -m streamlit run app/main.py
```

**Nota:** No Windows, use `python -m streamlit` em vez de apenas `streamlit`.

### Alternativa (se o comando acima não funcionar):

```powershell
# Tente com o caminho completo do Python
python.exe -m streamlit run app/main.py
```

## O que Esperar

1. O Streamlit iniciará e mostrará uma mensagem como:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

2. O navegador abrirá automaticamente com o dashboard

3. Se não abrir automaticamente, copie a URL e cole no navegador

## Solução de Problemas

### Erro: "streamlit não é reconhecido"
**Solução:** Use `python -m streamlit` em vez de `streamlit`

### Erro: "Módulo não encontrado"
**Solução:** Instale as dependências:
```powershell
pip install -r requirements.txt
```

### Erro: "Arquivo não encontrado"
**Solução:** Certifique-se de estar no diretório raiz do projeto (onde está o arquivo `modelo Power BI .xlsx`)

### Dashboard não carrega dados
**Solução:** Verifique se o arquivo `modelo Power BI .xlsx` está no diretório raiz

## Parar o Dashboard

Pressione `Ctrl + C` no terminal onde o Streamlit está rodando.

## Testar Carregamento de Dados

Antes de executar o dashboard, você pode testar se os dados carregam corretamente:

```powershell
python test_load.py
```

---

**Dúvidas?** Consulte o arquivo `README.md` para documentação completa.
