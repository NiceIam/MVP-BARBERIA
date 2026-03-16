"""Script para extraer números de la última semana."""
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
print("📱 EXTRAER NÚMEROS DE LA ÚLTIMA SEMANA - BARBERÍA CHURCO")
print("=" * 70)

# Calcular fechas
ahora = datetime.now()
hace_una_semana = ahora - timedelta(days=7)

print(f"\n📅 Rango de fechas:")
print(f"   Desde: {hace_una_semana.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Hasta: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

# Convertir a timestamps (segundos desde epoch)
timestamp_inicio = int(hace_una_semana.timestamp())
timestamp_fin = int(ahora.timestamp())

print(f"\n🔢 Timestamps:")
print(f"   Inicio: {timestamp_inicio}")
print(f"   Fin: {timestamp_fin}")

print("\n🔍 Probando diferentes formatos de payload...")

# Intentar diferentes formatos de payload
payloads_a_probar = [
    {
        "limit": 1000,
        "where": {
            "messageTimestamp": {
                "gte": timestamp_inicio,
                "lte": timestamp_fin
            }
        }
    },
    {
        "limit": 1000,
        "startDate": hace_una_semana.isoformat(),
        "endDate": ahora.isoformat()
    },
    {
        "limit": 1000,
        "dateStart": hace_una_semana.strftime('%Y-%m-%d'),
        "dateEnd": ahora.strftime('%Y-%m-%d')
    },
    {
        "limit": 1000,
        "fromTimestamp": timestamp_inicio,
        "toTimestamp": timestamp_fin
    },
    {
        "limit": 1000,
        "filter": {
            "timestamp": {
                "$gte": timestamp_inicio,
                "$lte": timestamp_fin
            }
        }
    }
]

url = f"{BASE_URL}/chat/findMessages/{INSTANCE}"

for i, payload in enumerate(payloads_a_probar, 1):
    print(f"\n{i}. Probando payload:")
    print(f"   {payload}")
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            messages_data = data.get('messages', {})
            records = messages_data.get('records', [])
            total = messages_data.get('total', 0)
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Total en sistema: {total}")
            print(f"   Mensajes obtenidos: {len(records)}")
            
            # Verificar si los mensajes están en el rango de fechas
            if records:
                primer_timestamp = records[0].get('messageTimestamp', 0)
                ultimo_timestamp = records[-1].get('messageTimestamp', 0)
                
                if primer_timestamp:
                    primer_fecha = datetime.fromtimestamp(primer_timestamp)
                    print(f"   Primer mensaje: {primer_fecha.strftime('%Y-%m-%d %H:%M')}")
                
                if ultimo_timestamp:
                    ultima_fecha = datetime.fromtimestamp(ultimo_timestamp)
                    print(f"   Último mensaje: {ultima_fecha.strftime('%Y-%m-%d %H:%M')}")
                
                # Contar mensajes en el rango
                mensajes_en_rango = 0
                for msg in records:
                    msg_timestamp = msg.get('messageTimestamp', 0)
                    if timestamp_inicio <= msg_timestamp <= timestamp_fin:
                        mensajes_en_rango += 1
                
                print(f"   Mensajes en rango (última semana): {mensajes_en_rango}")
                
                if mensajes_en_rango > 0:
                    print(f"   🎯 ¡ESTE PAYLOAD FUNCIONA!")
                    
                    # Extraer números
                    numeros_set = set()
                    contactos = {}
                    
                    for mensaje in records:
                        msg_timestamp = mensaje.get('messageTimestamp', 0)
                        
                        # Solo mensajes de la última semana
                        if timestamp_inicio <= msg_timestamp <= timestamp_fin:
                            key = mensaje.get('key', {})
                            remote_jid_alt = key.get('remoteJidAlt', '')
                            
                            if '@s.whatsapp.net' in remote_jid_alt:
                                numero = remote_jid_alt.replace('@s.whatsapp.net', '')
                                numeros_set.add(numero)
                                
                                if numero not in contactos:
                                    push_name = mensaje.get('pushName', 'Sin nombre')
                                    contactos[numero] = {
                                        'nombre': push_name,
                                        'timestamp': msg_timestamp
                                    }
                    
                    print(f"\n   📊 Números únicos encontrados: {len(numeros_set)}")
                    
                    if numeros_set:
                        print(f"\n   📋 Lista de números:")
                        numeros_lista = []
                        for numero in numeros_set:
                            info = contactos.get(numero, {})
                            numeros_lista.append({
                                'numero': numero,
                                'nombre': info.get('nombre', 'Sin nombre'),
                                'timestamp': info.get('timestamp', 0)
                            })
                        
                        numeros_lista.sort(key=lambda x: x['timestamp'], reverse=True)
                        
                        for j, contacto in enumerate(numeros_lista, 1):
                            numero = contacto['numero']
                            nombre = contacto['nombre']
                            ts = contacto['timestamp']
                            fecha = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                            print(f"      {j}. {numero} - {nombre} ({fecha})")
                        
                        # Exportar
                        filename = f"numeros_ultima_semana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write("NÚMEROS DE LA ÚLTIMA SEMANA - BARBERÍA CHURCO\n")
                            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"Rango: {hace_una_semana.strftime('%Y-%m-%d')} a {ahora.strftime('%Y-%m-%d')}\n")
                            f.write(f"Total: {len(numeros_lista)}\n")
                            f.write("=" * 70 + "\n\n")
                            
                            for j, contacto in enumerate(numeros_lista, 1):
                                numero = contacto['numero']
                                nombre = contacto['nombre']
                                ts = contacto['timestamp']
                                fecha = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                                f.write(f"{j}. {numero} - {nombre} ({fecha})\n")
                            
                            f.write("\n" + "=" * 70 + "\n")
                            f.write("SOLO NÚMEROS:\n")
                            f.write(", ".join([c['numero'] for c in numeros_lista]))
                        
                        print(f"\n   ✅ Archivo creado: {filename}")
                    
                    break  # Salir del loop si encontramos un payload que funciona
            
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

print("\n" + "=" * 70)
print("💡 NOTA:")
print("=" * 70)
print("Si ningún payload funcionó con filtro de fecha, significa que")
print("Evolution API no soporta filtrado por fecha en este endpoint.")
print("\nAlternativa: Obtener todos los mensajes y filtrar manualmente.")
print()
