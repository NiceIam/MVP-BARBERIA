"""
Script para probar que el webhook esté funcionando correctamente
"""
import requests
import json

# URL de tu servidor desplegado
BASE_URL = "http://localhost:8000"  # Cambia esto por tu URL de producción

def test_health():
    """Prueba el endpoint de salud"""
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Respuesta: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_root():
    """Prueba el endpoint raíz"""
    print("\n" + "=" * 60)
    print("TEST 2: Root Endpoint")
    print("=" * 60)
    
    url = f"{BASE_URL}/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Respuesta: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_webhook_simulado():
    """Simula un mensaje de WhatsApp al webhook"""
    print("\n" + "=" * 60)
    print("TEST 3: Webhook Simulado")
    print("=" * 60)
    
    url = f"{BASE_URL}/webhook"
    
    # Simular estructura de mensaje de Evolution API
    payload = {
        "event": "messages.upsert",
        "data": {
            "key": {
                "remoteJid": "573001234567@s.whatsapp.net",
                "fromMe": False,
                "id": "TEST123"
            },
            "messageType": "conversation",
            "message": {
                "conversation": "Hola"
            }
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Respuesta: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_send_message():
    """Prueba el endpoint de envío de mensajes"""
    print("\n" + "=" * 60)
    print("TEST 4: Envío de Mensaje")
    print("=" * 60)
    
    url = f"{BASE_URL}/send-message"
    
    payload = {
        "telefono": "3001234567",
        "mensaje": "Mensaje de prueba desde el script de testing"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Respuesta: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_stats():
    """Prueba el endpoint de estadísticas"""
    print("\n" + "=" * 60)
    print("TEST 5: Estadísticas")
    print("=" * 60)
    
    url = f"{BASE_URL}/stats"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Respuesta: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("🧪 SUITE DE PRUEBAS DEL WEBHOOK")
    print("=" * 60)
    print(f"\n🌐 URL Base: {BASE_URL}")
    
    resultados = []
    
    # Test 1: Health
    resultados.append(("Health Check", test_health()))
    
    # Test 2: Root
    resultados.append(("Root Endpoint", test_root()))
    
    # Test 3: Webhook
    resultados.append(("Webhook Simulado", test_webhook_simulado()))
    
    # Test 4: Send Message
    resultados.append(("Envío de Mensaje", test_send_message()))
    
    # Test 5: Stats
    resultados.append(("Estadísticas", test_stats()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for nombre, resultado in resultados:
        estado = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{estado} - {nombre}")
    
    total = len(resultados)
    exitosos = sum(1 for _, r in resultados if r)
    
    print("\n" + "=" * 60)
    print(f"Resultado: {exitosos}/{total} pruebas exitosas")
    print("=" * 60)
    
    if exitosos == total:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("\n✅ Tu servidor está funcionando correctamente")
        print(f"✅ El webhook está listo en: {BASE_URL}/webhook")
        print("\n💡 Próximos pasos:")
        print("  1. Ejecuta: python configurar_webhook.py")
        print("  2. Selecciona opción 5 (Todo)")
        print("  3. Escanea el código QR con WhatsApp")
        print("  4. Envía un mensaje al número de WhatsApp")
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        print("\n💡 Verifica:")
        print("  1. Que el servidor esté corriendo")
        print("  2. Que la URL sea correcta")
        print("  3. Que no haya problemas de red/firewall")


if __name__ == "__main__":
    ejecutar_todos_los_tests()
