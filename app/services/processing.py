"""
Módulo de processamento e regras de negócio
Contém lógica de transformação e enriquecimento de dados
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Classe responsável por processar e enriquecer dados
    """
    
    @staticmethod
    def enrich_with_periods(df: pd.DataFrame, date_column: str = 'data') -> pd.DataFrame:
        """
        Enriquece DataFrame com colunas de período (ano, mês, trimestre, etc)
        """
        if date_column not in df.columns:
            return df
        
        df_enriched = df.copy()
        
        # Extrai componentes de data
        df_enriched['ano'] = df_enriched[date_column].dt.year
        df_enriched['mes'] = df_enriched[date_column].dt.month
        df_enriched['mes_nome'] = df_enriched[date_column].dt.strftime('%B')
        df_enriched['trimestre'] = df_enriched[date_column].dt.quarter
        df_enriched['semana'] = df_enriched[date_column].dt.isocalendar().week
        df_enriched['dia_semana'] = df_enriched[date_column].dt.day_name()
        
        return df_enriched
    
    @staticmethod
    def add_calculated_columns(df: pd.DataFrame, 
                              value_column: str) -> pd.DataFrame:
        """
        Adiciona colunas calculadas úteis para análise
        """
        df_calc = df.copy()
        
        if value_column not in df_calc.columns:
            return df_calc
        
        # Calcula percentual do total
        total = df_calc[value_column].sum()
        if total > 0:
            df_calc[f'{value_column}_percentual'] = (
                df_calc[value_column] / total * 100
            )
        
        # Calcula acumulado
        df_calc = df_calc.sort_values('data') if 'data' in df_calc.columns else df_calc
        df_calc[f'{value_column}_acumulado'] = df_calc[value_column].cumsum()
        
        # Calcula média móvel (7 dias se tiver data)
        if 'data' in df_calc.columns:
            df_calc = df_calc.sort_values('data')
            df_calc[f'{value_column}_media_movel'] = (
                df_calc[value_column].rolling(window=7, min_periods=1).mean()
            )
        
        return df_calc
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, 
                       column: str,
                       method: str = 'iqr') -> pd.DataFrame:
        """
        Detecta outliers em uma coluna numérica
        method: 'iqr' (Interquartile Range) ou 'zscore'
        """
        if column not in df.columns:
            return df
        
        df_outliers = df.copy()
        
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            df_outliers['is_outlier'] = (
                (df_outliers[column] < lower_bound) |
                (df_outliers[column] > upper_bound)
            )
        
        elif method == 'zscore':
            mean = df[column].mean()
            std = df[column].std()
            if std > 0:
                df_outliers['zscore'] = abs((df_outliers[column] - mean) / std)
                df_outliers['is_outlier'] = df_outliers['zscore'] > 3
        
        return df_outliers
    
    @staticmethod
    def pivot_table(df: pd.DataFrame,
                   index: str,
                   columns: Optional[str],
                   values: str,
                   aggfunc: str = 'sum') -> pd.DataFrame:
        """
        Cria tabela dinâmica
        """
        try:
            if columns:
                pivot = pd.pivot_table(
                    df,
                    index=index,
                    columns=columns,
                    values=values,
                    aggfunc=aggfunc,
                    fill_value=0
                )
            else:
                pivot = pd.pivot_table(
                    df,
                    index=index,
                    values=values,
                    aggfunc=aggfunc
                )
            
            return pivot.reset_index()
        
        except Exception as e:
            logger.error(f"Erro ao criar pivot table: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def normalize_data(df: pd.DataFrame, 
                      columns: List[str]) -> pd.DataFrame:
        """
        Normaliza colunas numéricas (0-1)
        """
        df_norm = df.copy()
        
        for col in columns:
            if col in df_norm.columns and pd.api.types.is_numeric_dtype(df_norm[col]):
                min_val = df_norm[col].min()
                max_val = df_norm[col].max()
                if max_val > min_val:
                    df_norm[f'{col}_normalizado'] = (
                        (df_norm[col] - min_val) / (max_val - min_val)
                    )
        
        return df_norm
