"""Script para probar diferentes endpoints de Evolution API."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('EVOLUTION_API_URL', '').rstrip('/')
API_KEY = os.getenv('EVOLUTION_API_KEY', '')
INSTANCE = os.getenv('EVOLUTION_INSTANCE_NAME', '')

HEADERS = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
}

print("=" * 70)
print("🔍 PROBANDO ENDPOINTS DE EVOLUTION API")
print("=" * 70)
print(f"\nBase URL: {BASE_URL}")
print(f"Instance: {INSTANCE}")

# Lista de endpoints posibles para obtener chats
endpoints = [
    f"/chat/findChats/{INSTANCE}",
    f"/chat/find/{INSTANCE}",
    f"/chat/fetchAllChats/{INSTANCE}",
    f"/chat/fetchChats/{INSTANCE}",
    f"/message/findMessages/{INSTANCE}",
    f"/instance/fetchInstances",
    f"/chat/findContacts/{INSTANCE}",
    f"/chat/getChats/{INSTANCE}",
]

print("\n📋 Probando endpoints...")
print("=" * 70)

for endpoint in endpoints:
    url = BASE_URL + endpoint
    print(f"\n🔗 Probando: {endpoint}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ FUNCIONA!")
            data = response.json()
            print(f"   Tipo de respuesta: {type(data)}")
            if isinstance(data, list):
                print(f"   Cantidad de items: {len(data)}")
                if len(data) > 0:
                    print(f"   Primer item keys: {list(data[0].keys())[:5]}")
            elif isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:5]}")
        elif response.status_code == 404:
            print(f"   ❌ No encontrado")
        else:
            print(f"   ⚠️  Código: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("Prueba completada")
print()
