"""Script de prueba para enviar mensaje a un número específico."""
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', '')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY', '')
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME', '')

print("=" * 70)
print("🧪 TEST - Envío de Mensaje de Prueba")
print("=" * 70)

# Verificar configuración
print("\n📋 Configuración:")
print(f"   URL: {EVOLUTION_API_URL}")
print(f"   Instance: {EVOLUTION_INSTANCE_NAME}")
print(f"   API Key: {'✅ Configurada' if EVOLUTION_API_KEY else '❌ NO configurada'}")

if not all([EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME]):
    print("\n❌ Error: Faltan variables de entorno")
    exit(1)

# Número de destino
TELEFONO = "573123613840"

# Mensaje de prueba
MENSAJE = """🔔 *Mensaje de Prueba - Barbería Churco*

Hola! 👋

Este es un mensaje de prueba del sistema de notificaciones.

Si recibes este mensaje, significa que el sistema está funcionando correctamente. ✅

_Escribe *hola* para volver al menú principal._"""

print(f"\n📱 Número de destino: {TELEFONO}")
print(f"\n📝 Mensaje:")
print("-" * 70)
print(MENSAJE)
print("-" * 70)

# Enviar mensaje
print(f"\n📤 Enviando mensaje...")

try:
    BASE_URL = EVOLUTION_API_URL.rstrip('/')
    url = f"{BASE_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}"
    
    headers = {
        'apikey': EVOLUTION_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "number": TELEFONO,
        "text": MENSAJE
    }
    
    print(f"\n🔗 URL: {url}")
    print(f"📦 Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text}")
    
    response.raise_for_status()
    
    print("\n" + "=" * 70)
    print("✅ MENSAJE ENVIADO EXITOSAMENTE!")
    print("=" * 70)
    print(f"\n💡 Revisa tu WhatsApp ({TELEFONO}) para confirmar la recepción.")
    
except requests.exceptions.RequestException as e:
    print("\n" + "=" * 70)
    print("❌ ERROR AL ENVIAR MENSAJE")
    print("=" * 70)
    print(f"\n{e}")
    
    if hasattr(e, 'response') and e.response is not None:
        print(f"\nDetalles del error:")
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

print()
