import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "hf.co/SpeakLeash/Bielik-11B-v2.6-Instruct-GGUF:Q4_K_M"  # dopasuj nazwę modelu lokalnego, np. bielik, mistral itp.

def query_local_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Wysyła zapytanie do lokalnego modelu LLM przez Ollama REST API.
    Zwraca pełną odpowiedź jako tekst.
    """
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
    except Exception as e:
        return f"Błąd połączenia z lokalnym modelem: {e}"
