"""Script para obtener contactos/chats de Evolution API."""
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = os.getenv('EVOLUTION_API_URL', '').rstrip('/')
API_KEY = os.getenv('EVOLUTION_API_KEY', '')
INSTANCE = os.getenv('EVOLUTION_INSTANCE_NAME', '')

HEADERS = {
    'apikey': API_KEY,
    'Content-Type': 'application/json'
}

print("=" * 70)
print("📱 OBTENIENDO CONTACTOS - BARBERÍA CHURCO")
print("=" * 70)

# Método 1: Intentar obtener todos los contactos
print("\n1️⃣ Intentando obtener contactos...")
try:
    url = f"{BASE_URL}/chat/fetchAllContacts/{INSTANCE}"
    print(f"URL: {url}")
    
    response = requests.get(url, headers=HEADERS, timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Respuesta exitosa!")
        print(f"Tipo: {type(data)}")
        
        if isinstance(data, list):
            print(f"Total de contactos: {len(data)}")
            
            # Filtrar solo números personales
            contactos_personales = [
                c for c in data 
                if isinstance(c, dict) and '@s.whatsapp.net' in c.get('id', '')
            ]
            
            print(f"Contactos personales: {len(contactos_personales)}")
            
            # Mostrar primeros 50
            print("\n📋 Primeros 50 contactos:")
            print("=" * 70)
            
            for i, contacto in enumerate(contactos_personales[:50], 1):
                contact_id = contacto.get('id', '')
                telefono = contact_id.replace('@s.whatsapp.net', '')
                nombre = contacto.get('name', contacto.get('pushName', 'Sin nombre'))
                
                print(f"{i}. {telefono} - {nombre}")
            
            # Lista de números
            print("\n📋 SOLO NÚMEROS (primeros 50):")
            print("=" * 70)
            numeros = [
                c.get('id', '').replace('@s.whatsapp.net', '') 
                for c in contactos_personales[:50]
            ]
            print(", ".join(numeros))
            
        else:
            print(f"Estructura: {json.dumps(data, indent=2)[:500]}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Método 2: Intentar con Google Sheets (clientes que ya agendaron)
print("\n\n2️⃣ Alternativa: Obtener clientes desde Google Sheets...")
try:
    from services import SheetsClient
    
    sheets = SheetsClient()
    
    # Leer todos los clientes
    clientes_data = sheets._read_range("clientes!A2:C")
    
    if clientes_data:
        print(f"✅ Clientes en Google Sheets: {len(clientes_data)}")
        print("\n📋 Clientes registrados:")
        print("=" * 70)
        
        for i, row in enumerate(clientes_data[:50], 1):
            if len(row) >= 3:
                cliente_id = row[0]
                nombre = row[1]
                telefono = row[2]
                print(f"{i}. {telefono} - {nombre}")
        
        # Lista de números
        print("\n📋 SOLO NÚMEROS (primeros 50):")
        print("=" * 70)
        numeros = [row[2] for row in clientes_data[:50] if len(row) >= 3]
        print(", ".join(numeros))
        
except Exception as e:
    print(f"❌ Error accediendo a Google Sheets: {e}")
    print("   (Esto es normal si las credenciales de Google no están configuradas)")

print("\n" + "=" * 70)
print("✅ Proceso completado")
print()
