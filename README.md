# 📊 Dashboard Analytics - Streamlit

Dashboard web interativo e moderno desenvolvido em Python utilizando Streamlit, projetado para visualização e análise de dados financeiros/operacionais a partir de planilhas Excel.

## 🚀 Características

- **Arquitetura Modular**: Código organizado em módulos separados por responsabilidade
- **Design Moderno**: Interface inspirada em Power BI e Tableau
- **Interatividade**: Gráficos Plotly com zoom, hover e filtros dinâmicos
- **Segurança**: Validação e sanitização de dados
- **Performance**: Cache inteligente para otimização
- **Responsivo**: Layout adaptável e profissional

## 📁 Estrutura do Projeto

```
dashboard zappa/
├── app/
│   ├── main.py              # Entry point Streamlit
│   ├── config/
│   │   └── settings.py      # Configurações globais
│   ├── data/
│   │   └── loader.py        # Leitura e validação do Excel
│   ├── services/
│   │   ├── processing.py    # Regras de negócio
│   │   └── metrics.py        # KPIs e agregações
│   ├── ui/
│   │   ├── layout.py        # Layout geral
│   │   ├── sidebar.py       # Filtros e controles
│   │   └── charts.py         # Gráficos e visualizações
│   ├── security/
│   │   └── validation.py     # Sanitização e validação
│   └── utils/
│       └── helpers.py        # Funções auxiliares
├── modelo Power BI .xlsx     # Arquivo de dados
└── requirements.txt          # Dependências
```

## 🛠️ Instalação

1. **Clone ou baixe o projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Certifique-se de que o arquivo Excel está no diretório raiz:**
   - O arquivo deve se chamar `modelo Power BI .xlsx`
   - Ou ajuste o caminho em `app/config/settings.py`

## 🚀 Executando o Dashboard

```bash
streamlit run app/main.py
```

O dashboard será aberto automaticamente no navegador em `http://localhost:8501`

## 📊 Funcionalidades

### KPIs Principais
- Total geral
- Médias e medianas
- Percentuais de crescimento
- Indicadores visuais (📈/📉)

### Filtros Interativos
- **Período**: Seletor de intervalo de datas
- **Categorias**: Filtro múltiplo por categorias
- **Valores**: Range slider para valores numéricos
- **Reset**: Botão para limpar todos os filtros

### Visualizações
- **Gráfico de Linha**: Evolução temporal
- **Gráfico de Área**: Evolução acumulada
- **Gráfico de Barras**: Comparativos por categoria
- **Gráfico de Pizza/Donut**: Distribuição percentual
- **Tabela Interativa**: Dados detalhados com formatação

## 🔧 Configuração

### Ajustar Caminho do Excel

Edite `app/config/settings.py`:

```python
EXCEL_FILE = BASE_DIR / "caminho/para/seu/arquivo.xlsx"
```

### Personalizar Cores

Edite `app/config/settings.py`:

```python
PRIMARY_COLOR = "#1f77b4"
SUCCESS_COLOR = "#2ca02c"
# ... outras cores
```

## 📝 Estrutura de Dados Esperada

O dashboard detecta automaticamente:
- **Colunas de Data**: Procura por colunas com nomes como "data", "date", "periodo", etc.
- **Colunas Numéricas**: Identifica colunas de valores (valor, total, receita, etc.)
- **Colunas de Categoria**: Detecta colunas textuais com poucos valores únicos

### Formato Recomendado

| Data | Categoria | Valor | Status |
|------|-----------|-------|--------|
| 2024-01-01 | A | 1000 | Ativo |
| 2024-01-02 | B | 2000 | Ativo |

## 🎨 Personalização

### Adicionar Novos Gráficos

Edite `app/ui/charts.py` e adicione novas funções de gráfico.

### Adicionar Novas Métricas

Edite `app/services/metrics.py` e adicione novos métodos de cálculo.

### Modificar Layout

Edite `app/ui/layout.py` para ajustar a estrutura visual.

## 🔒 Segurança

- Validação de tipos de dados
- Sanitização de entradas
- Proteção contra arquivos corrompidos
- Limitação de tamanho de arquivo (50MB)
- Tratamento robusto de erros

## 📈 Performance

- Cache de dados com `st.cache_data` (TTL: 1 hora)
- Processamento otimizado de DataFrames
- Lazy loading de visualizações

## 🐛 Troubleshooting

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo Excel está no diretório correto
- Confirme o nome do arquivo em `app/config/settings.py`

### Erro: "Nenhum dado encontrado"
- Verifique se o Excel contém dados válidos
- Confirme que há pelo menos uma coluna numérica

### Dashboard não carrega
- Verifique se todas as dependências estão instaladas: `pip install -r requirements.txt`
- Verifique os logs no terminal para mensagens de erro

## 📄 Licença

Este projeto foi desenvolvido para uso interno/empresarial.

## 👨‍💻 Desenvolvimento

### Arquitetura

O projeto segue princípios de:
- **Separação de Responsabilidades**: Cada módulo tem uma função específica
- **Reutilização**: Funções auxiliares centralizadas
- **Manutenibilidade**: Código limpo e comentado
- **Escalabilidade**: Fácil adicionar novas funcionalidades

### Boas Práticas Implementadas

- Type hints em funções
- Docstrings em classes e métodos
- Tratamento de erros robusto
- Logging para debugging
- Validação de dados em múltiplas camadas

---

**Desenvolvido com ❤️ usando Streamlit e Plotly**
