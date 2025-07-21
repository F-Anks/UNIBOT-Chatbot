# UNIBOT.

Bienvenido a UNIBOT, un asistente conversacional inteligente diseñado para la Universitaria Tecnológica de Bolívar (UNITECNAR). Este proyecto utiliza un modelo de lenguaje local y una arquitectura de Generación Aumentada por Recuperación (RAG) para responder preguntas basadas en el contenido extraído del sitio web oficial de la universidad.

## Características Principales

* **Inteligencia Local:** Todo el procesamiento de IA se realiza localmente utilizando **Ollama**, garantizando la privacidad de los datos y sin depender de APIs de terceros.
* **Generación Aumentada por Recuperación (RAG):** El chatbot no inventa respuestas. Utiliza información extraída del sitio web de Unitecnar, almacenada en una base de datos vectorial, para formular respuestas precisas y contextualizadas.
* **Extracción de Datos Automatizada:** Incluye un crawler avanzado basado en **Selenium** y **BeautifulSoup** capaz de navegar por el sitio web y extraer su contenido textual de forma automática.
* **Interfaz de Prueba:** Una interfaz web sencilla con estilo de WhatsApp para probar e interactuar con el chatbot en un entorno local.
* **Backend Moderno:** Construido con **FastAPI**, asegurando un alto rendimiento y una API robusta.

## Tecnologías
| Categoría | Herramienta | Descripción breve |
|:---:|:---|:---|
| 🧠 **IA y Modelos** | **Ollama** | Plataforma para ejecutar modelos de lenguaje grandes (LLMs) de forma local. |
| | **Llama 2 (7B)** | Modelo de lenguaje principal para generar las respuestas del chatbot. |
| | **mxbai-embed-large** | Modelo de embeddings para vectorizar el texto y permitir búsquedas semánticas. |
| 🐍 **Backend** | **Python 3.11** | Lenguaje de programación principal del proyecto. |
| | **FastAPI** | Framework web asíncrono para construir la API del chatbot. |
| | **Uvicorn** | Servidor ASGI para ejecutar la aplicación FastAPI. |
| 🗃️ **Base de Datos** | **ChromaDB** | Base de datos vectorial para almacenar y consultar los embeddings del conocimiento. |
| 🌐 **Scraping Web** | **Selenium** | Herramienta para automatizar y controlar un navegador web real. |
| | **Selenium-Stealth** | Plugin para Selenium que evade sistemas avanzados de detección de bots. |
| | **BeautifulSoup4** | Librería para parsear HTML y extraer contenido de las páginas web. |
| 💬 **Integración** | **Twilio** | API para la futura integración del chatbot con WhatsApp. |
| 🧰 **Herramientas**| **Git** | Sistema de control de versiones para gestionar el código fuente. |
| | **VS Code** | Editor de código principal para el desarrollo. |
| | **python-dotenv** | Librería para gestionar variables de entorno y secretos. |
| ⚖️ **Marco Legal** | **Ley 1581 de 2012** | Normativa colombiana de protección de datos a considerar en el manejo de información. |

---

## 🚀 Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local después de clonar el repositorio.

### Prerrequisitos

Asegúrate de tener instalado lo siguiente:

* **Python 3.11** o superior.
* **Git**.
* **Google Chrome** (para que Selenium funcione correctamente).
* **Ollama:** Descárgalo e instálalo desde [ollama.com](https://ollama.com).

### 🔧 Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/F-Anks/UNIBOT-Chatbot.git
    cd UNIBOT-Chatbot
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    # source venv/bin/activate
    ```

3.  **Instala las dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Descarga los modelos de Ollama:**
    Abre una nueva terminal y ejecuta estos comandos. Ollama debe estar corriendo en segundo plano.
    ```bash
    # Descargar el modelo de chat (4.7 GB)
    ollama pull llama3:8b-instruct

    # Descargar el modelo para la base de datos (400 MB)
    ollama pull mxbai-embed-large
    ```

### 🧠 Creación de la Base de Conocimiento

Este paso utiliza el crawler para extraer la información de la web y la guarda en la base de datos vectorial.

1.  **Ejecuta el script de scraping:**
    Este proceso tardará varios minutos, ya que navegará por todo el sitio web.
    ```bash
    python scripts/scrape_unitecnar.py
    ```

2.  **Ejecuta el script de creación de la base de datos:**
    Este proceso también tardará varios minutos mientras procesa todo el texto extraído.
    ```bash
    python scripts/create_database.py
    ```

### ▶️ Ejecución del Chatbot

Una vez que la base de datos ha sido creada, puedes iniciar el chatbot.

1.  **Inicia el servidor de FastAPI:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0
    ```

2.  **Abre la interfaz de chat:**
    Abre tu navegador y ve a `http://127.0.0.1:8000`. ¡Ya puedes chatear con tu bot!

## 📁 Estructura del Proyecto
```text
UNIBOT-Chatbot/
├── app/                  # Contiene la aplicación principal de FastAPI
│   ├── static/           # Archivos de la interfaz web (HTML, CSS, JS)
│   └── main.py           # Lógica de la API y del RAG en tiempo real
│
├── scripts/              # Scripts de un solo uso
│   ├── scrape_unitecnar.py # El crawler que extrae el contenido de la web
│   └── create_database.py  # Procesa el contenido y crea la base de datos
│
├── knowledge_base/       # Carpeta donde se guarda el texto extraído
│
├── db/                   # Carpeta donde ChromaDB almacena la base de datos vectorial
│
└── requirements.txt      # Lista de dependencias de Python
```
