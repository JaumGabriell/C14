# C14 - Análise de Dados com Testes Unitários

Este projeto implementa funções para análise de dados de exercícios físicos com uma suíte completa de testes unitários.

## � Funcionalidades

O projeto possui as seguintes funcionalidades principais:

- **Carregamento de dados**: Leitura de arquivos CSV com validação
- **Visualização de dados**: Exibição das primeiras e últimas linhas
- **Informações do DataFrame**: Obtenção de metadados dos dados
- **Validação de qualidade**: Análise de completude e duplicatas dos dados

## 🧪 Testes Unitários

O projeto conta com uma suíte completa de **28 testes unitários** que cobrem:

### Casos Positivos (14 testes):
- Carregamento bem-sucedido de arquivos CSV
- Obtenção correta das primeiras e últimas linhas
- Funcionamento com DataFrames vazios
- Análise de qualidade de dados perfeitos
- Processamento de dados com valores nulos
- Detecção de duplicatas

### Casos Negativos (14 testes):
- Arquivos não encontrados
- Arquivos vazios ou com formato inválido
- Parâmetros inválidos (tipos incorretos, valores negativos)
- Entrada de dados inválidos
- Validação de tipos de entrada

## 🐛 Análise de Regressões Detectadas

Durante o processo de revisão de código, foram identificadas e corrigidas as seguintes regressões introduzidas por um colega:

### ❌ Problemas Detectados:

1. **Erro na função `get_last_n_rows()`**:
   - **Problema**: Função retornava as primeiras linhas (`head()`) em vez das últimas (`tail()`)
   - **Impacto**: Resultados incorretos em todas as operações que dependiam das últimas linhas
   - **Testes que falharam**: `test_get_last_n_rows_default`, `test_get_last_n_rows_custom_n`

2. **Remoção de validação de parâmetros**:
   - **Problema**: Validações de tipo e valor foram comentadas na função `get_last_n_rows()`
   - **Impacto**: Função aceitava parâmetros inválidos sem gerar erros apropriados
   - **Testes que falharam**: `test_get_last_n_rows_negative_n`, `test_get_last_n_rows_zero_n`, `test_get_last_n_rows_float_n`

3. **Divisão por zero não tratada**:
   - **Problema**: Remoção da proteção contra divisão por zero na função `validate_data_quality()`
   - **Impacto**: Geração de valores `NaN` em vez de `0` para DataFrames vazios
   - **Testes que falharam**: `test_validate_data_quality_empty_dataframe`

4. **Remoção de validação de tipo**:
   - **Problema**: Validação de DataFrame removida na função `validate_data_quality()`
   - **Impacto**: Função tentava processar tipos incorretos, causando `AttributeError`
   - **Testes que falharam**: `test_validate_data_quality_invalid_input`

5. **Parâmetros incorretos na função main()**:
   - **Problema**: Passagem de string em vez de inteiro e `None` em vez de DataFrame
   - **Impacto**: Erros de execução no programa principal

### ✅ Correções Aplicadas:

1. **Restauração da lógica correta**: Voltou-se a usar `df.tail(n)` na função `get_last_n_rows()`
2. **Reativação das validações**: Todas as validações de parâmetros foram restauradas
3. **Proteção contra divisão por zero**: Adicionada verificação `if total_cells > 0 else 0`
4. **Validação de tipos**: Restauradas as verificações de tipo DataFrame
5. **Correção de parâmetros**: Parâmetros corretos na função main()

### 📊 Resultado dos Testes:

**Antes das correções**: 7 testes falharam, 21 passaram
**Após as correções**: 28 testes passaram (100% de sucesso)

## �📦 Instalação do Poetry

### 1. Instalar o Poetry
Abra o terminal (PowerShell no Windows) e execute:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 2. Verificar instalação
Feche e abra o terminal novamente, depois execute:

```powershell
poetry --version
```

### 3. Instalar dependências do projeto
Para instalar as dependências listadas no `pyproject.toml`:

```powershell
poetry install
```

### 4. Ativar ambiente virtual
Para ativar o ambiente virtual do Poetry:

```powershell
poetry shell
```

## 🧪 Executando os Testes

Para executar todos os testes:

```powershell
poetry run pytest test_main.py -v
```

Para executar testes com relatório de cobertura:

```powershell
poetry run pytest test_main.py --cov=c14 --cov-report=html
```

## 🏗️ Estrutura do Projeto

```
C14_juju/
├── c14/
│   ├── __init__.py
│   └── main.py          # Código principal com funções de análise
├── data.csv             # Arquivo de dados de exercícios
├── test_main.py         # Suíte completa de testes unitários
├── pyproject.toml       # Configuração do Poetry
├── poetry.lock          # Lock file das dependências
└── README.md           # Este arquivo
```

## 📈 Qualidade do Código

- **Cobertura de testes**: 100% das funções testadas
- **Casos de teste**: 28 testes cobrindo cenários positivos e negativos
- **Validação de entrada**: Todas as funções validam tipos e valores de entrada
- **Tratamento de erros**: Mensagens de erro claras e específicas
- **Documentação**: Todas as funções documentadas com docstrings

## Para resolver o conflito de merge:
Utilizamos a ferramente merge editor do vs code.

