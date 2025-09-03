import pandas as pd
import os


def load_data(file_path):
    """
    Carrega dados de um arquivo CSV.
    
    Args:
        file_path (str): Caminho para o arquivo CSV
        
    Returns:
        pd.DataFrame: DataFrame com os dados carregados
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        pd.errors.EmptyDataError: Se o arquivo estiver vazio
        pd.errors.ParserError: Se houver erro no parsing do CSV
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    return pd.read_csv(file_path)


def get_last_n_rows(df, n=2):
    """
    Retorna as últimas n linhas do DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame de entrada
        n (int): Número de linhas a retornar (padrão: 2)
        
    Returns:
        pd.DataFrame: DataFrame com as últimas n linhas
        
    Raises:
        ValueError: Se n for negativo ou zero
        TypeError: Se df não for um DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro df deve ser um pandas DataFrame")
    
    if not isinstance(n, int) or n <= 0:
        raise ValueError("O parâmetro n deve ser um inteiro positivo")
    
    return df.tail(n)
def get_first_n_rows(df, n=5):
    """
    Retorna as primeiras n linhas do DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame de entrada
        n (int): Número de linhas a retornar (padrão: 5)
        
    Returns:
        pd.DataFrame: DataFrame com as primeiras n linhas
        
    Raises:
        ValueError: Se n for negativo ou zero
        TypeError: Se df não for um DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro df deve ser um pandas DataFrame")
    
    if not isinstance(n, int) or n <= 0:
        raise ValueError("O parâmetro n deve ser um inteiro positivo")
    
    return df.head(n)


def get_dataframe_info(df):
    """
    Retorna informações básicas sobre o DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame de entrada
        
    Returns:
        dict: Dicionário com informações do DataFrame
        
    Raises:
        TypeError: Se df não for um DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro df deve ser um pandas DataFrame")
    
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'null_count': df.isnull().sum().to_dict(),
        'total_null_values': df.isnull().sum().sum()
    }


def validate_data_quality(df):
    """
    Valida a qualidade dos dados no DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame de entrada
        
    Returns:
        dict: Dicionário com métricas de qualidade dos dados
        
    Raises:
        TypeError: Se df não for um DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro df deve ser um pandas DataFrame")
    
    total_cells = df.shape[0] * df.shape[1]
    null_cells = df.isnull().sum().sum()
    completeness = ((total_cells - null_cells) / total_cells * 100) if total_cells > 0 else 0
    
    return {
        'total_rows': df.shape[0],
        'total_columns': df.shape[1],
        'total_cells': total_cells,
        'null_cells': null_cells,
        'completeness_percentage': round(completeness, 2),
        'has_duplicates': df.duplicated().any(),
        'duplicate_count': df.duplicated().sum()
    }


def main():
    """Função principal que executa o processamento dos dados."""
    try:
        # Carrega os dados
        db = load_data('data.csv')
        
        print("Mostra as duas últimas linhas:")
        print(get_last_n_rows(db, 2))
        
        print("\nTabela toda:")
        print(db)
        
        print("\nMostra as primeiras linhas:")
        print(get_first_n_rows(db))
        
        print("\nInformações do DataFrame:")
        info = get_dataframe_info(db)
        for key, value in info.items():
            print(f"{key}: {value}")
        
        print("\nQualidade dos dados:")
        quality = validate_data_quality(db)
        for key, value in quality.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
