"""
Módulo de layout e estrutura visual do dashboard
Define a estrutura geral e componentes visuais
"""

import streamlit as st
from typing import Dict, Optional
from pathlib import Path
from app.config.settings import COLORS


def apply_custom_css():
    """
    Aplica CSS customizado para design moderno
    """
    st.markdown("""
    <style>
        /* Estilo geral */
        .main {
            padding: 2rem 1rem;
            background-color: #666666;
        }
        
        /* Fundo da página */
        .stApp {
            background-color: #666666;
        }
        
        /* Fundo do conteúdo principal */
        .block-container {
            background-color: #666666;
        }
        
        /* Cards de KPI */
        .metric-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #1f77b4;
            margin-bottom: 1rem;
        }
        
        .metric-card h3 {
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .metric-card .value {
            color: #212529;
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }
        
        .metric-card .change {
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        .metric-card .change.positive {
            color: #2ca02c;
        }
        
        .metric-card .change.negative {
            color: #d62728;
        }
        
        /* Título principal */
        h1 {
            color: #212529;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        /* Header com marca da empresa */
        .company-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }
        
        .company-name {
            color: #1f77b4;
            font-weight: 600;
            font-size: 1.5rem;
            margin: 0;
        }
        
        /* Sidebar */
        .css-1d391kg {
            padding-top: 3rem;
        }
        
        /* Gráficos */
        .js-plotly-plot {
            border-radius: 10px;
        }
        
        /* Botões */
        .stButton > button {
            border-radius: 8px;
            border: none;
            background-color: #1f77b4;
            color: white;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #1565a0;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Containers */
        .stContainer {
            background-color: #666666;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        /* Tabelas */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Scrollbar customizada */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str = "Dashboard Analytics", company_name: str = None, logo_path: str = None):
    """
    Renderiza cabeçalho do dashboard com marca da empresa no canto superior
    """
    from app.config.settings import COMPANY_NAME, COMPANY_LOGO_PATH, BASE_DIR
    
    # Usa configurações padrão se não fornecidas
    company = company_name or COMPANY_NAME
    logo = logo_path or COMPANY_LOGO_PATH
    
    # Converte logo para Path se for string
    if logo and isinstance(logo, str):
        # Se for caminho relativo, usa BASE_DIR
        if not Path(logo).is_absolute():
            logo = BASE_DIR / logo
        else:
            logo = Path(logo)
    elif logo and not isinstance(logo, Path):
        # Garante que seja Path
        logo = Path(logo) if logo else None
    
    # Header com marca no canto superior direito
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f" {title}")
    
    with col2:
        # Verifica se existe logo e exibe
        logo_path_str = None
        if logo and isinstance(logo, Path):
            if logo.exists():
                logo_path_str = str(logo)
        
        if logo_path_str:
            st.image(logo_path_str, width=250, use_container_width=True)
        else:
            # Se não houver logo, exibe nome da empresa estilizado
            st.markdown(f"""
            <div style="text-align: right; padding: 1rem 0;">
                <h3 style="color: {COLORS['primary']}; margin: 0; font-weight: 600;">
                    {company}
                </h3>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")


def render_kpi_cards(kpis: Dict, columns_per_row: int = 4):
    """
    Renderiza cards de KPI no topo do dashboard
    """
    apply_custom_css()
    
    # Divide KPIs em colunas
    kpi_items = list(kpis.items())
    num_cols = min(columns_per_row, len(kpi_items))
    
    cols = st.columns(num_cols)
    
    for idx, (label, value) in enumerate(kpi_items):
        col_idx = idx % num_cols
        with cols[col_idx]:
            # Formata valor
            if isinstance(value, dict):
                # KPI com variação
                main_value = value.get('value', 0)
                change = value.get('change', 0)
                change_percent = value.get('change_percent', 0)
                
                # Formata número
                if isinstance(main_value, (int, float)):
                    if abs(main_value) >= 1000000:
                        formatted_value = f"R$ {main_value/1000000:.2f}M"
                    elif abs(main_value) >= 1000:
                        formatted_value = f"R$ {main_value/1000:.2f}K"
                    else:
                        formatted_value = f"R$ {main_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                else:
                    formatted_value = str(main_value)
                
                # Determina cor da variação
                change_class = "positive" if change >= 0 else "negative"
                change_icon = "📈" if change >= 0 else "📉"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{label}</h3>
                    <p class="value">{formatted_value}</p>
                    <p class="change {change_class}">
                        {change_icon} {abs(change_percent):.2f}% 
                        ({'+' if change >= 0 else ''}{change:,.2f})
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # KPI simples
                if isinstance(value, (int, float)):
                    if abs(value) >= 1000000:
                        formatted_value = f"{value/1000000:.2f}M"
                    elif abs(value) >= 1000:
                        formatted_value = f"{value/1000:.2f}K"
                    else:
                        formatted_value = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                else:
                    formatted_value = str(value)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{label}</h3>
                    <p class="value">{formatted_value}</p>
                </div>
                """, unsafe_allow_html=True)


def render_section_title(title: str, icon: str = "📈"):
    """
    Renderiza título de seção
    """
    st.markdown(f"### {icon} {title}")
    st.markdown("")


def create_container():
    """
    Cria container para agrupar elementos
    """
    return st.container()
