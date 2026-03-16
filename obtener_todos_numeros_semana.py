"""Script para obtener TODOS los números de la última semana con paginación."""
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

load_dotenv()

BASE_URL = os.getenv('EVOLUTION_API_URL', '').rstrip('/')
API_KEY = os.getenv('EVOLUTION_API_KEY', '')
INSTANCE = os.getenv('EVOLUTION_INSTANCE_NAME', '')

HEADERS = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
}

print("=" * 70)
print("📱 OBTENER TODOS LOS NÚMEROS DE LA ÚLTIMA SEMANA")
print("=" * 70)

# Calcular fechas
ahora = datetime.now()
hace_una_semana = ahora - timedelta(days=7)

print(f"\n📅 Rango de fechas:")
print(f"   Desde: {hace_una_semana.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Hasta: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

timestamp_inicio = int(hace_una_semana.timestamp())
timestamp_fin = int(ahora.timestamp())

url = f"{BASE_URL}/chat/findMessages/{INSTANCE}"

# Recolectar todos los números
numeros_set = set()
contactos = {}
total_mensajes_procesados = 0
total_mensajes_en_rango = 0

print(f"\n🔍 Obteniendo mensajes con paginación...")
print("=" * 70)

# Intentar con paginación
page = 1
max_pages = 100  # Límite de seguridad

while page <= max_pages:
    # Probar diferentes formatos de paginación
    payloads_a_probar = [
        {
            "limit": 50,
            "page": page,
            "startDate": hace_una_semana.isoformat(),
            "endDate": ahora.isoformat()
        },
        {
            "limit": 50,
            "offset": (page - 1) * 50,
            "startDate": hace_una_semana.isoformat(),
            "endDate": ahora.isoformat()
        },
        {
            "limit": 50,
            "skip": (page - 1) * 50,
            "startDate": hace_una_semana.isoformat(),
            "endDate": ahora.isoformat()
        }
    ]
    
    records = []
    
    for payload in payloads_a_probar:
        try:
            response = requests.post(url, json=payload, headers=HEADERS, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                messages_data = data.get('messages', {})
                records = messages_data.get('records', [])
                
                if records:
                    print(f"\n📄 Página {page} - Payload funcionó: {list(payload.keys())}")
                    break
        except:
            continue
    
    if not records:
        print(f"\n⚠️  Página {page} - No se obtuvieron más mensajes")
        break
    
    print(f"   Mensajes obtenidos: {len(records)}")
    
    # Procesar mensajes
    mensajes_nuevos_en_rango = 0
    
    for mensaje in records:
        total_mensajes_procesados += 1
        msg_timestamp = mensaje.get('messageTimestamp', 0)
        
        # Verificar que esté en el rango
        if timestamp_inicio <= msg_timestamp <= timestamp_fin:
            total_mensajes_en_rango += 1
            mensajes_nuevos_en_rango += 1
            
            key = mensaje.get('key', {})
            remote_jid_alt = key.get('remoteJidAlt', '')
            
            # Solo números personales
            if '@s.whatsapp.net' in remote_jid_alt:
                numero = remote_jid_alt.replace('@s.whatsapp.net', '')
                
                if numero not in numeros_set:
                    numeros_set.add(numero)
                    push_name = mensaje.get('pushName', 'Sin nombre')
                    contactos[numero] = {
                        'nombre': push_name,
                        'timestamp': msg_timestamp
                    }
                else:
                    # Actualizar si este mensaje es más reciente
                    if msg_timestamp > contactos[numero]['timestamp']:
                        contactos[numero]['timestamp'] = msg_timestamp
    
    print(f"   Mensajes en rango: {mensajes_nuevos_en_rango}")
    print(f"   Números únicos hasta ahora: {len(numeros_set)}")
    
    # Si no hay más mensajes en el rango, detener
    if mensajes_nuevos_en_rango == 0:
        print(f"\n✅ No hay más mensajes en el rango de fechas")
        break
    
    # Si obtuvimos menos de 50, probablemente es la última página
    if len(records) < 50:
        print(f"\n✅ Última página alcanzada")
        break
    
    page += 1
    
    # Pequeño delay para no saturar la API
    time.sleep(0.5)

print("\n" + "=" * 70)
print("📊 PROCESAMIENTO COMPLETADO")
print("=" * 70)
print(f"Total de mensajes procesados: {total_mensajes_procesados:,}")
print(f"Mensajes en rango de fechas: {total_mensajes_en_rango:,}")
print(f"Números únicos encontrados: {len(numeros_set)}")

if len(numeros_set) == 0:
    print("\n❌ No se encontraron números")
    print("\n💡 Posibles razones:")
    print("   1. No hay mensajes en la última semana")
    print("   2. La API no soporta paginación")
    print("   3. El filtro de fecha no está funcionando correctamente")
    exit(0)

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
filename = f"todos_numeros_semana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(filename, 'w', encoding='utf-8') as f:
    f.write("TODOS LOS NÚMEROS DE LA ÚLTIMA SEMANA - BARBERÍA CHURCO\n")
    f.write(f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Rango: {hace_una_semana.strftime('%Y-%m-%d')} a {ahora.strftime('%Y-%m-%d')}\n")
    f.write(f"Total de números: {len(numeros_lista)}\n")
    f.write(f"Mensajes procesados: {total_mensajes_procesados:,}\n")
    f.write(f"Mensajes en rango: {total_mensajes_en_rango:,}\n")
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

# Resumen final
print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)
print(f"Período: Última semana ({hace_una_semana.strftime('%d/%m')} - {ahora.strftime('%d/%m')})")
print(f"Páginas procesadas: {page}")
print(f"Mensajes totales procesados: {total_mensajes_procesados:,}")
print(f"Mensajes en rango: {total_mensajes_en_rango:,}")
print(f"Números únicos: {len(numeros_lista)}")
print(f"Archivo: {filename}")

print("\n💡 PRÓXIMOS PASOS:")
print("=" * 70)
print("1. Revisa el archivo generado")
print("2. Usa estos números para enviar mensajes:")
print("   python enviar_mensaje_masivo.py")

print()
