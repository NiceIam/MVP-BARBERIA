"""
Script para configurar el webhook en Evolution API
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# URL de tu servidor desplegado
WEBHOOK_URL = "https://n8n-barberia-mvp.dtbfmw.easypanel.host/webhook"

def configurar_webhook():
    """Configura el webhook en Evolution API"""
    
    api_url = os.getenv("EVOLUTION_API_URL")
    api_key = os.getenv("EVOLUTION_API_KEY")
    instance_name = os.getenv("EVOLUTION_INSTANCE_NAME")
    
    print("=" * 60)
    print("🔧 CONFIGURACIÓN DE WEBHOOK EN EVOLUTION API")
    print("=" * 60)
    
    print(f"\n📡 URL del Webhook: {WEBHOOK_URL}")
    print(f"🔑 Instancia: {instance_name}")
    
    # Configurar webhook
    endpoint = f"{api_url.rstrip('/')}/webhook/set/{instance_name}"
    
    headers = {
        'Content-Type': 'application/json',
        'apikey': api_key
    }
    
    data = {
        "url": WEBHOOK_URL,
        "webhook_by_events": False,
        "webhook_base64": False,
        "events": [
            "MESSAGES_UPSERT",
            "MESSAGES_UPDATE",
            "CONNECTION_UPDATE",
            "QRCODE_UPDATED"
        ]
    }
    
    print("\n📤 Enviando configuración a Evolution API...")
    
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        
        print("✅ Webhook configurado exitosamente!")
        print(f"\n📋 Respuesta de Evolution API:")
        print(response.json())
        
        # Verificar configuración
        print("\n🔍 Verificando configuración...")
        verificar_webhook()
        
        print("\n" + "=" * 60)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print("\n💡 Próximos pasos:")
        print("  1. Asegúrate de que tu servidor esté corriendo")
        print("  2. Verifica que WhatsApp esté conectado")
        print("  3. Envía un mensaje de prueba al número de WhatsApp")
        print("\n🧪 Para probar:")
        print(f"  curl {WEBHOOK_URL.replace('/webhook', '/health')}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error configurando webhook: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Respuesta: {e.response.text}")
        
        print("\n💡 Verifica:")
        print("  1. Que Evolution API esté accesible")
        print("  2. Que el API_KEY sea correcto")
        print("  3. Que la instancia exista")


def verificar_webhook():
    """Verifica la configuración actual del webhook"""
    
    api_url = os.getenv("EVOLUTION_API_URL")
    api_key = os.getenv("EVOLUTION_API_KEY")
    instance_name = os.getenv("EVOLUTION_INSTANCE_NAME")
    
    endpoint = f"{api_url.rstrip('/')}/webhook/find/{instance_name}"
    
    headers = {
        'Content-Type': 'application/json',
        'apikey': api_key
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        config = response.json()
        print("✅ Configuración actual del webhook:")
        print(f"   URL: {config.get('url', 'No configurada')}")
        print(f"   Eventos: {', '.join(config.get('events', []))}")
        
        return config
        
    except Exception as e:
        print(f"⚠️  No se pudo verificar la configuración: {e}")
        return None


def verificar_instancia():
    """Verifica el estado de la instancia"""
    
    api_url = os.getenv("EVOLUTION_API_URL")
    api_key = os.getenv("EVOLUTION_API_KEY")
    instance_name = os.getenv("EVOLUTION_INSTANCE_NAME")
    
    print("\n🔍 Verificando estado de la instancia...")
    
    endpoint = f"{api_url.rstrip('/')}/instance/connectionState/{instance_name}"
    
    headers = {
        'Content-Type': 'application/json',
        'apikey': api_key
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        estado = response.json()
        print(f"✅ Estado de la instancia: {estado}")
        
        return estado
        
    except Exception as e:
        print(f"❌ Error verificando instancia: {e}")
        return None


def obtener_qr():
    """Obtiene el código QR si la instancia no está conectada"""
    
    api_url = os.getenv("EVOLUTION_API_URL")
    api_key = os.getenv("EVOLUTION_API_KEY")
    instance_name = os.getenv("EVOLUTION_INSTANCE_NAME")
    
    print("\n📱 Obteniendo código QR...")
    
    endpoint = f"{api_url.rstrip('/')}/instance/connect/{instance_name}"
    
    headers = {
        'Content-Type': 'application/json',
        'apikey': api_key
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        qr_data = response.json()
        
        if 'qrcode' in qr_data or 'base64' in qr_data:
            print("✅ Código QR generado")
            print("\n💡 Escanea el código QR con WhatsApp:")
            print("   1. Abre WhatsApp en tu teléfono")
            print("   2. Ve a Configuración > Dispositivos vinculados")
            print("   3. Toca 'Vincular un dispositivo'")
            print("   4. Escanea el código QR")
            
            # Si hay una URL del QR, mostrarla
            if 'qrcode' in qr_data:
                print(f"\n🔗 URL del QR: {qr_data['qrcode']}")
        else:
            print("ℹ️  La instancia ya está conectada")
        
        return qr_data
        
    except Exception as e:
        print(f"❌ Error obteniendo QR: {e}")
        return None


def menu_principal():
    """Menú principal de configuración"""
    
    print("\n" + "=" * 60)
    print("🔧 CONFIGURACIÓN DE EVOLUTION API")
    print("=" * 60)
    print("\n¿Qué deseas hacer?")
    print("\n1. Configurar webhook")
    print("2. Verificar webhook actual")
    print("3. Verificar estado de instancia")
    print("4. Obtener código QR")
    print("5. Todo (configurar y verificar)")
    print("0. Salir")
    
    opcion = input("\nSelecciona una opción: ").strip()
    
    if opcion == "1":
        configurar_webhook()
    elif opcion == "2":
        verificar_webhook()
    elif opcion == "3":
        verificar_instancia()
    elif opcion == "4":
        obtener_qr()
    elif opcion == "5":
        print("\n🚀 Ejecutando configuración completa...\n")
        verificar_instancia()
        configurar_webhook()
        obtener_qr()
    elif opcion == "0":
        print("\n👋 ¡Hasta luego!")
    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    menu_principal()
