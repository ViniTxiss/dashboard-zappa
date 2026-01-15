"""
Módulo de carregamento e validação de dados do Excel
Responsável por ler, limpar e padronizar os dados da planilha
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import warnings

from app.config.settings import EXCEL_FILE, DATE_FORMATS
from app.utils.helpers import normalize_column_name, safe_convert_date, safe_convert_numeric
from app.security.validation import (
    validate_file_path, 
    validate_dataframe, 
    sanitize_dataframe
)

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Classe responsável por carregar e processar dados do Excel
    """
    
    def __init__(self, excel_path: Optional[Path] = None):
        """
        Inicializa o loader com o caminho do arquivo Excel
        """
        self.excel_path = excel_path or EXCEL_FILE
        self.raw_data: Dict[str, pd.DataFrame] = {}
        self.processed_data: Optional[pd.DataFrame] = None
        
    def load_excel(self) -> Tuple[bool, Optional[str]]:
        """
        Carrega o arquivo Excel e valida
        Retorna: (success, error_message)
        """
        try:
            # Valida arquivo
            is_valid, error = validate_file_path(self.excel_path)
            if not is_valid:
                return False, error
            
            # Lê todas as abas do Excel
            excel_file = pd.ExcelFile(self.excel_path)
            sheet_names = excel_file.sheet_names
            
            if not sheet_names:
                return False, "Arquivo Excel não contém abas"
            
            logger.info(f"Carregando {len(sheet_names)} aba(s) do Excel")
            
            # Carrega cada aba
            for sheet in sheet_names:
                try:
                    df = pd.read_excel(excel_file, sheet_name=sheet)
                    if not df.empty:
                        self.raw_data[sheet] = df
                        logger.info(f"Aba '{sheet}': {len(df)} linhas, {len(df.columns)} colunas")
                except Exception as e:
                    logger.warning(f"Erro ao ler aba '{sheet}': {e}")
                    continue
            
            if not self.raw_data:
                return False, "Nenhuma aba válida encontrada no Excel"
            
            return True, None
            
        except Exception as e:
            error_msg = f"Erro ao carregar Excel: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def process_data(self, sheet_name: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Processa e padroniza os dados de uma aba específica ou da primeira disponível
        Retorna: (success, error_message)
        """
        try:
            if not self.raw_data:
                return False, "Nenhum dado carregado. Execute load_excel() primeiro."
            
            # Seleciona a aba
            if sheet_name and sheet_name in self.raw_data:
                df = self.raw_data[sheet_name].copy()
            else:
                # Usa a primeira aba disponível
                df = list(self.raw_data.values())[0].copy()
            
            # Valida DataFrame
            is_valid, error = validate_dataframe(df)
            if not is_valid:
                return False, error
            
            # Sanitiza dados
            df = sanitize_dataframe(df)
            
            # Normaliza nomes de colunas
            df.columns = [normalize_column_name(col) for col in df.columns]
            
            # Identifica e processa colunas de data
            date_col = self._find_date_column(df)
            if date_col:
                df[date_col] = df[date_col].apply(
                    lambda x: safe_convert_date(x, DATE_FORMATS)
                )
                df = df.rename(columns={date_col: 'data'})
            
            # Identifica e processa colunas numéricas
            numeric_cols = self._find_numeric_columns(df)
            for col in numeric_cols:
                df[col] = df[col].apply(safe_convert_numeric)
            
            # Remove linhas onde todas as colunas numéricas são nulas
            if numeric_cols:
                df = df.dropna(subset=numeric_cols, how='all')
            
            # Remove coluna 'rota' se existir
            if 'rota' in df.columns:
                df = df.drop(columns=['rota'])
                logger.info("Coluna 'rota' removida")
            
            # Remove duplicatas
            df = df.drop_duplicates()
            
            # Reseta índice
            df = df.reset_index(drop=True)
            
            # Valida novamente após processamento
            is_valid, error = validate_dataframe(df)
            if not is_valid:
                return False, f"Erro após processamento: {error}"
            
            self.processed_data = df
            logger.info(f"Dados processados: {len(df)} linhas, {len(df.columns)} colunas")
            
            return True, None
            
        except Exception as e:
            error_msg = f"Erro ao processar dados: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _find_date_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Identifica a coluna de data no DataFrame
        """
        # Procura por nomes comuns de data
        date_keywords = ['data', 'date', 'dt', 'periodo', 'mes', 'ano']
        
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in date_keywords):
                # Tenta converter algumas amostras para confirmar
                sample = df[col].dropna().head(10)
                if len(sample) > 0:
                    converted = sum(1 for val in sample 
                                  if safe_convert_date(val, DATE_FORMATS) is not None)
                    if converted >= len(sample) * 0.5:  # 50% de sucesso
                        return col
        
        return None
    
    def _find_numeric_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Identifica colunas numéricas no DataFrame
        """
        numeric_cols = []
        
        # Palavras-chave comuns para valores
        value_keywords = ['valor', 'value', 'total', 'montante', 'receita', 
                         'despesa', 'custo', 'preco', 'preço', 'quantidade']
        
        for col in df.columns:
            col_lower = str(col).lower()
            
            # Se já é numérico
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)
                continue
            
            # Se contém palavras-chave de valor
            if any(keyword in col_lower for keyword in value_keywords):
                # Tenta converter amostra
                sample = df[col].dropna().head(20)
                if len(sample) > 0:
                    converted = sum(1 for val in sample 
                                  if safe_convert_numeric(val) is not None)
                    if converted >= len(sample) * 0.7:  # 70% de sucesso
                        numeric_cols.append(col)
        
        return numeric_cols
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Retorna os dados processados
        """
        return self.processed_data
    
    def get_sheet_names(self) -> List[str]:
        """
        Retorna lista de nomes das abas disponíveis
        """
        return list(self.raw_data.keys())
    
    def get_summary(self) -> Dict:
        """
        Retorna resumo dos dados carregados
        """
        if self.processed_data is None:
            return {}
        
        df = self.processed_data
        
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'date_range': None,
            'numeric_columns': []
        }
        
        # Encontra intervalo de datas
        if 'data' in df.columns:
            dates = df['data'].dropna()
            if len(dates) > 0:
                summary['date_range'] = {
                    'min': dates.min(),
                    'max': dates.max()
                }
        
        # Identifica colunas numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        summary['numeric_columns'] = numeric_cols
        
        return summary
