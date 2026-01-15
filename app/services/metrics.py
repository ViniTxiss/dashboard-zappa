"""
Módulo de cálculo de métricas e KPIs
Centraliza todos os cálculos de indicadores e agregações
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
import logging

from app.utils.helpers import calculate_percentage_change

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """
    Classe responsável por calcular métricas e KPIs
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa com DataFrame processado
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """
        Prepara dados para cálculos
        """
        # Identifica coluna principal de valores
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            self.value_column = numeric_cols[0]  # Usa primeira coluna numérica
        else:
            self.value_column = None
        
        # Identifica coluna de data se existir
        if 'data' in self.df.columns:
            self.date_column = 'data'
        else:
            self.date_column = None
    
    def get_total(self, column: Optional[str] = None) -> float:
        """
        Calcula total de uma coluna
        """
        col = column or self.value_column
        if col is None or col not in self.df.columns:
            return 0.0
        
        return float(self.df[col].sum() or 0)
    
    def get_average(self, column: Optional[str] = None) -> float:
        """
        Calcula média de uma coluna
        """
        col = column or self.value_column
        if col is None or col not in self.df.columns:
            return 0.0
        
        return float(self.df[col].mean() or 0)
    
    def get_median(self, column: Optional[str] = None) -> float:
        """
        Calcula mediana de uma coluna
        """
        col = column or self.value_column
        if col is None or col not in self.df.columns:
            return 0.0
        
        return float(self.df[col].median() or 0)
    
    def get_count(self) -> int:
        """
        Retorna contagem de registros
        """
        return len(self.df)
    
    def get_min(self, column: Optional[str] = None) -> float:
        """
        Retorna valor mínimo
        """
        col = column or self.value_column
        if col is None or col not in self.df.columns:
            return 0.0
        
        return float(self.df[col].min() or 0)
    
    def get_max(self, column: Optional[str] = None) -> float:
        """
        Retorna valor máximo
        """
        col = column or self.value_column
        if col is None or col not in self.df.columns:
            return 0.0
        
        return float(self.df[col].max() or 0)
    
    def get_period_comparison(self, 
                             current_start: datetime,
                             current_end: datetime,
                             previous_start: Optional[datetime] = None,
                             previous_end: Optional[datetime] = None) -> Dict:
        """
        Compara período atual com período anterior
        Retorna dicionário com métricas comparativas
        """
        if self.date_column is None or self.value_column is None:
            return {
                'current_total': 0,
                'previous_total': 0,
                'change': 0,
                'change_percent': 0
            }
        
        # Filtra período atual
        current_df = self.df[
            (self.df[self.date_column] >= current_start) &
            (self.df[self.date_column] <= current_end)
        ]
        current_total = float(current_df[self.value_column].sum() or 0)
        
        # Calcula período anterior se não fornecido
        if previous_start is None or previous_end is None:
            period_days = (current_end - current_start).days + 1
            previous_end = current_start - timedelta(days=1)
            previous_start = previous_end - timedelta(days=period_days - 1)
        
        # Filtra período anterior
        previous_df = self.df[
            (self.df[self.date_column] >= previous_start) &
            (self.df[self.date_column] <= previous_end)
        ]
        previous_total = float(previous_df[self.value_column].sum() or 0)
        
        # Calcula variação
        change = current_total - previous_total
        change_percent = calculate_percentage_change(current_total, previous_total) or 0
        
        return {
            'current_total': current_total,
            'previous_total': previous_total,
            'change': change,
            'change_percent': change_percent
        }
    
    def get_temporal_aggregation(self, 
                                 freq: str = 'D',
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Agrega dados por período temporal (dia, semana, mês)
        freq: 'D' (dia), 'W' (semana), 'M' (mês), 'Y' (ano)
        """
        if self.date_column is None or self.value_column is None:
            return pd.DataFrame()
        
        df_filtered = self.df.copy()
        
        # Aplica filtros de data se fornecidos
        if start_date:
            df_filtered = df_filtered[df_filtered[self.date_column] >= start_date]
        if end_date:
            df_filtered = df_filtered[df_filtered[self.date_column] <= end_date]
        
        if df_filtered.empty:
            return pd.DataFrame()
        
        # Agrupa por período
        df_filtered = df_filtered.set_index(self.date_column)
        aggregated = df_filtered.resample(freq)[self.value_column].agg(['sum', 'mean', 'count'])
        aggregated = aggregated.reset_index()
        aggregated.columns = ['periodo', 'total', 'media', 'contagem']
        
        return aggregated
    
    def get_category_breakdown(self, 
                               category_column: Optional[str] = None,
                               top_n: int = 10) -> pd.DataFrame:
        """
        Quebra valores por categoria
        """
        if self.value_column is None:
            return pd.DataFrame()
        
        # Tenta encontrar coluna de categoria
        if category_column is None:
            # Procura por colunas que parecem categorias
            cat_candidates = [col for col in self.df.columns 
                            if col not in [self.date_column, self.value_column] 
                            and self.df[col].dtype == 'object']
            
            if cat_candidates:
                category_column = cat_candidates[0]
            else:
                return pd.DataFrame()
        
        if category_column not in self.df.columns:
            return pd.DataFrame()
        
        # Agrupa por categoria
        breakdown = self.df.groupby(category_column)[self.value_column].agg([
            'sum', 'mean', 'count'
        ]).reset_index()
        
        breakdown.columns = ['categoria', 'total', 'media', 'contagem']
        breakdown = breakdown.sort_values('total', ascending=False)
        
        # Retorna top N
        return breakdown.head(top_n)
    
    def get_summary_kpis(self) -> Dict:
        """
        Retorna dicionário com todos os KPIs principais
        """
        return {
            'total': self.get_total(),
            'media': self.get_average(),
            'mediana': self.get_median(),
            'minimo': self.get_min(),
            'maximo': self.get_max(),
            'contagem': self.get_count()
        }
    
    def filter_data(self, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   categories: Optional[List] = None,
                   category_column: Optional[str] = None) -> 'MetricsCalculator':
        """
        Retorna nova instância com dados filtrados
        """
        df_filtered = self.df.copy()
        
        # Filtro de data
        if self.date_column and (start_date or end_date):
            if start_date:
                df_filtered = df_filtered[df_filtered[self.date_column] >= start_date]
            if end_date:
                df_filtered = df_filtered[df_filtered[self.date_column] <= end_date]
        
        # Filtro de categoria
        if category_column and categories:
            if category_column in df_filtered.columns:
                df_filtered = df_filtered[df_filtered[category_column].isin(categories)]
        
        # Retorna nova instância com dados filtrados
        new_calculator = MetricsCalculator(df_filtered)
        return new_calculator
