"""
Configurações globais do dashboard
Centraliza todas as constantes e configurações da aplicação
"""

import os
from pathlib import Path

# ============================================================================
# PATHS E ARQUIVOS
# ============================================================================

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent.parent

# Caminho do arquivo Excel de entrada
# Tenta primeiro o arquivo real, depois o exemplo
EXCEL_FILE = BASE_DIR / "modelo Power BI .xlsx"
EXCEL_FILE_EXEMPLO = BASE_DIR / "modelo Power BI - exemplo.xlsx"

# Usa exemplo se o arquivo real não existir (útil para deploy)
if not EXCEL_FILE.exists() and EXCEL_FILE_EXEMPLO.exists():
    EXCEL_FILE = EXCEL_FILE_EXEMPLO

# ============================================================================
# CONFIGURAÇÕES DE DADOS
# ============================================================================

# Nomes padrão de colunas esperadas (serão normalizados)
DATE_COLUMNS = ['data', 'date', 'dt', 'periodo', 'período', 'mes', 'ano']
VALUE_COLUMNS = ['valor', 'value', 'total', 'montante', 'receita', 'despesa']
CATEGORY_COLUMNS = ['categoria', 'category', 'tipo', 'status', 'segmento']

# Formato de data esperado
DATE_FORMAT = '%Y-%m-%d'
DATE_FORMATS = [
    '%Y-%m-%d',
    '%d/%m/%Y',
    '%m/%d/%Y',
    '%Y-%m-%d %H:%M:%S',
    '%d-%m-%Y'
]

# ============================================================================
# CONFIGURAÇÕES DE UI
# ============================================================================

# Tema e cores
PRIMARY_COLOR = "#1f77b4"
SUCCESS_COLOR = "#2ca02c"
WARNING_COLOR = "#ff7f0e"
DANGER_COLOR = "#d62728"
INFO_COLOR = "#17a2b8"

# Cores do tema
COLORS = {
    'primary': PRIMARY_COLOR,
    'success': SUCCESS_COLOR,
    'warning': WARNING_COLOR,
    'danger': DANGER_COLOR,
    'info': INFO_COLOR,
    'background': '#f8f9fa',
    'card': '#ffffff',
    'text': '#212529',
    'border': '#dee2e6'
}

# Configurações de gráficos
CHART_HEIGHT = 400
CHART_TEMPLATE = "plotly_white"

# ============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO
# ============================================================================

# Valores mínimos/máximos para validação
MIN_DATE = "2000-01-01"
MAX_DATE = "2100-12-31"

# Tamanho máximo de arquivo (em MB)
MAX_FILE_SIZE_MB = 50

# ============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================================

# Cache TTL (em segundos)
CACHE_TTL = 3600  # 1 hora

# ============================================================================
# CONFIGURAÇÕES DE LOGGING
# ============================================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
