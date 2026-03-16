"""Script para ver la estructura de los mensajes."""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('EVOLUTION_API_URL', '').rstrip('/')
API_KEY = os.getenv('EVOLUTION_API_KEY', '')
INSTANCE = os.getenv('EVOLUTION_INSTANCE_NAME', '')

HEADERS = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
}

print("🔍 DEBUG - Estructura de Mensajes")
print("=" * 70)

url = f"{BASE_URL}/chat/findMessages/{INSTANCE}"
payload = {"limit": 10}

response = requests.post(url, json=payload, headers=HEADERS, timeout=30)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    
    print(f"\n📊 Tipo de respuesta: {type(data)}")
    print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'No es dict'}")
    
    print(f"\n📄 Respuesta completa (formateada):")
    print("=" * 70)
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
    print("=" * 70)
    
    # Guardar en archivo
    with open('debug_mensajes_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Respuesta completa guardada en: debug_mensajes_response.json")
else:
    print(f"❌ Error: {response.text}")

print()
