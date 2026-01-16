"""
Dashboard Web Interativo - Streamlit
Entry point principal da aplicação
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import logging
from pathlib import Path
import sys
from pathlib import Path

# Adiciona diretório raiz ao path para garantir que o pacote 'app' seja encontrado
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from app.config.settings import EXCEL_FILE, COLORS, CHART_HEIGHT, CHART_TEMPLATE
from app.data.loader import DataLoader
from app.services.metrics import MetricsCalculator
from app.services.processing import DataProcessor
from app.ui.layout import render_header, render_kpi_cards, render_section_title, apply_custom_css
from app.ui.sidebar import render_sidebar, apply_filters
from app.ui.charts import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_area_chart,
    create_ranking_chart,
    create_table
)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplica CSS customizado
apply_custom_css()


@st.cache_data(ttl=3600)
def load_data():
    """
    Carrega e processa dados do Excel (com cache)
    """
    loader = DataLoader()
    
    # Carrega Excel
    success, error = loader.load_excel()
    if not success:
        st.error(f"❌ Erro ao carregar dados: {error}")
        return None, None
    
    # Processa dados
    success, error = loader.process_data()
    if not success:
        st.error(f"❌ Erro ao processar dados: {error}")
        return None, None
    
    df = loader.get_data()
    summary = loader.get_summary()
    
    return df, summary


def main():
    """
    Função principal do dashboard
    """
    # Header
    render_header("Dashboard Analytics")
    
    # Carrega dados
    with st.spinner("🔄 Carregando dados..."):
        df, summary = load_data()
    
    if df is None or df.empty:
        st.error("❌ Não foi possível carregar os dados. Verifique o arquivo Excel.")
        st.info("💡 Certifique-se de que o arquivo 'modelo Power BI .xlsx' está no diretório raiz do projeto.")
        return
    
    # Sidebar com filtros
    filters = render_sidebar(df)
    
    # Aplica filtros
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        return
    
    # Inicializa calculadora de métricas
    metrics_calc = MetricsCalculator(df_filtered)
    
    # Enriquece dados com períodos
    processor = DataProcessor()
    df_enriched = processor.enrich_with_periods(df_filtered)
    
    # Identifica colunas principais
    numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
    
    # Identifica coluna de motorista
    motorista_col = None
    for col in df_filtered.columns:
        if 'motorista' in str(col).lower():
            motorista_col = col
            break
    
    # Identifica colunas específicas
    km_col = None
    spr_col = None
    paradas_col = None
    orh_col = None
    
    for col in df_filtered.columns:
        col_lower = str(col).lower()
        if col_lower == 'km':
            km_col = col
        elif col_lower == 'spr':
            spr_col = col
        elif 'parada' in col_lower:
            paradas_col = col
        elif col_lower == 'orh':
            orh_col = col
    
    # ========================================================================
    # SEÇÃO 1: KPIs PRINCIPAIS
    # ========================================================================
    st.markdown("## 📈 Indicadores Principais")
    st.markdown("")
    
    # Calcula KPIs específicos
    kpis_display = {}
    
    if km_col and km_col in df_filtered.columns:
        km_series = pd.to_numeric(df_filtered[km_col], errors='coerce')
        if km_series.notna().any():
            total_km = km_series.sum()
            media_km = km_series.mean()
            kpis_display['Total KM'] = f"{total_km:,.2f}"
            kpis_display['Média KM'] = f"{media_km:,.2f}"
    
    if spr_col and spr_col in df_filtered.columns:
        spr_series = pd.to_numeric(df_filtered[spr_col], errors='coerce')
        if spr_series.notna().any():
            total_spr = spr_series.sum()
            media_spr = spr_series.mean()
            kpis_display['Total Caixas (SPR)'] = f"{total_spr:,.0f}"
            kpis_display['Média Caixas'] = f"{media_spr:,.2f}"
    
    if paradas_col and paradas_col in df_filtered.columns:
        paradas_series = pd.to_numeric(df_filtered[paradas_col], errors='coerce')
        if paradas_series.notna().any():
            total_paradas = paradas_series.sum()
            media_paradas = paradas_series.mean()
            kpis_display['Total Paradas'] = f"{total_paradas:,.0f}"
            kpis_display['Média Paradas'] = f"{media_paradas:,.2f}"
    
    # Adiciona KPIs de ORH (formato horas)
    if orh_col and orh_col in df_filtered.columns:
        # Garante que a coluna seja numérica antes de calcular
        orh_series = pd.to_numeric(df_filtered[orh_col], errors='coerce')
        if orh_series.notna().any():
            total_orh = orh_series.sum()
            media_orh = orh_series.mean()
            # Formata em horas (HH:MM)
            def format_hours_kpi(decimal_hours):
                if pd.isna(decimal_hours):
                    return "0:00"
                hours = int(decimal_hours)
                minutes = int((decimal_hours - hours) * 60)
                return f"{hours}:{minutes:02d}"
            
            kpis_display['Total ORH'] = format_hours_kpi(total_orh)
            kpis_display['Média ORH'] = format_hours_kpi(media_orh)
    
    # Adiciona contagem de motoristas
    if motorista_col:
        num_motoristas = df_filtered[motorista_col].nunique()
        kpis_display['Motoristas'] = num_motoristas
    
    # Exibe KPIs
    if kpis_display:
        # Converte para formato esperado
        kpis_formatted = {k: {'value': v} if isinstance(v, str) else {'value': v} 
                         for k, v in kpis_display.items()}
        render_kpi_cards(kpis_formatted, columns_per_row=4)
    
    st.markdown("---")
    
    # ========================================================================
    # SEÇÃO 2: RANQUEAMENTO DOS MOTORISTAS
    # ========================================================================
    if motorista_col:
        render_section_title("🏆 Ranqueamento dos Motoristas", "🏆")
        
        # Ranqueamento por KM
        if km_col and km_col in df_filtered.columns:
            st.markdown("### 📏 Quilometragem Percorrida (KM)")
            fig_km = create_ranking_chart(
                df_filtered,
                category_column=motorista_col,
                value_column=km_col,
                title="Top Motoristas por Quilometragem",
                top_n=15,
                orientation='h'
            )
            st.plotly_chart(fig_km, width='stretch')
            st.markdown("")
        
        # Ranqueamento por SPR (Caixas)
        if spr_col and spr_col in df_filtered.columns:
            st.markdown("### 📦 Quantidade de Caixas Transportadas (SPR)")
            fig_spr = create_ranking_chart(
                df_filtered,
                category_column=motorista_col,
                value_column=spr_col,
                title="Top Motoristas por Caixas Transportadas",
                top_n=15,
                orientation='h'
            )
            st.plotly_chart(fig_spr, width='stretch')
            st.markdown("")
        
        # Ranqueamento por Paradas
        if paradas_col and paradas_col in df_filtered.columns:
            st.markdown("### 🚚 Número de Paradas (Entregas)")
            fig_paradas = create_ranking_chart(
                df_filtered,
                category_column=motorista_col,
                value_column=paradas_col,
                title="Top Motoristas por Número de Paradas",
                top_n=15,
                orientation='h'
            )
            st.plotly_chart(fig_paradas, width='stretch')
            st.markdown("")
        
        st.markdown("---")
        
        # ========================================================================
        # SEÇÃO 3: VISÃO COMPARATIVA
        # ========================================================================
        render_section_title("📊 Visão Comparativa", "📊")
        
        # Agrupa dados por motorista
        if motorista_col:
            # Cria cópia do DataFrame para garantir tipos numéricos
            df_agg = df_filtered.copy()
            agg_dict = {}
            
            if km_col and km_col in df_filtered.columns:
                if not pd.api.types.is_numeric_dtype(df_agg[km_col]):
                    df_agg[km_col] = pd.to_numeric(df_agg[km_col], errors='coerce')
                agg_dict[km_col] = 'sum'
            
            if spr_col and spr_col in df_filtered.columns:
                if not pd.api.types.is_numeric_dtype(df_agg[spr_col]):
                    df_agg[spr_col] = pd.to_numeric(df_agg[spr_col], errors='coerce')
                agg_dict[spr_col] = 'sum'
            
            if paradas_col and paradas_col in df_filtered.columns:
                if not pd.api.types.is_numeric_dtype(df_agg[paradas_col]):
                    df_agg[paradas_col] = pd.to_numeric(df_agg[paradas_col], errors='coerce')
                agg_dict[paradas_col] = 'sum'
            
            if agg_dict:
                motorista_stats = df_agg.groupby(motorista_col).agg(agg_dict).reset_index()
                
                # Renomeia colunas
                rename_dict = {motorista_col: 'Motorista'}
                if km_col in motorista_stats.columns:
                    rename_dict[km_col] = 'Total KM'
                if spr_col in motorista_stats.columns:
                    rename_dict[spr_col] = 'Total SPR'
                if paradas_col in motorista_stats.columns:
                    rename_dict[paradas_col] = 'Total Paradas'
                
                motorista_stats = motorista_stats.rename(columns=rename_dict)
                
                # Ordena por KM se disponível
                sort_col = 'Total KM' if 'Total KM' in motorista_stats.columns else motorista_stats.columns[1]
                motorista_stats = motorista_stats.sort_values(sort_col, ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de barras comparativo
                    if 'Total KM' in motorista_stats.columns and 'Total SPR' in motorista_stats.columns:
                        fig_comparativo = go.Figure()
                        
                        motorista_stats_top = motorista_stats.head(10)
                        
                        fig_comparativo.add_trace(go.Bar(
                            name='KM',
                            x=motorista_stats_top['Motorista'],
                            y=motorista_stats_top['Total KM'],
                            marker_color=COLORS['primary']
                        ))
                        
                        fig_comparativo.add_trace(go.Bar(
                            name='SPR',
                            x=motorista_stats_top['Motorista'],
                            y=motorista_stats_top['Total SPR'],
                            marker_color=COLORS['success']
                        ))
                        
                        fig_comparativo.update_layout(
                            title="Comparativo KM vs SPR (Top 10)",
                            xaxis_title="Motorista",
                            yaxis_title="Valor",
                            barmode='group',
                            height=CHART_HEIGHT,
                            template=CHART_TEMPLATE,
                            xaxis=dict(tickangle=-45),
                            margin=dict(l=20, r=20, t=60, b=100)
                        )
                        
                        st.plotly_chart(fig_comparativo, width='stretch')
                
                with col2:
                    # Tabela de resumo
                    st.markdown("#### Resumo por Motorista")
                    st.dataframe(
                        motorista_stats,
                        width='stretch',
                        height=400
                    )
        
        st.markdown("---")
     
    # ========================================================================
    # SEÇÃO 4: TABELA DE DADOS
    # ========================================================================
    render_section_title("Dados Detalhados", "📋")
    
    # Prepara tabela
    df_table = create_table(df_filtered, max_rows=100)
    
    st.dataframe(
        df_table,
        width='stretch',
        height=400
    )
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6c757d; padding: 2rem;'>
            <p>Dashboard Analytics | Desenvolvido com Streamlit e Plotly</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
