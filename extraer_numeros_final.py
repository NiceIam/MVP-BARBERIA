"""Script FINAL para extraer números de WhatsApp desde Evolution API."""
import os
import requests
from datetime import datetime
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
print("📱 EXTRAER NÚMEROS DE WHATSAPP - BARBERÍA CHURCO")
print("=" * 70)

print("\n🔍 Obteniendo mensajes...")

try:
    url = f"{BASE_URL}/chat/findMessages/{INSTANCE}"
    
    # Obtener múltiples páginas para tener más números
    payload = {
        "limit": 50  # Mensajes por página
    }
    
    print(f"URL: {url}")
    
    response = requests.post(url, json=payload, headers=HEADERS, timeout=30)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        exit(1)
    
    data = response.json()
    messages_data = data.get('messages', {})
    records = messages_data.get('records', [])
    total = messages_data.get('total', 0)
    
    print(f"✅ Total de mensajes en sistema: {total}")
    print(f"✅ Mensajes obtenidos: {len(records)}")
    
    # Extraer números únicos
    numeros_set = set()
    contactos = {}
    
    for mensaje in records:
        key = mensaje.get('key', {})
        
        # Obtener número del remoteJidAlt (formato: 573XXXXXXXXX@s.whatsapp.net)
        remote_jid_alt = key.get('remoteJidAlt', '')
        
        # Solo números personales (no grupos, no lids)
        if '@s.whatsapp.net' in remote_jid_alt:
            numero = remote_jid_alt.replace('@s.whatsapp.net', '')
            numeros_set.add(numero)
            
            # Guardar info adicional
            if numero not in contactos:
                push_name = mensaje.get('pushName', 'Sin nombre')
                message_timestamp = mensaje.get('messageTimestamp', 0)
                
                contactos[numero] = {
                    'nombre': push_name,
                    'timestamp': message_timestamp
                }
    
    # Convertir a lista y ordenar por timestamp
    numeros_lista = []
    for numero in numeros_set:
        info = contactos.get(numero, {})
        numeros_lista.append({
            'numero': numero,
            'nombre': info.get('nombre', 'Sin nombre'),
            'timestamp': info.get('timestamp', 0)
        })
    
    # Ordenar por timestamp (más reciente primero)
    numeros_lista.sort(key=lambda x: x['timestamp'], reverse=True)
    
    print(f"\n✅ Se encontraron {len(numeros_lista)} números únicos")
    
    # Mostrar todos los contactos
    print("\n📋 LISTA COMPLETA DE CONTACTOS:")
    print("=" * 70)
    
    for i, contacto in enumerate(numeros_lista, 1):
        numero = contacto['numero']
        nombre = contacto['nombre']
        timestamp = contacto['timestamp']
        
        if timestamp:
            fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        else:
            fecha = 'Sin fecha'
        
        print(f"{i}. {numero} - {nombre} (Último: {fecha})")
    
    # Solo números
    print("\n📱 SOLO NÚMEROS (para copiar):")
    print("=" * 70)
    todos_numeros = [c['numero'] for c in numeros_lista]
    print(", ".join(todos_numeros))
    
    # Exportar a archivo
    print("\n💾 Exportando a archivo...")
    filename = f"numeros_whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("NÚMEROS DE WHATSAPP - BARBERÍA CHURCO\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de mensajes en sistema: {total}\n")
        f.write(f"Números únicos encontrados: {len(numeros_lista)}\n")
        f.write(f"Fuente: Evolution API - Mensajes\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("LISTA COMPLETA (ordenada por más reciente):\n")
        f.write("-" * 70 + "\n")
        for i, contacto in enumerate(numeros_lista, 1):
            numero = contacto['numero']
            nombre = contacto['nombre']
            timestamp = contacto['timestamp']
            
            if timestamp:
                fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            else:
                fecha = 'Sin fecha'
            
            f.write(f"{i}. {numero} - {nombre} (Último: {fecha})\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("SOLO NÚMEROS (separados por coma):\n")
        f.write("-" * 70 + "\n")
        f.write(", ".join(todos_numeros))
        f.write("\n\n")
        
        f.write("SOLO NÚMEROS (uno por línea):\n")
        f.write("-" * 70 + "\n")
        for numero in todos_numeros:
            f.write(f"{numero}\n")
    
    print(f"✅ Archivo creado: {filename}")
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"Total de mensajes en sistema: {total:,}")
    print(f"Mensajes analizados: {len(records)}")
    print(f"Números únicos encontrados: {len(numeros_lista)}")
    print(f"Archivo exportado: {filename}")
    
    print("\n💡 PRÓXIMOS PASOS:")
    print("=" * 70)
    print("1. Revisa el archivo generado para ver todos los números")
    print("2. Copia los números que quieres contactar")
    print("3. Usa el script de mensajes masivos:")
    print("   python enviar_mensaje_masivo.py")
    print("\n⚠️  IMPORTANTE:")
    print("   - Estos son contactos que han enviado mensajes")
    print("   - Empieza con pocos mensajes (10-20) para probar")
    print("   - Usa delay de 10 segundos entre mensajes")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n")
