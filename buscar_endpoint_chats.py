"""Script para encontrar el endpoint correcto de chats en Evolution API."""
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
print("🔍 BUSCANDO ENDPOINT CORRECTO PARA CHATS")
print("=" * 70)

# Lista extendida de posibles endpoints
endpoints_get = [
    # Chats
    f"/chat/findChats/{INSTANCE}",
    f"/chat/find/{INSTANCE}",
    f"/chat/fetchAllChats/{INSTANCE}",
    f"/chat/fetchChats/{INSTANCE}",
    f"/chat/getChats/{INSTANCE}",
    f"/chat/list/{INSTANCE}",
    f"/chat/all/{INSTANCE}",
    
    # Contactos
    f"/chat/findContacts/{INSTANCE}",
    f"/chat/fetchAllContacts/{INSTANCE}",
    f"/chat/fetchContacts/{INSTANCE}",
    f"/chat/getContacts/{INSTANCE}",
    f"/contact/findAll/{INSTANCE}",
    f"/contact/fetchAll/{INSTANCE}",
    
    # Mensajes
    f"/message/findMessages/{INSTANCE}",
    f"/message/find/{INSTANCE}",
    f"/message/list/{INSTANCE}",
    
    # Instance
    f"/instance/fetchInstances",
    f"/instance/connectionState/{INSTANCE}",
    f"/instance/connect/{INSTANCE}",
]

# Endpoints POST
endpoints_post = [
    (f"/chat/findMessages/{INSTANCE}", {"limit": 50}),
    (f"/message/find/{INSTANCE}", {"limit": 50}),
]

print("\n📋 Probando endpoints GET...")
print("=" * 70)

for endpoint in endpoints_get:
    url = BASE_URL + endpoint
    print(f"\n🔗 GET {endpoint}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ FUNCIONA! Status: {response.status_code}")
            data = response.json()
            print(f"   Tipo: {type(data)}")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"   Items: {len(data)}")
                print(f"   Primer item: {list(data[0].keys())[:10] if isinstance(data[0], dict) else data[0]}")
            elif isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:10]}")
                
        elif response.status_code == 404:
            print(f"   ❌ 404 - No encontrado")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

print("\n\n📋 Probando endpoints POST...")
print("=" * 70)

for endpoint, payload in endpoints_post:
    url = BASE_URL + endpoint
    print(f"\n🔗 POST {endpoint}")
    print(f"   Payload: {payload}")
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"   ✅ FUNCIONA! Status: {response.status_code}")
            data = response.json()
            print(f"   Tipo: {type(data)}")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"   Items: {len(data)}")
                print(f"   Primer item: {list(data[0].keys())[:10] if isinstance(data[0], dict) else data[0]}")
            elif isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:10]}")
                
        elif response.status_code == 404:
            print(f"   ❌ 404 - No encontrado")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

# Intentar acceder a la documentación
print("\n\n📚 Intentando acceder a documentación...")
print("=" * 70)

docs_urls = [
    "/docs",
    "/api-docs",
    "/swagger",
    "/api/docs",
]

for doc_url in docs_urls:
    url = BASE_URL + doc_url
    print(f"\n🔗 {doc_url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Documentación disponible en: {url}")
            print(f"   Abre en navegador para ver endpoints disponibles")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except:
        print(f"   ❌ No disponible")

print("\n" + "=" * 70)
print("🎯 RECOMENDACIÓN:")
print("=" * 70)
print("\nSi ningún endpoint funciona, intenta:")
print("1. Acceder a la documentación en el navegador:")
print(f"   {BASE_URL}/docs")
print(f"   {BASE_URL}/swagger")
print("\n2. Contactar al proveedor de Evolution API para conocer los endpoints")
print("\n3. Usar la interfaz web de Evolution API si está disponible")
print()
