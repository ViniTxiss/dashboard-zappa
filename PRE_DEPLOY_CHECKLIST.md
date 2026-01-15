# ✅ Checklist Pré-Deploy

Use este checklist antes de fazer deploy do dashboard.

## 📋 Preparação do Código

- [x] Código testado localmente
- [x] `requirements.txt` atualizado com todas as dependências
- [x] `.gitignore` configurado para excluir dados sensíveis
- [x] Arquivo de exemplo criado (`modelo Power BI - exemplo.xlsx`)
- [x] Configurações do Streamlit (`.streamlit/config.toml`) criadas

## 📁 Arquivos Criados para Deploy

- [x] `DEPLOY.md` - Guia completo de deploy
- [x] `GUIA_DEPLOY_RAPIDO.md` - Guia rápido passo a passo
- [x] `script_criar_exemplo.py` - Script para criar dados de exemplo
- [x] `.streamlit/config.toml` - Configurações do Streamlit
- [x] `packages.txt` - Pacotes do sistema (se necessário)

## 🔒 Segurança

- [ ] Arquivo Excel com dados reais **NÃO** está no repositório
- [ ] `.gitignore` configurado para excluir `*.xlsx` (exceto exemplo)
- [ ] Nenhuma credencial ou API key no código
- [ ] Dados de exemplo são genéricos (sem informações reais)

## 🚀 Pronto para Deploy

- [ ] Repositório GitHub criado
- [ ] Código commitado e enviado para GitHub
- [ ] Conta Streamlit Cloud criada
- [ ] Pronto para seguir o `GUIA_DEPLOY_RAPIDO.md`

## 📝 Comandos Finais

```powershell
# 1. Verificar status do Git
git status

# 2. Verificar se arquivo Excel real está sendo ignorado
git check-ignore "modelo Power BI .xlsx"
# Deve retornar o caminho do arquivo (está sendo ignorado)

# 3. Verificar se arquivo de exemplo será incluído
git ls-files | findstr "exemplo"
# Deve mostrar: modelo Power BI - exemplo.xlsx

# 4. Fazer commit final
git add .
git commit -m "Preparado para deploy - Streamlit Cloud"

# 5. Enviar para GitHub
git push origin main
```

---

**Quando todos os itens estiverem marcados, siga o `GUIA_DEPLOY_RAPIDO.md`!**
