import requests
import json

# La URL donde Ollama está escuchando. Por defecto es esta.
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2:7b" # El modelo que descargaste

def get_bot_response(user_message: str) -> str:
    """
    Envía un mensaje a la API de Ollama y obtiene una respuesta.
    """
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": user_message,
            "stream": False  # Queremos la respuesta completa, no en trozos
        }

        # Hacemos la solicitud POST a la API de Ollama
        response = requests.post(OLLAMA_API_URL, data=json.dumps(payload))

        # Verificamos si la solicitud fue exitosa
        response.raise_for_status()

        # Extraemos la respuesta del JSON
        response_data = response.json()
        return response_data.get("response", "No se recibió respuesta del modelo.").strip()

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con Ollama: {e}")
        return "Lo siento, no puedo conectarme con el servicio de IA en este momento."
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return "Lo siento, ocurrió un error inesperado."