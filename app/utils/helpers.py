"""
Funções auxiliares reutilizáveis
"""

import pandas as pd
import re
from typing import Optional, List, Any
from datetime import datetime


def normalize_column_name(col: str) -> str:
    """
    Normaliza nomes de colunas para formato padrão
    Remove acentos, espaços e caracteres especiais
    """
    if pd.isna(col):
        return "unnamed"
    
    # Converte para string e minúsculas
    col = str(col).lower().strip()
    
    # Remove acentos básicos
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c'
    }
    for old, new in replacements.items():
        col = col.replace(old, new)
    
    # Remove caracteres especiais e espaços
    col = re.sub(r'[^a-z0-9_]', '_', col)
    
    # Remove underscores múltiplos
    col = re.sub(r'_+', '_', col)
    
    # Remove underscores no início/fim
    col = col.strip('_')
    
    return col if col else "unnamed"


def safe_convert_date(date_value: Any, formats: List[str]) -> Optional[datetime]:
    """
    Tenta converter um valor para data usando múltiplos formatos
    """
    if pd.isna(date_value):
        return None
    
    # Se já for datetime
    if isinstance(date_value, datetime):
        return date_value
    
    # Se for Timestamp do pandas
    if isinstance(date_value, pd.Timestamp):
        return date_value.to_pydatetime()
    
    # Tenta converter string
    if isinstance(date_value, str):
        for fmt in formats:
            try:
                return datetime.strptime(date_value.strip(), fmt)
            except (ValueError, AttributeError):
                continue
    
    return None


def safe_convert_numeric(value: Any) -> Optional[float]:
    """
    Converte valor para numérico de forma segura
    """
    if pd.isna(value):
        return None
    
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # Remove caracteres não numéricos exceto ponto e vírgula
        cleaned = value.replace(',', '.').strip()
        # Remove espaços e caracteres especiais
        cleaned = re.sub(r'[^\d\.\-]', '', cleaned)
        try:
            return float(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None
    
    return None


def format_currency(value: float, currency: str = "R$") -> str:
    """
    Formata valor como moeda
    """
    if value is None or pd.isna(value):
        return f"{currency} 0,00"
    
    return f"{currency} {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Formata valor como percentual
    """
    if value is None or pd.isna(value):
        return "0,00%"
    
    return f"{value:.{decimals}f}%".replace('.', ',')


def calculate_percentage_change(current: float, previous: float) -> Optional[float]:
    """
    Calcula variação percentual entre dois valores
    """
    if previous is None or previous == 0:
        return None
    
    if current is None:
        return None
    
    return ((current - previous) / previous) * 100


def get_trend_indicator(value: float) -> str:
    """
    Retorna emoji de tendência baseado no valor
    """
    if value is None:
        return "➡️"
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    else:
        return "➡️"
