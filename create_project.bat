@echo off
setlocal enabledelayedexpansion

:: Crear directorios principales
mkdir app
mkdir app\components
mkdir app\config
mkdir app\pages
mkdir app\services
mkdir app\utils
mkdir frontend
mkdir frontend\assets
mkdir frontend\styles
mkdir components
mkdir config
mkdir services
mkdir utils
mkdir .venv

:: Crear archivos de configuración
echo # Virtual Environment > .env
echo PYTHONPATH=${PWD}/app >> .env
echo VIRTUAL_ENV=.venv >> .env

echo [build-system] > pyproject.toml
echo requires = ["setuptools>=61.0"] >> pyproject.toml
echo build-backend = "setuptools.build_meta" >> pyproject.toml
echo. >> pyproject.toml
echo [project] >> pyproject.toml
echo name = "acma-dashboard" >> pyproject.toml
echo version = "0.1.0" >> pyproject.toml
echo authors = [ >> pyproject.toml
echo     { name = "Your Name", email = "your.email@example.com" }, >> pyproject.toml
echo ] >> pyproject.toml
echo description = "ACMA Dashboard" >> pyproject.toml
echo requires-python = ">=3.8" >> pyproject.toml

echo streamlit==1.32.0 > requirements.txt
echo plotly==5.18.0 >> requirements.txt
echo pandas==2.2.0 >> requirements.txt
echo redis==5.0.1 >> requirements.txt
echo python-dotenv==1.0.0 >> requirements.txt
echo black==24.2.0 >> requirements.txt
echo isort==5.13.2 >> requirements.txt
echo mypy==1.8.0 >> requirements.txt
echo pylint==3.0.3 >> requirements.txt
echo nbformat>=4.2.0 >> requirements.txt

echo # Virtual Environment > .gitignore
echo .venv/ >> .gitignore
echo venv/ >> .gitignore
echo env/ >> .gitignore
echo .env/ >> .gitignore
echo ENV/ >> .gitignore
echo. >> .gitignore
echo # Python >> .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo *.so >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo wheels/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore

echo # ACMA Dashboard > README.md
echo. >> README.md
echo ACMA Dashboard es una aplicación modular y escalable diseñada para gestionar solicitudes, certificados, y ofrecer un asistente virtual basado en inteligencia artificial (IA). >> README.md

:: Crear archivos __init__.py vacíos
echo. > app\components\__init__.py
echo. > app\config\__init__.py
echo. > app\pages\__init__.py
echo. > app\services\__init__.py
echo. > app\utils\__init__.py
echo. > components\__init__.py
echo. > config\__init__.py
echo. > services\__init__.py
echo. > utils\__init__.py

:: Crear archivos de código principales
echo import streamlit as st > app\run.py
echo from dotenv import load_dotenv >> app\run.py
echo from app.main import main >> app\run.py
echo. >> app\run.py
echo if __name__ == "__main__": >> app\run.py
echo     try: >> app\run.py
echo         load_dotenv() >> app\run.py
echo         st.set_page_config( >> app\run.py
echo             page_title="ACMA Dashboard", >> app\run.py
echo             page_icon="📊", >> app\run.py
echo             layout="wide" >> app\run.py
echo         ) >> app\run.py
echo         main() >> app\run.py
echo     except Exception as e: >> app\run.py
echo         st.error(f"Error iniciando la aplicación: {str(e)}") >> app\run.py

:: Crear archivo de estilos CSS
echo /* Estilos principales */ > frontend\styles\style.css
echo body { >> frontend\styles\style.css
echo     font-family: 'Arial', sans-serif; >> frontend\styles\style.css
echo     background-color: #f5f5f5; >> frontend\styles\style.css
echo     margin: 0; >> frontend\styles\style.css
echo     padding: 0; >> frontend\styles\style.css
echo } >> frontend\styles\style.css

echo Estructura del proyecto creada exitosamente!
pause
