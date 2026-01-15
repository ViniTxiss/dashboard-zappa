"""
Script para criar arquivo Excel de exemplo
Execute: python script_criar_exemplo.py
"""

import pandas as pd
from pathlib import Path

# Dados de exemplo (estrutura similar aos dados reais)
dados_exemplo = {
    'Motorista': [
        'Motorista Exemplo A',
        'Motorista Exemplo B',
        'Motorista Exemplo C',
        'Motorista Exemplo D',
        'Motorista Exemplo E'
    ],
    'KM': [100.5, 150.2, 120.8, 95.3, 180.7],
    'ORH': [8.5, 7.2, 9.1, 6.8, 10.2],
    'Paradas': [10, 15, 12, 8, 20],
    'SPR': [50, 75, 60, 40, 100],
    'Insucessos': [0, 1, 0, 2, 0],
    'CR': [0, 0, 0, 0, 0],
    'DS': [100.0, 98.5, 100.0, 97.0, 100.0]
}

# Cria DataFrame
df = pd.DataFrame(dados_exemplo)

# Salva como Excel
arquivo_exemplo = Path('modelo Power BI - exemplo.xlsx')
df.to_excel(arquivo_exemplo, index=False, sheet_name='performance - 2022-12-02T105208')

print(f"Arquivo de exemplo criado: {arquivo_exemplo}")
print(f"Total de linhas: {len(df)}")
print(f"Colunas: {', '.join(df.columns.tolist())}")
