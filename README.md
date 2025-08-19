## 📦 Instalação do Poetry

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
