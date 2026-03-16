"""Script para ver los chats disponibles sin enviar mensajes."""
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', '')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY', '')
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME', '')

BASE_URL = EVOLUTION_API_URL.rstrip('/')
HEADERS = {
    'apikey': EVOLUTION_API_KEY,
    'Content-Type': 'application/json'
}

print("=" * 70)
print("📱 LISTA DE CHATS - BARBERÍA CHURCO")
print("=" * 70)

# Obtener chats
print("\n🔍 Obteniendo chats...")
try:
    url = f"{BASE_URL}/chat/findChats/{EVOLUTION_INSTANCE_NAME}"
    
    print(f"\n🔗 URL: {url}")
    print(f"🔑 API Key: {EVOLUTION_API_KEY[:10]}...")
    
    response = requests.get(url, headers=HEADERS, timeout=30)
    
    print(f"📊 Status Code: {response.status_code}")
    
    response.raise_for_status()
    data = response.json()
    
    # Filtrar solo chats personales (no grupos)
    chats = [chat for chat in data if '@s.whatsapp.net' in chat.get('id', '')]
    
    # Ordenar por timestamp (más reciente primero)
    chats_ordenados = sorted(
        chats, 
        key=lambda x: x.get('conversationTimestamp', 0), 
        reverse=True
    )
    
    # Tomar los últimos 50
    chats_recientes = chats_ordenados[:50]
    
    print(f"\n✅ Total de chats personales: {len(chats)}")
    print(f"📋 Mostrando los últimos 50 chats más recientes:")
    print("=" * 70)
    
    # Mostrar chats
    for i, chat in enumerate(chats_recientes, 1):
        chat_id = chat.get('id', '')
        telefono = chat_id.replace('@s.whatsapp.net', '')
        nombre = chat.get('name', 'Sin nombre')
        
        # Timestamp de la última conversación
        timestamp = chat.get('conversationTimestamp', 0)
        if timestamp:
            fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            fecha = 'Sin fecha'
        
        # Último mensaje
        ultimo_mensaje = chat.get('lastMessage', {})
        mensaje_texto = ''
        if ultimo_mensaje:
            mensaje_texto = ultimo_mensaje.get('message', {}).get('conversation', '')
            if not mensaje_texto:
                mensaje_texto = ultimo_mensaje.get('message', {}).get('extendedTextMessage', {}).get('text', '')
            if mensaje_texto and len(mensaje_texto) > 50:
                mensaje_texto = mensaje_texto[:50] + '...'
        
        print(f"\n{i}. {telefono}")
        print(f"   Nombre: {nombre}")
        print(f"   Última conversación: {fecha}")
        if mensaje_texto:
            print(f"   Último mensaje: {mensaje_texto}")
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"Total de chats: {len(chats)}")
    print(f"Mostrando: {len(chats_recientes)}")
    
    # Exportar a archivo
    print("\n💾 ¿Quieres exportar la lista a un archivo? (s/n): ", end="")
    exportar = input().strip().lower()
    
    if exportar == 's':
        filename = f"chats_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("LISTA DE CHATS - BARBERÍA CHURCO\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total: {len(chats_recientes)}\n")
            f.write("=" * 70 + "\n\n")
            
            for i, chat in enumerate(chats_recientes, 1):
                chat_id = chat.get('id', '')
                telefono = chat_id.replace('@s.whatsapp.net', '')
                nombre = chat.get('name', 'Sin nombre')
                timestamp = chat.get('conversationTimestamp', 0)
                if timestamp:
                    fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    fecha = 'Sin fecha'
                
                f.write(f"{i}. {telefono}\n")
                f.write(f"   Nombre: {nombre}\n")
                f.write(f"   Última conversación: {fecha}\n\n")
        
        print(f"✅ Lista exportada a: {filename}")
    
    # Mostrar solo números para copiar
    print("\n📋 SOLO NÚMEROS (para copiar):")
    print("=" * 70)
    numeros = [chat.get('id', '').replace('@s.whatsapp.net', '') for chat in chats_recientes]
    print(", ".join(numeros))
    
except requests.exceptions.RequestException as e:
    print(f"\n❌ Error obteniendo chats: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"\nDetalles del error:")
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

print("\n")
