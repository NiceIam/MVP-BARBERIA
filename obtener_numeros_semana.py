"""Script optimizado para obtener números de la última semana."""
import os
import requests
from datetime import datetime, timedelta
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
print("📱 NÚMEROS DE LA ÚLTIMA SEMANA - BARBERÍA CHURCO")
print("=" * 70)

# Calcular fechas
ahora = datetime.now()
hace_una_semana = ahora - timedelta(days=7)

print(f"\n📅 Rango de fechas:")
print(f"   Desde: {hace_una_semana.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Hasta: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

# Payload con formato ISO
payload = {
    "limit": 1000,  # Aumentar para obtener más mensajes
    "startDate": hace_una_semana.isoformat(),
    "endDate": ahora.isoformat()
}

print(f"\n🔍 Obteniendo mensajes...")
print(f"Límite: {payload['limit']} mensajes")

try:
    url = f"{BASE_URL}/chat/findMessages/{INSTANCE}"
    response = requests.post(url, json=payload, headers=HEADERS, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
    data = response.json()
    messages_data = data.get('messages', {})
    records = messages_data.get('records', [])
    total = messages_data.get('total', 0)
    
    print(f"✅ Total de mensajes en sistema: {total:,}")
    print(f"✅ Mensajes obtenidos: {len(records)}")
    
    # Extraer números únicos
    timestamp_inicio = int(hace_una_semana.timestamp())
    timestamp_fin = int(ahora.timestamp())
    
    numeros_set = set()
    contactos = {}
    mensajes_en_rango = 0
    
    for mensaje in records:
        msg_timestamp = mensaje.get('messageTimestamp', 0)
        
        # Verificar que esté en el rango
        if timestamp_inicio <= msg_timestamp <= timestamp_fin:
            mensajes_en_rango += 1
            
            key = mensaje.get('key', {})
            remote_jid_alt = key.get('remoteJidAlt', '')
            
            # Solo números personales
            if '@s.whatsapp.net' in remote_jid_alt:
                numero = remote_jid_alt.replace('@s.whatsapp.net', '')
                numeros_set.add(numero)
                
                if numero not in contactos:
                    push_name = mensaje.get('pushName', 'Sin nombre')
                    contactos[numero] = {
                        'nombre': push_name,
                        'timestamp': msg_timestamp
                    }
                else:
                    # Actualizar si este mensaje es más reciente
                    if msg_timestamp > contactos[numero]['timestamp']:
                        contactos[numero]['timestamp'] = msg_timestamp
    
    print(f"✅ Mensajes en rango de fechas: {mensajes_en_rango}")
    print(f"✅ Números únicos encontrados: {len(numeros_set)}")
    
    # Convertir a lista y ordenar
    numeros_lista = []
    for numero in numeros_set:
        info = contactos.get(numero, {})
        numeros_lista.append({
            'numero': numero,
            'nombre': info.get('nombre', 'Sin nombre'),
            'timestamp': info.get('timestamp', 0)
        })
    
    numeros_lista.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Mostrar lista
    print("\n📋 LISTA COMPLETA DE CONTACTOS:")
    print("=" * 70)
    
    for i, contacto in enumerate(numeros_lista, 1):
        numero = contacto['numero']
        nombre = contacto['nombre']
        ts = contacto['timestamp']
        fecha = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        print(f"{i}. {numero} - {nombre} (Último: {fecha})")
    
    # Solo números
    print("\n📱 SOLO NÚMEROS (para copiar):")
    print("=" * 70)
    todos_numeros = [c['numero'] for c in numeros_lista]
    print(", ".join(todos_numeros))
    
    # Exportar a archivo
    print("\n💾 Exportando a archivo...")
    filename = f"numeros_ultima_semana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("NÚMEROS DE LA ÚLTIMA SEMANA - BARBERÍA CHURCO\n")
        f.write(f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Rango: {hace_una_semana.strftime('%Y-%m-%d')} a {ahora.strftime('%Y-%m-%d')}\n")
        f.write(f"Total de números: {len(numeros_lista)}\n")
        f.write(f"Mensajes analizados: {mensajes_en_rango}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("LISTA COMPLETA (ordenada por más reciente):\n")
        f.write("-" * 70 + "\n")
        for i, contacto in enumerate(numeros_lista, 1):
            numero = contacto['numero']
            nombre = contacto['nombre']
            ts = contacto['timestamp']
            fecha = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
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
    print(f"Período: Última semana ({hace_una_semana.strftime('%d/%m')} - {ahora.strftime('%d/%m')})")
    print(f"Mensajes analizados: {mensajes_en_rango:,}")
    print(f"Números únicos: {len(numeros_lista)}")
    print(f"Archivo: {filename}")
    
    print("\n💡 PRÓXIMOS PASOS:")
    print("=" * 70)
    print("1. Revisa el archivo generado")
    print("2. Usa estos números para enviar mensajes:")
    print("   python enviar_mensaje_masivo.py")
    print("\n⚠️  RECOMENDACIONES:")
    print("   - Empieza con 10-20 mensajes para probar")
    print("   - Usa delay de 10 segundos entre mensajes")
    print("   - Envía en horarios apropiados (10 AM - 7 PM)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n")
