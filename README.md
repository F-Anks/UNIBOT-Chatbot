# 🤖 Chatbot IA – Solución Multiplataforma WhatsApp

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-ASGI%20Framework-009688?logo=fastapi)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp_API-F22F46?logo=twilio)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Propósito**  
> Desarrollar dos chatbots basados en IA que operen mediante WhatsApp:  
> 1. **Universidad (Colombia):** Asistencia académica, envío de imágenes, canalización a un agente humano.  
> 2. **Hotel:** Recepción de mensajes y audios, gestión de reservas, visualización de habitaciones disponibles.

---

## 📑 Tabla de contenido
1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Tecnologías](#tecnologías)
4. [Características principales](#características-principales)
5. [Instalación](#instalación)
6. [Estructura del proyecto](#estructura-del-proyecto)
7. [Guía de uso rápido](#guía-de-uso-rápido)
8. [Cumplimiento legal](#cumplimiento-legal)
9. [Contribuciones](#contribuciones)
10. [Licencia](#licencia)
11. [Contacto](#contacto)

---

## Descripción del proyecto
Este repositorio alberga el código y la documentación de **dos** chatbots que comparten la misma base tecnológica. Ambos se comunican mediante **WhatsApp** gracias a la API de **Twilio**, y aprovechan modelos de lenguaje alojados localmente en **Ollama** con **Llama&nbsp;2** como motor principal.  
Cada instancia expone un conjunto de endpoints **REST** a través de **FastAPI**, permitiendo la integración con sistemas externos y la orquestación de flujos conversacionales específicos.

---

## Arquitectura
```text
┌──────────────────┐   Webhook   ┌──────────────────────┐
│      Usuario     │◀──────────▶│       Twilio         │
└──────────────────┘             └────────┬─────────────┘
                                          │
                              HTTP(S)     ▼
                                ┌──────────────────────┐
                                │     FastAPI App      │
                                │  (Uvicorn ASGI)      │
                                └────────┬─────────────┘
                                   Async │ Calls
                                          ▼
                                ┌──────────────────────┐
                                │    IA Service        │
                                │  Ollama + Llama 2    │
                                └────────┬─────────────┘
                                   I/O   │
                                          ▼
                                ┌──────────────────────┐
                                │  DB / External APIs  │
                                └──────────────────────┘
```
*Los dos chatbots comparten la misma infraestructura; difieren únicamente en la capa de lógica de negocio.*

---

## Tecnologías
| Categoría | Herramienta | Descripción breve |
|-----------|-------------|-------------------|
|🧠 IA|**Ollama**|Hosting local de modelos de lenguaje|
| |**Llama 2**|Modelo de lenguaje base|
|🐍 Backend|**Python 3.11**|Lenguaje principal|
| |**FastAPI**|Framework web REST|
| |**Uvicorn**|Servidor ASGI eficiente|
|💬 WhatsApp|**Twilio**|Envío/recepción de mensajes y audios|
|🧰 Dev Tools|**Git**|Control de versiones|
| |**VS Code**|Editor de código|
| |**python-dotenv**|Gestión de variables de entorno|
| |**loguru**|Logging estructurado|
|🌐 Scraping|**requests**|HTTP client|
| |**BeautifulSoup4**|Parseo HTML|
| |**selenium**|Automatización navegador|
|📊 Datos|**pandas**|Manipulación de datos|
| |**openpyxl**|Excel I/O|
|⚖️ Legal|**Ley 1581 de 2012**|Protección de datos personales (Colombia)|

---

## Características principales
- **Flujos conversacionales definidos** mediante intents y contexto.
- **Derivación a agente humano** cuando se requiere atención especializada.
- **Envío y recepción de multimedia** (imágenes y audios).
- **Persistencia de conversaciones** y registros operativos.
- **Despliegue simple** en entornos *bare‑metal* o *cloud*.

---

## Instalación
```bash
# 1. Clonar repositorio
git clone https://github.com/tu_usuario/chatbot-ia-whatsapp.git
cd chatbot-ia-whatsapp

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Definir variables de entorno
cp .env.example .env
# Editar .env con credenciales Twilio, claves API, etc.

# 5. Lanzar servidor
uvicorn app.main:app --reload
```

---

## Estructura del proyecto
```text
.
├── app
│   ├── api
│   │   ├── routes
│   │   └── schemas
│   ├── core
│   ├── services
│   ├── utils
│   └── main.py
├── tests
├── requirements.txt
└── README.md
```

---

## Guía de uso rápido
1. Abrir **Twilio Console** y configurar la URL del webhook a:
   ```
   https://<dominio>/webhook/twilio
   ```
2. Enviar un mensaje de WhatsApp al número de prueba.  
3. Observar la respuesta automática generada por **Llama 2**.  
4. Para escalar la conversación a un humano, enviar la palabra clave:
   ```
   ASESOR
   ```

---

## Cumplimiento legal
El tratamiento de datos personales se realiza conforme a la **Ley 1581 de 2012 (Colombia)** y su decreto reglamentario.  
Se garantiza:
- Autorización previa, expresa e informada del titular.  
- Uso limitado al fin específico de prestación del servicio.  
- Custodia y seguridad de la información mediante cifrado y control de acceso.

---

## Contribuciones
1. Crear *fork* y nueva rama: `git checkout -b feature/nueva_funcionalidad`.
2. Seguir la guía de estilo `PEP 8` y emplear *snake_case* para todas las variables.
3. Documentar las funciones y endpoints con docstrings y ejemplos.
4. Abrir *pull request* detallando cambios y pruebas realizadas.

---

## Licencia
Distribuido bajo la licencia **MIT**. Revisa el archivo `LICENSE` para más detalles.

---

## Contacto
**Autor/a:** Ana  
Correo: <tu_email_profesional@example.com>  
LinkedIn: https://linkedin.com/in/tu_perfil

---

> “La inteligencia artificial es la nueva electricidad.” – Andrew Ng