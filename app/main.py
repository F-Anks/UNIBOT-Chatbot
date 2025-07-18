# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import chromadb
import ollama
from pathlib import Path

# --- Configuración ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db"
COLLECTION_NAME = "unitecnar_full_site"
EMBEDDING_MODEL = "mxbai-embed-large"

# --- MEJORA 1: Cambiamos al modelo más moderno que tienes ---
LLM_MODEL = "gemma3:latest" 

# --- MEJORA 2: Pre-filtro de saludos ---
GREETINGS = ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches", "qué tal", "que tal"]

# --- Inicialización ---
try:
    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_collection(name=COLLECTION_NAME)
    print("✅ Conexión con la base de datos vectorial establecida.")
except Exception as e:
    print(f"❌ Error al conectar con la base de datos: {e}")
    collection = None

# --- Modelos de Datos ---
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# --- Aplicación FastAPI ---
app = FastAPI(
    title="Chatbot API",
    description="API para el chatbot de la universidad con RAG",
    version="1.1.0" # Versión mejorada
)

# --- Endpoint de Chat (Lógica RAG Mejorada) ---
@app.post("/api/chat", response_model=ChatResponse)
async def handle_chat(chat_message: ChatMessage):
    user_message = chat_message.message.strip().lower() # Convertimos a minúsculas
    
    # --- Lógica del Pre-filtro de Saludos ---
    if any(saludo in user_message for saludo in GREETINGS):
        return ChatResponse(response="¡Hola! Soy el asistente virtual de Unitecnar. ¿En qué puedo ayudarte hoy?")

    if not collection:
        return ChatResponse(response="Lo siento, la base de conocimiento no está disponible en este momento.")

    # 1. Retrieve
    query_embedding = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=user_message
    )['embedding']

    # --- MEJORA 3: Reducimos el número de resultados para mayor eficiencia ---
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3 
    )
    retrieved_context = "\n\n---\n\n".join(results['documents'][0])

    # 2. Augment (con un prompt mucho más robusto)
    # --- MEJORA 4: Prompt Engineering Avanzado ---
    prompt_template = f"""
    Eres un asistente virtual experto y amigable de la Corporación Universitaria Tecnológica de Bolívar (Unitecnar).
    Tu única tarea es responder las preguntas de los usuarios basándote estricta y únicamente en el CONTEXTO que te proporciono.

    INSTRUCCIONES:
    - Responde de manera concisa y directa a la pregunta del usuario.
    - No inventes información que no esté en el contexto.
    - Si la información solicitada no se encuentra en el CONTEXTO, responde amablemente: "Lo siento, no tengo información sobre ese tema en mi base de conocimiento."
    - No menciones el "contexto" en tu respuesta. Actúa como si supieras la información de forma natural.
    - Si la pregunta es una conversación casual, responde de forma breve y amigable.

    CONTEXTO:
    {retrieved_context}

    PREGUNTA DEL USUARIO:
    {user_message}

    ASISTENTE DE UNITECNAR:
    """

    # 3. Generate
    try:
        llm_response = ollama.chat(
            model=LLM_MODEL,
            messages=[{'role': 'user', 'content': prompt_template}]
        )
        bot_response = llm_response['message']['content']
    except Exception as e:
        print(f"Error al generar respuesta con el LLM: {e}")
        bot_response = "Tuve problemas para generar una respuesta. Inténtalo de nuevo."

    return ChatResponse(response=bot_response)

# --- Montar Archivos Estáticos ---
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")