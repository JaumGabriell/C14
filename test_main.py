import pytest
import pandas as pd
import os
import tempfile
from unittest.mock import patch, mock_open
from c14.main import (
    load_data, 
    get_last_n_rows, 
    get_first_n_rows, 
    get_dataframe_info, 
    validate_data_quality
)


class TestLoadData:
    """Testes para a função load_data"""
    
    def test_load_data_success(self):
        """Teste positivo: carregamento bem-sucedido de arquivo CSV válido"""
        # Cria um arquivo CSV temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Duration,Date,Pulse,Maxpulse,Calories\n")
            f.write("60,2020/12/01,110,130,409.1\n")
            f.write("45,2020/12/02,117,145,479.0\n")
            temp_file = f.name
        
        try:
            df = load_data(temp_file)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert list(df.columns) == ['Duration', 'Date', 'Pulse', 'Maxpulse', 'Calories']
        finally:
            os.unlink(temp_file)
    
    def test_load_data_file_not_found(self):
        """Teste negativo: arquivo não existe"""
        with pytest.raises(FileNotFoundError, match="Arquivo não encontrado"):
            load_data("arquivo_inexistente.csv")
    
    def test_load_data_empty_file(self):
        """Teste negativo: arquivo vazio"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            with pytest.raises(pd.errors.EmptyDataError):
                load_data(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_load_data_invalid_csv_format(self):
        """Teste negativo: formato CSV inválido"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("dados invalidos sem formato CSV adequado\n")
            f.write("linha sem virgulas ou estrutura\n")
            temp_file = f.name
        
        try:
            df = load_data(temp_file)
            # Pandas pode conseguir ler, mas será uma estrutura estranha
            assert isinstance(df, pd.DataFrame)
        finally:
            os.unlink(temp_file)


class TestGetLastNRows:
    """Testes para a função get_last_n_rows"""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Fixture com DataFrame de exemplo"""
        return pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e']
        })
    
    def test_get_last_n_rows_default(self, sample_dataframe):
        """Teste positivo: últimas 2 linhas (padrão)"""
        result = get_last_n_rows(sample_dataframe)
        assert len(result) == 2
        assert result.iloc[0]['A'] == 4
        assert result.iloc[1]['A'] == 5
    
    def test_get_last_n_rows_custom_n(self, sample_dataframe):
        """Teste positivo: últimas 3 linhas"""
        result = get_last_n_rows(sample_dataframe, 3)
        assert len(result) == 3
        assert result.iloc[0]['A'] == 3
        assert result.iloc[-1]['A'] == 5
    
    def test_get_last_n_rows_n_greater_than_dataframe(self, sample_dataframe):
        """Teste positivo: n maior que o tamanho do DataFrame"""
        result = get_last_n_rows(sample_dataframe, 10)
        assert len(result) == len(sample_dataframe)
        assert result.equals(sample_dataframe)
    
    def test_get_last_n_rows_empty_dataframe(self):
        """Teste positivo: DataFrame vazio"""
        empty_df = pd.DataFrame()
        result = get_last_n_rows(empty_df, 2)
        assert len(result) == 0
        assert isinstance(result, pd.DataFrame)
    
    def test_get_last_n_rows_invalid_dataframe(self):
        """Teste negativo: parâmetro não é DataFrame"""
        with pytest.raises(TypeError, match="O parâmetro df deve ser um pandas DataFrame"):
            get_last_n_rows([1, 2, 3], 2)
    
    def test_get_last_n_rows_negative_n(self, sample_dataframe):
        """Teste negativo: n negativo"""
        with pytest.raises(ValueError, match="O parâmetro n deve ser um inteiro positivo"):
            get_last_n_rows(sample_dataframe, -1)
    
    def test_get_last_n_rows_zero_n(self, sample_dataframe):
        """Teste negativo: n zero"""
        with pytest.raises(ValueError, match="O parâmetro n deve ser um inteiro positivo"):
            get_last_n_rows(sample_dataframe, 0)
    
    def test_get_last_n_rows_float_n(self, sample_dataframe):
        """Teste negativo: n não é inteiro"""
        with pytest.raises(ValueError, match="O parâmetro n deve ser um inteiro positivo"):
            get_last_n_rows(sample_dataframe, 2.5)


class TestGetFirstNRows:
    """Testes para a função get_first_n_rows"""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Fixture com DataFrame de exemplo"""
        return pd.DataFrame({
            'X': [10, 20, 30, 40, 50],
            'Y': ['x', 'y', 'z', 'w', 'v']
        })
    
    def test_get_first_n_rows_default(self, sample_dataframe):
        """Teste positivo: primeiras 5 linhas (padrão)"""
        result = get_first_n_rows(sample_dataframe)
        assert len(result) == 5
        assert result.equals(sample_dataframe)
    
    def test_get_first_n_rows_custom_n(self, sample_dataframe):
        """Teste positivo: primeiras 2 linhas"""
        result = get_first_n_rows(sample_dataframe, 2)
        assert len(result) == 2
        assert result.iloc[0]['X'] == 10
        assert result.iloc[1]['X'] == 20
    
    def test_get_first_n_rows_single_row(self, sample_dataframe):
        """Teste positivo: primeira linha apenas"""
        result = get_first_n_rows(sample_dataframe, 1)
        assert len(result) == 1
        assert result.iloc[0]['X'] == 10
    
    def test_get_first_n_rows_invalid_dataframe(self):
        """Teste negativo: parâmetro não é DataFrame"""
        with pytest.raises(TypeError, match="O parâmetro df deve ser um pandas DataFrame"):
            get_first_n_rows("not a dataframe", 5)
    
    def test_get_first_n_rows_negative_n(self, sample_dataframe):
        """Teste negativo: n negativo"""
        with pytest.raises(ValueError, match="O parâmetro n deve ser um inteiro positivo"):
            get_first_n_rows(sample_dataframe, -3)


class TestGetDataframeInfo:
    """Testes para a função get_dataframe_info"""
    
    def test_get_dataframe_info_complete_data(self):
        """Teste positivo: DataFrame com dados completos"""
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.1, 2.2, 3.3],
            'str_col': ['a', 'b', 'c']
        })
        
        info = get_dataframe_info(df)
        
        assert info['shape'] == (3, 3)
        assert info['columns'] == ['int_col', 'float_col', 'str_col']
        assert info['total_null_values'] == 0
        assert len(info['dtypes']) == 3
        assert len(info['null_count']) == 3
    
    def test_get_dataframe_info_with_nulls(self):
        """Teste positivo: DataFrame com valores nulos"""
        df = pd.DataFrame({
            'col1': [1, None, 3],
            'col2': [None, 2, None]
        })
        
        info = get_dataframe_info(df)
        
        assert info['shape'] == (3, 2)
        assert info['total_null_values'] == 3
        assert info['null_count']['col1'] == 1
        assert info['null_count']['col2'] == 2
    
    def test_get_dataframe_info_empty_dataframe(self):
        """Teste positivo: DataFrame vazio"""
        df = pd.DataFrame()
        info = get_dataframe_info(df)
        
        assert info['shape'] == (0, 0)
        assert info['columns'] == []
        assert info['total_null_values'] == 0
    
    def test_get_dataframe_info_invalid_input(self):
        """Teste negativo: entrada inválida"""
        with pytest.raises(TypeError, match="O parâmetro df deve ser um pandas DataFrame"):
            get_dataframe_info({'not': 'dataframe'})


class TestValidateDataQuality:
    """Testes para a função validate_data_quality"""
    
    def test_validate_data_quality_perfect_data(self):
        """Teste positivo: dados perfeitos sem valores nulos ou duplicatas"""
        df = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'value': ['a', 'b', 'c', 'd']
        })
        
        quality = validate_data_quality(df)
        
        assert quality['total_rows'] == 4
        assert quality['total_columns'] == 2
        assert quality['total_cells'] == 8
        assert quality['null_cells'] == 0
        assert quality['completeness_percentage'] == 100.0
        assert quality['has_duplicates'] == False
        assert quality['duplicate_count'] == 0
    
    def test_validate_data_quality_with_nulls(self):
        """Teste positivo: dados com valores nulos"""
        df = pd.DataFrame({
            'col1': [1, None, 3, 4],
            'col2': ['a', 'b', None, 'd']
        })
        
        quality = validate_data_quality(df)
        
        assert quality['total_rows'] == 4
        assert quality['total_columns'] == 2
        assert quality['total_cells'] == 8
        assert quality['null_cells'] == 2
        assert quality['completeness_percentage'] == 75.0
        assert quality['has_duplicates'] == False
    
    def test_validate_data_quality_with_duplicates(self):
        """Teste positivo: dados com duplicatas"""
        df = pd.DataFrame({
            'col1': [1, 2, 1, 3],
            'col2': ['a', 'b', 'a', 'c']
        })
        
        quality = validate_data_quality(df)
        
        assert quality['has_duplicates'] == True
        assert quality['duplicate_count'] == 1
    
    def test_validate_data_quality_empty_dataframe(self):
        """Teste positivo: DataFrame vazio"""
        df = pd.DataFrame()
        quality = validate_data_quality(df)
        
        assert quality['total_rows'] == 0
        assert quality['total_columns'] == 0
        assert quality['total_cells'] == 0
        assert quality['completeness_percentage'] == 0
    
    def test_validate_data_quality_single_row(self):
        """Teste positivo: DataFrame com uma única linha"""
        df = pd.DataFrame({'single_col': [42]})
        quality = validate_data_quality(df)
        
        assert quality['total_rows'] == 1
        assert quality['total_columns'] == 1
        assert quality['completeness_percentage'] == 100.0
    
    def test_validate_data_quality_all_nulls(self):
        """Teste negativo: DataFrame com todos os valores nulos"""
        df = pd.DataFrame({
            'col1': [None, None],
            'col2': [None, None]
        })
        
        quality = validate_data_quality(df)
        
        assert quality['completeness_percentage'] == 0.0
        assert quality['null_cells'] == 4
    
    def test_validate_data_quality_invalid_input(self):
        """Teste negativo: entrada inválida"""
        with pytest.raises(TypeError, match="O parâmetro df deve ser um pandas DataFrame"):
            validate_data_quality([1, 2, 3])


if __name__ == "__main__":
    pytest.main([__file__])
