"""Script para extraer números de teléfono desde mensajes de Evolution API."""
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
print("📱 EXTRAER NÚMEROS DESDE MENSAJES - BARBERÍA CHURCO")
print("=" * 70)

print("\n🔍 Obteniendo mensajes...")

try:
    url = f"{BASE_URL}/chat/findMessages/{INSTANCE}"
    
    # Intentar obtener muchos mensajes para tener más números únicos
    payload = {
        "limit": 1000  # Máximo posible
    }
    
    print(f"URL: {url}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=HEADERS, timeout=30)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        exit(1)
    
    data = response.json()
    mensajes = data.get('messages', [])
    
    print(f"✅ Se obtuvieron {len(mensajes)} mensajes")
    
    # Debug: ver estructura del primer mensaje
    if mensajes:
        print(f"\n🔍 Estructura del primer mensaje:")
        print(f"Tipo: {type(mensajes[0])}")
        if isinstance(mensajes[0], dict):
            print(f"Keys: {list(mensajes[0].keys())}")
        else:
            print(f"Valor: {mensajes[0]}")
    
    # Extraer números únicos
    numeros_set = set()
    contactos = {}
    
    for mensaje in mensajes:
        # Si el mensaje es un string, parsearlo
        if isinstance(mensaje, str):
            import json
            try:
                mensaje = json.loads(mensaje)
            except:
                continue
        
        if not isinstance(mensaje, dict):
            continue
        
        # Obtener el remoteJid (identificador del chat)
        key = mensaje.get('key', {})
        remote_jid = key.get('remoteJid', '')
        
        # Solo números personales (no grupos)
        if '@s.whatsapp.net' in remote_jid:
            numero = remote_jid.replace('@s.whatsapp.net', '')
            numeros_set.add(numero)
            
            # Guardar info adicional si está disponible
            if numero not in contactos:
                push_name = mensaje.get('pushName', 'Sin nombre')
                timestamp = mensaje.get('messageTimestamp', 0)
                
                contactos[numero] = {
                    'nombre': push_name,
                    'ultimo_mensaje': timestamp
                }
    
    # Convertir a lista y ordenar por timestamp
    numeros_lista = []
    for numero in numeros_set:
        info = contactos.get(numero, {})
        numeros_lista.append({
            'numero': numero,
            'nombre': info.get('nombre', 'Sin nombre'),
            'timestamp': info.get('ultimo_mensaje', 0)
        })
    
    # Ordenar por timestamp (más reciente primero)
    numeros_lista.sort(key=lambda x: x['timestamp'], reverse=True)
    
    print(f"\n✅ Se encontraron {len(numeros_lista)} números únicos")
    
    # Mostrar primeros 50
    print("\n📋 PRIMEROS 50 CONTACTOS (más recientes):")
    print("=" * 70)
    
    for i, contacto in enumerate(numeros_lista[:50], 1):
        numero = contacto['numero']
        nombre = contacto['nombre']
        timestamp = contacto['timestamp']
        
        if timestamp:
            fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        else:
            fecha = 'Sin fecha'
        
        print(f"{i}. {numero} - {nombre} (Último: {fecha})")
    
    if len(numeros_lista) > 50:
        print(f"\n... y {len(numeros_lista) - 50} más")
    
    # Solo números (primeros 50)
    print("\n📱 SOLO NÚMEROS (primeros 50):")
    print("=" * 70)
    numeros_50 = [c['numero'] for c in numeros_lista[:50]]
    print(", ".join(numeros_50))
    
    # Exportar a archivo
    print("\n💾 Exportando a archivo...")
    filename = f"numeros_whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("NÚMEROS DE WHATSAPP - BARBERÍA CHURCO\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(numeros_lista)}\n")
        f.write(f"Fuente: Mensajes de Evolution API\n")
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
        todos_numeros = [c['numero'] for c in numeros_lista]
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
    print(f"Mensajes analizados: {len(mensajes)}")
    print(f"Números únicos encontrados: {len(numeros_lista)}")
    print(f"Archivo exportado: {filename}")
    
    print("\n💡 PRÓXIMOS PASOS:")
    print("=" * 70)
    print("1. Revisa el archivo generado para ver todos los números")
    print("2. Usa estos números con el script de mensajes masivos:")
    print("   python enviar_mensaje_masivo.py")
    print("\n⚠️  IMPORTANTE:")
    print("   - Estos son TODOS los contactos que han enviado mensajes")
    print("   - Incluye clientes, consultas, etc.")
    print("   - Filtra manualmente si es necesario")
    print("   - Empieza con pocos mensajes (10-20) para probar")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n")
