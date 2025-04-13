# ChatBot de Legislación en Ciberseguridad

Asistente virtual especializado en la legislación sobre ciberseguridad, desarrollado con Python, Streamlit y OpenAI Assistants API.

## Descripción

Este chatbot proporciona información y orientación sobre:

- Legislación en materia de ciberseguridad
- Normativas aplicables en diferentes países
- Cumplimiento regulatorio
- Mejores prácticas legales para proteger la información y sistemas

## Requisitos

- Python 3.8 o superior
- Una cuenta de OpenAI con acceso a la API

## Instalación

1. Clona este repositorio o descarga los archivos
2. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```

3. Configura tu API key en el archivo `.env`:
   - Abre el archivo `.env`
   - Reemplaza `tu_api_key_aqui` con tu API key de OpenAI
   - El ID del asistente ya está configurado

## Uso

Para iniciar la aplicación, ejecuta:

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador web predeterminado. Puedes empezar a hacer preguntas sobre legislación en ciberseguridad directamente en la interfaz.

## Nota importante

Este chatbot utiliza un asistente de OpenAI previamente configurado con el ID: `asst_KKEuRKPBAvBKwlWxSJFTNS39`
