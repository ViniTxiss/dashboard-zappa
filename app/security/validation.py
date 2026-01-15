"""
Módulo de segurança e validação de dados
Protege contra dados inválidos, corrompidos e ataques
"""

import pandas as pd
import os
from pathlib import Path
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)


def validate_file_path(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Valida se o arquivo existe e é acessível
    Retorna: (is_valid, error_message)
    """
    try:
        if not file_path.exists():
            return False, f"Arquivo não encontrado: {file_path}"
        
        if not file_path.is_file():
            return False, f"Caminho não é um arquivo: {file_path}"
        
        # Verifica tamanho do arquivo
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > 50:  # 50MB máximo
            return False, f"Arquivo muito grande: {file_size_mb:.2f}MB (máximo: 50MB)"
        
        return True, None
    
    except Exception as e:
        logger.error(f"Erro ao validar arquivo: {e}")
        return False, f"Erro ao validar arquivo: {str(e)}"


def validate_dataframe(df: pd.DataFrame, min_rows: int = 1) -> Tuple[bool, Optional[str]]:
    """
    Valida estrutura básica do DataFrame
    Retorna: (is_valid, error_message)
    """
    try:
        if df is None:
            return False, "DataFrame é None"
        
        if not isinstance(df, pd.DataFrame):
            return False, "Objeto não é um DataFrame"
        
        if df.empty:
            return False, "DataFrame está vazio"
        
        if len(df) < min_rows:
            return False, f"DataFrame tem menos de {min_rows} linha(s)"
        
        if df.columns.empty:
            return False, "DataFrame não tem colunas"
        
        return True, None
    
    except Exception as e:
        logger.error(f"Erro ao validar DataFrame: {e}")
        return False, f"Erro ao validar DataFrame: {str(e)}"


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove ou trata dados potencialmente perigosos
    """
    try:
        df_clean = df.copy()
        
        # Remove linhas completamente vazias
        df_clean = df_clean.dropna(how='all')
        
        # Limita tamanho de strings para prevenir DoS
        for col in df_clean.select_dtypes(include=['object']).columns:
            df_clean[col] = df_clean[col].astype(str).str[:1000]
        
        return df_clean
    
    except Exception as e:
        logger.error(f"Erro ao sanitizar DataFrame: {e}")
        return df


def validate_date_range(start_date, end_date) -> Tuple[bool, Optional[str]]:
    """
    Valida intervalo de datas
    """
    try:
        if start_date is None or end_date is None:
            return True, None  # Datas opcionais
        
        if start_date > end_date:
            return False, "Data inicial não pode ser maior que data final"
        
        return True, None
    
    except Exception as e:
        logger.error(f"Erro ao validar intervalo de datas: {e}")
        return False, f"Erro ao validar datas: {str(e)}"


def validate_numeric_column(df: pd.DataFrame, column: str) -> Tuple[bool, Optional[str]]:
    """
    Valida se coluna existe e contém valores numéricos
    """
    try:
        if column not in df.columns:
            return False, f"Coluna '{column}' não encontrada"
        
        # Tenta converter para numérico
        numeric_values = pd.to_numeric(df[column], errors='coerce')
        valid_count = numeric_values.notna().sum()
        
        if valid_count == 0:
            return False, f"Coluna '{column}' não contém valores numéricos válidos"
        
        return True, None
    
    except Exception as e:
        logger.error(f"Erro ao validar coluna numérica: {e}")
        return False, f"Erro ao validar coluna: {str(e)}"
