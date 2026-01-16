"""
Módulo de sidebar e filtros
Implementa todos os controles de filtragem do dashboard
"""

import streamlit as st
import pandas as pd
from typing import Optional, List, Tuple
from datetime import datetime, date

from app.config.settings import COLORS


def render_sidebar(df: pd.DataFrame) -> dict:
    """
    Renderiza sidebar com filtros e retorna dicionário com valores selecionados
    """
    st.sidebar.title("🔍 Filtros")
    st.sidebar.markdown("---")
    
    filters = {}
    
    # Filtro de data
    if 'data' in df.columns:
        dates = df['data'].dropna()
        if len(dates) > 0:
            min_date = dates.min().date() if hasattr(dates.min(), 'date') else dates.min()
            max_date = dates.max().date() if hasattr(dates.max(), 'date') else dates.max()
            
            st.sidebar.subheader("📅 Período")
            
            date_range = st.sidebar.date_input(
                "Selecione o intervalo",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="date_range"
            )
            
            if isinstance(date_range, tuple) and len(date_range) == 2:
                filters['start_date'] = datetime.combine(date_range[0], datetime.min.time())
                filters['end_date'] = datetime.combine(date_range[1], datetime.max.time())
            elif isinstance(date_range, (date, datetime)):
                filters['start_date'] = datetime.combine(
                    date_range if isinstance(date_range, date) else date_range.date(),
                    datetime.min.time()
                )
                filters['end_date'] = datetime.combine(
                    date_range if isinstance(date_range, date) else date_range.date(),
                    datetime.max.time()
                )
    
    # Filtro de categoria
    category_columns = _find_category_columns(df)
    if category_columns:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📂 Categorias")
        
        for col in category_columns[:3]:  # Limita a 3 colunas de categoria
            unique_values = sorted(df[col].dropna().unique().tolist())
            if len(unique_values) > 0 and len(unique_values) <= 50:
                selected = st.sidebar.multiselect(
                    f"**{col.title()}**",
                    options=unique_values,
                    default=unique_values,
                    key=f"filter_{col}"
                )
                if selected:
                    filters[f'category_{col}'] = selected
    
    # Filtro de valores (range slider)
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        st.sidebar.markdown("---")
        st.sidebar.subheader("💰 Valores")
        
        main_value_col = numeric_columns[0]
        min_val = float(df[main_value_col].min())
        max_val = float(df[main_value_col].max())
        
        value_range = st.sidebar.slider(
            f"**{main_value_col.title()}**",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
            key="value_range"
        )
        filters['value_range'] = value_range
    
    # Botão de reset
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Resetar Filtros", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    return filters


def _find_category_columns(df: pd.DataFrame) -> List[str]:
    """
    Identifica colunas que parecem ser categorias
    """
    category_keywords = ['categoria', 'category', 'tipo', 'status', 
                        'segmento', 'grupo', 'classe', 'classificacao']
    
    category_cols = []
    
    # Procura por colunas de texto com poucos valores únicos
    for col in df.columns:
        if col == 'data':
            continue
        
        col_lower = str(col).lower()
        
        # Se contém palavra-chave de categoria
        if any(keyword in col_lower for keyword in category_keywords):
            category_cols.append(col)
        # Se é texto e tem poucos valores únicos (provavelmente categoria)
        elif df[col].dtype == 'object':
            unique_count = df[col].nunique()
            total_count = len(df[col].dropna())
            if total_count > 0 and (unique_count / total_count) < 0.3 and unique_count <= 50:
                category_cols.append(col)
    
    return category_cols


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Aplica filtros ao DataFrame
    """
    df_filtered = df.copy()
    
    # Filtro de data
    if 'start_date' in filters and 'data' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['data'] >= filters['start_date']]
    
    if 'end_date' in filters and 'data' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['data'] <= filters['end_date']]
    
    # Filtro de categoria
    for key, value in filters.items():
        if key.startswith('category_'):
            col = key.replace('category_', '')
            if col in df_filtered.columns and value:
                df_filtered = df_filtered[df_filtered[col].isin(value)]
    
    # Filtro de valores
    if 'value_range' in filters:
        numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            min_val, max_val = filters['value_range']
            df_filtered = df_filtered[
                (df_filtered[numeric_cols[0]] >= min_val) &
                (df_filtered[numeric_cols[0]] <= max_val)
            ]
    
    return df_filtered
