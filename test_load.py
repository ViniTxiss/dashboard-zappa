"""
Script de teste para validar carregamento de dados
Execute: python test_load.py
"""

import sys
from pathlib import Path

# Adiciona diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.data.loader import DataLoader
from app.config.settings import EXCEL_FILE

def test_load():
    """Testa carregamento e processamento de dados"""
    print("=" * 60)
    print("TESTE DE CARREGAMENTO DE DADOS")
    print("=" * 60)
    print(f"\nArquivo: {EXCEL_FILE}")
    print(f"Existe: {EXCEL_FILE.exists()}\n")
    
    # Cria loader
    loader = DataLoader()
    
    # Carrega Excel
    print("Carregando Excel...")
    success, error = loader.load_excel()
    
    if not success:
        print(f"ERRO: {error}")
        return False
    
    print(f"Excel carregado com sucesso!")
    print(f"   Abas encontradas: {loader.get_sheet_names()}\n")
    
    # Processa dados
    print("Processando dados...")
    success, error = loader.process_data()
    
    if not success:
        print(f"ERRO: {error}")
        return False
    
    print("Dados processados com sucesso!\n")
    
    # Obtém dados
    df = loader.get_data()
    summary = loader.get_summary()
    
    print("=" * 60)
    print("RESUMO DOS DADOS")
    print("=" * 60)
    print(f"Total de linhas: {summary.get('total_rows', 0):,}")
    print(f"Total de colunas: {summary.get('total_columns', 0)}")
    print(f"\nColunas: {', '.join(summary.get('columns', [])[:10])}")
    if len(summary.get('columns', [])) > 10:
        print(f"... e mais {len(summary.get('columns', [])) - 10} colunas")
    
    if summary.get('date_range'):
        date_range = summary['date_range']
        print(f"\nIntervalo de datas:")
        print(f"   De: {date_range['min']}")
        print(f"   Ate: {date_range['max']}")
    
    if summary.get('numeric_columns'):
        print(f"\nColunas numericas: {', '.join(summary['numeric_columns'])}")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUIDO COM SUCESSO!")
    print("=" * 60)
    print("\nVoce pode executar o dashboard com:")
    print("   streamlit run app/main.py")
    
    return True

if __name__ == "__main__":
    try:
        test_load()
    except Exception as e:
        print(f"\nERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
