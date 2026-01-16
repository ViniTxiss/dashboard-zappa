"""
Módulo de criação de gráficos e visualizações
Utiliza Plotly para gráficos interativos
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime

from app.config.settings import COLORS, CHART_HEIGHT, CHART_TEMPLATE


def format_hours(decimal_hours: float) -> str:
    """
    Converte horas decimais para formato HH:MM
    Exemplo: 8.5 -> "8:30", 7.25 -> "7:15"
    """
    if pd.isna(decimal_hours):
        return ""
    
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    return f"{hours}:{minutes:02d}"


def create_line_chart(df: pd.DataFrame,
                     x_column: str,
                     y_column: str,
                     title: str = "Evolução Temporal",
                     color: Optional[str] = None) -> go.Figure:
    """
    Cria gráfico de linha temporal
    """
    fig = go.Figure()
    
    if color and color in df.columns:
        # Múltiplas linhas por categoria
        for category in df[color].unique():
            df_cat = df[df[color] == category]
            fig.add_trace(go.Scatter(
                x=df_cat[x_column],
                y=df_cat[y_column],
                mode='lines+markers',
                name=str(category),
                line=dict(width=2),
                marker=dict(size=6)
            ))
    else:
        # Linha única
        fig.add_trace(go.Scatter(
            x=df[x_column],
            y=df[y_column],
            mode='lines+markers',
            name=y_column,
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8, color=COLORS['primary'])
        ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=COLORS['text']),
            x=0.5
        ),
        xaxis_title=x_column.title(),
        yaxis_title=y_column.title(),
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    return fig


def create_bar_chart(df: pd.DataFrame,
                    x_column: str,
                    y_column: str,
                    title: str = "Comparativo",
                    orientation: str = 'v',
                    color_column: Optional[str] = None) -> go.Figure:
    """
    Cria gráfico de barras
    orientation: 'v' (vertical) ou 'h' (horizontal)
    """
    if orientation == 'h':
        x_col, y_col = y_column, x_column
    else:
        x_col, y_col = x_column, y_column
    
    if color_column and color_column in df.columns:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_column,
            title=title,
            orientation=orientation
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker_color=COLORS['primary'],
            text=df[y_col],
            textposition='auto',
            name=y_column
        ))
        fig.update_layout(title=title)
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=COLORS['text']),
            x=0.5
        ),
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        xaxis_title=x_col.title(),
        yaxis_title=y_col.title(),
        margin=dict(l=20, r=20, t=60, b=40),
        showlegend=color_column is not None
    )
    
    return fig


def create_pie_chart(df: pd.DataFrame,
                    names_column: str,
                    values_column: str,
                    title: str = "Distribuição") -> go.Figure:
    """
    Cria gráfico de pizza
    """
    fig = go.Figure(data=[go.Pie(
        labels=df[names_column],
        values=df[values_column],
        hole=0.4,  # Donut chart
        textinfo='label+percent',
        textposition='outside',
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='#FFFFFF', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>' +
                      f'{values_column}: %{{value:,.2f}}<br>' +
                      'Percentual: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=COLORS['text']),
            x=0.5
        ),
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1
        )
    )
    
    return fig


def create_area_chart(df: pd.DataFrame,
                     x_column: str,
                     y_column: str,
                     title: str = "Evolução Acumulada") -> go.Figure:
    """
    Cria gráfico de área
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_column],
        y=df[y_column],
        fill='tozeroy',
        mode='lines',
        name=y_column,
        line=dict(color=COLORS['primary'], width=2),
        fillcolor=f"rgba(31, 119, 180, 0.3)"
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=COLORS['text']),
            x=0.5
        ),
        xaxis_title=x_column.title(),
        yaxis_title=y_column.title(),
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        hovermode='x unified',
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    return fig


def create_heatmap(df: pd.DataFrame,
                  x_column: str,
                  y_column: str,
                  values_column: str,
                  title: str = "Mapa de Calor") -> go.Figure:
    """
    Cria mapa de calor
    """
    # Cria tabela dinâmica
    pivot = df.pivot_table(
        index=y_column,
        columns=x_column,
        values=values_column,
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Viridis',
        text=pivot.values,
        texttemplate='%{text:.0f}',
        textfont={"size": 10},
        hovertemplate='<b>%{y}</b> x <b>%{x}</b><br>' +
                      f'{values_column}: %{{z}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=COLORS['text']),
            x=0.5
        ),
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        xaxis_title=x_column.title(),
        yaxis_title=y_column.title(),
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    return fig


def create_ranking_chart(df: pd.DataFrame,
                        category_column: str,
                        value_column: str,
                        title: str = "Ranqueamento",
                        top_n: int = 10,
                        orientation: str = 'h') -> go.Figure:
    """
    Cria gráfico de ranqueamento (ranking) dos top N
    """
    # Garante que a coluna de valor seja numérica antes de fazer operações
    df_copy = df.copy()
    if not pd.api.types.is_numeric_dtype(df_copy[value_column]):
        df_copy[value_column] = pd.to_numeric(df_copy[value_column], errors='coerce')
    
    # Agrupa por categoria e soma valores
    ranking = df_copy.groupby(category_column)[value_column].sum().reset_index()
    ranking.columns = ['categoria', 'total']
    
    # Ordena por total (maior para menor)
    ranking = ranking.sort_values('total', ascending=(orientation == 'h'))
    
    # Top N
    ranking = ranking.head(top_n)
    
    # Cria cores gradientes (do maior para o menor)
    colors = px.colors.sequential.Blues[::-1][:len(ranking)]
    
    if orientation == 'h':
        fig = go.Figure(data=[go.Bar(
            x=ranking['total'],
            y=ranking['categoria'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='#FFFFFF', width=1)
            ),
            text=ranking['total'],
            textposition='auto',
            texttemplate='%{text:,.0f}',
            hovertemplate='<b>%{y}</b><br>' +
                         f'{value_column}: %{{x:,.2f}}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=18, color=COLORS['text']),
                x=0.5
            ),
            xaxis_title=value_column.title(),
            yaxis_title=category_column.title(),
            height=CHART_HEIGHT,
            template=CHART_TEMPLATE,
            margin=dict(l=20, r=20, t=60, b=40),
            yaxis=dict(autorange='reversed')  # Inverte para maior no topo
        )
    else:
        fig = go.Figure(data=[go.Bar(
            x=ranking['categoria'],
            y=ranking['total'],
            marker=dict(
                color=colors,
                line=dict(color='#FFFFFF', width=1)
            ),
            text=ranking['total'],
            textposition='auto',
            texttemplate='%{text:,.0f}',
            hovertemplate='<b>%{x}</b><br>' +
                         f'{value_column}: %{{y:,.2f}}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=18, color=COLORS['text']),
                x=0.5
            ),
            xaxis_title=category_column.title(),
            yaxis_title=value_column.title(),
            height=CHART_HEIGHT,
            template=CHART_TEMPLATE,
            margin=dict(l=20, r=20, t=60, b=40),
            xaxis=dict(tickangle=-45)
        )
    
    return fig


def create_table(df: pd.DataFrame,
                title: str = "Tabela de Dados",
                max_rows: int = 100) -> pd.DataFrame:
    """
    Prepara DataFrame para exibição em tabela
    """
    # Limita número de linhas
    df_display = df.head(max_rows).copy()
    
    # Formata coluna orh para horas (HH:MM)
    for col in df_display.columns:
        if 'orh' in str(col).lower():
            # Garante que a coluna seja numérica antes de formatar
            df_display[col] = pd.to_numeric(df_display[col], errors='coerce')
            df_display[col] = df_display[col].apply(format_hours)
    
    # Formata colunas numéricas
    numeric_cols = df_display.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        # Pula coluna orh se já foi formatada
        if 'orh' not in str(col).lower():
            df_display[col] = df_display[col].apply(
                lambda x: f"{x:,.2f}" if pd.notna(x) else ""
            )
    
    # Formata datas
    date_cols = df_display.select_dtypes(include=['datetime64']).columns
    for col in date_cols:
        df_display[col] = df_display[col].dt.strftime('%d/%m/%Y')
    
    return df_display
