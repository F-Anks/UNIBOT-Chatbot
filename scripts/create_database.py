# scripts/create_database.py

import chromadb
import ollama
import os
from pathlib import Path

# --- Configuración de Rutas Absolutas ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# --- RUTA CORREGIDA ---
# Ahora busca la carpeta 'knowledge_base' DENTRO de la carpeta 'scripts'
KNOWLEDGE_BASE_FILE = SCRIPT_DIR / "knowledge_base" / "full_site_content.txt"
DB_PATH = PROJECT_ROOT / "db"

# --- Configuración del Modelo ---
COLLECTION_NAME = "unitecnar_full_site"
EMBEDDING_MODEL = "mxbai-embed-large"

def chunk_text(text, chunk_size=1000, overlap=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def create_full_vector_database():
    print(f"📍 Buscando archivo en la ruta corregida: {KNOWLEDGE_BASE_FILE}")
    
    if not KNOWLEDGE_BASE_FILE.exists():
        print(f"❌ Error: El archivo no se encuentra en la ruta especificada.")
        return

    client = chromadb.PersistentClient(path=str(DB_PATH))
    
    try:
        if COLLECTION_NAME in [c.name for c in client.list_collections()]:
            client.delete_collection(name=COLLECTION_NAME)
            print(f"Colección antigua '{COLLECTION_NAME}' eliminada.")
    except Exception as e:
        print(f"No se pudo eliminar la colección antigua: {e}")

    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"Colección '{COLLECTION_NAME}' creada.")

    with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
        full_text = f.read()

    text_chunks = chunk_text(full_text)
    if not text_chunks:
        print("No se pudieron generar chunks del archivo de conocimiento.")
        return
        
    print(f"Texto dividido en {len(text_chunks)} chunks. Iniciando proceso de embedding...")

    for i, doc in enumerate(text_chunks):
        try:
            embedding = ollama.embeddings(model=EMBEDDING_MODEL, prompt=doc)['embedding']
            collection.add(ids=[f"chunk_{i}"], embeddings=[embedding], documents=[doc])
            print(f" -> Procesando chunk {i+1}/{len(text_chunks)}")
        except Exception as e:
            print(f"Error procesando chunk {i+1}: {e}")

    print(f"\n✅ ¡Base de datos vectorial completada!")
    print(f"Total de documentos: {collection.count()}")

if __name__ == "__main__":
    print("Asegúrate de que Ollama esté corriendo.")
    create_full_vector_database()