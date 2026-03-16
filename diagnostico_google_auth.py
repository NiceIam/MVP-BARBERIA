"""Script de diagnóstico para problemas de autenticación de Google."""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 70)
print("🔍 DIAGNÓSTICO DE AUTENTICACIÓN DE GOOGLE")
print("=" * 70)

# 1. Verificar variables de entorno
print("\n1️⃣ Variables de Entorno:")
print("-" * 70)

service_account_env = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
sheets_id = os.getenv('GOOGLE_SHEETS_ID')
calendar_id = os.getenv('GOOGLE_CALENDAR_ID')

print(f"GOOGLE_SERVICE_ACCOUNT_FILE: {'✅ Configurada' if service_account_env else '❌ NO configurada'}")
print(f"GOOGLE_SHEETS_ID: {'✅ ' + sheets_id if sheets_id else '❌ NO configurada'}")
print(f"GOOGLE_CALENDAR_ID: {'✅ ' + calendar_id if calendar_id else '❌ NO configurada'}")

# 2. Verificar tipo de credencial
print("\n2️⃣ Tipo de Credencial:")
print("-" * 70)

if service_account_env:
    if service_account_env.startswith('{'):
        print("📄 Tipo: JSON en variable de entorno")
        try:
            creds = json.loads(service_account_env)
            print(f"✅ JSON válido")
            print(f"   - type: {creds.get('type', 'N/A')}")
            print(f"   - project_id: {creds.get('project_id', 'N/A')}")
            print(f"   - client_email: {creds.get('client_email', 'N/A')}")
            print(f"   - private_key_id: {creds.get('private_key_id', 'N/A')[:20]}...")
            
            # Verificar campos requeridos
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
            missing = [f for f in required_fields if f not in creds]
            if missing:
                print(f"❌ Campos faltantes: {', '.join(missing)}")
            else:
                print("✅ Todos los campos requeridos presentes")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON inválido: {e}")
    else:
        print("📁 Tipo: Path a archivo")
        file_path = Path(service_account_env)
        if file_path.exists():
            print(f"✅ Archivo existe: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    creds = json.load(f)
                print(f"✅ JSON válido en archivo")
                print(f"   - type: {creds.get('type', 'N/A')}")
                print(f"   - project_id: {creds.get('project_id', 'N/A')}")
                print(f"   - client_email: {creds.get('client_email', 'N/A')}")
            except Exception as e:
                print(f"❌ Error leyendo archivo: {e}")
        else:
            print(f"❌ Archivo NO existe: {file_path}")
else:
    print("❌ Variable GOOGLE_SERVICE_ACCOUNT_FILE no configurada")

# 3. Intentar autenticar
print("\n3️⃣ Prueba de Autenticación:")
print("-" * 70)

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/calendar'  # Scope completo para lectura y escritura
    ]
    
    if service_account_env and service_account_env.startswith('{'):
        creds_info = json.loads(service_account_env)
        credentials = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=SCOPES
        )
        print("✅ Credenciales creadas desde variable de entorno")
    else:
        file_path = Path(service_account_env) if service_account_env else Path('service_account.json')
        credentials = service_account.Credentials.from_service_account_file(
            str(file_path),
            scopes=SCOPES
        )
        print("✅ Credenciales creadas desde archivo")
    
    # Intentar conectar a Sheets
    print("\n   Probando Google Sheets API...")
    sheets_service = build('sheets', 'v4', credentials=credentials)
    
    # Intentar leer metadata del spreadsheet
    if sheets_id:
        result = sheets_service.spreadsheets().get(spreadsheetId=sheets_id).execute()
        print(f"   ✅ Conexión exitosa a Google Sheets")
        print(f"   📊 Spreadsheet: {result.get('properties', {}).get('title', 'N/A')}")
    else:
        print("   ⚠️ No se puede probar sin GOOGLE_SHEETS_ID")
    
    # Intentar conectar a Calendar
    print("\n   Probando Google Calendar API...")
    calendar_service = build('calendar', 'v3', credentials=credentials)
    
    if calendar_id:
        calendar = calendar_service.calendars().get(calendarId=calendar_id).execute()
        print(f"   ✅ Conexión exitosa a Google Calendar")
        print(f"   📅 Calendar: {calendar.get('summary', 'N/A')}")
    else:
        print("   ⚠️ No se puede probar sin GOOGLE_CALENDAR_ID")
    
    print("\n" + "=" * 70)
    print("✅ DIAGNÓSTICO EXITOSO - Credenciales funcionan correctamente")
    print("=" * 70)
    
except FileNotFoundError as e:
    print(f"\n❌ ERROR: Archivo no encontrado")
    print(f"   {e}")
    print("\n💡 SOLUCIÓN:")
    print("   1. Descarga el archivo service_account.json de Google Cloud Console")
    print("   2. Colócalo en la raíz del proyecto")
    print("   3. O configura GOOGLE_SERVICE_ACCOUNT_FILE con el JSON completo")
    
except json.JSONDecodeError as e:
    print(f"\n❌ ERROR: JSON inválido")
    print(f"   {e}")
    print("\n💡 SOLUCIÓN:")
    print("   Verifica que el JSON en GOOGLE_SERVICE_ACCOUNT_FILE esté bien formateado")
    
except Exception as e:
    error_str = str(e)
    print(f"\n❌ ERROR DE AUTENTICACIÓN: {error_str}")
    
    if 'invalid_grant' in error_str:
        print("\n🔴 PROBLEMA IDENTIFICADO: Credenciales inválidas o expiradas")
        print("\n💡 SOLUCIONES POSIBLES:")
        print("   1. La cuenta de servicio fue eliminada o deshabilitada")
        print("   2. Las credenciales son de un proyecto diferente")
        print("   3. El archivo service_account.json está corrupto")
        print("   4. La cuenta de servicio no tiene permisos")
        print("\n📋 PASOS PARA RESOLVER:")
        print("   1. Ve a Google Cloud Console: https://console.cloud.google.com")
        print("   2. Selecciona tu proyecto")
        print("   3. Ve a 'IAM & Admin' > 'Service Accounts'")
        print("   4. Verifica que la cuenta de servicio existe y está activa")
        print("   5. Si no existe, crea una nueva:")
        print("      - Nombre: barberia-churco-bot")
        print("      - Roles: Editor (o permisos específicos)")
        print("   6. Genera una nueva clave JSON")
        print("   7. Descarga el archivo y actualiza tu configuración")
        print("\n   8. IMPORTANTE: Comparte el Google Sheet y Calendar con el email")
        print("      de la cuenta de servicio (client_email del JSON)")
        
    elif 'account not found' in error_str:
        print("\n🔴 PROBLEMA: La cuenta de servicio no existe")
        print("\n💡 SOLUCIÓN:")
        print("   Necesitas crear una nueva cuenta de servicio en Google Cloud")
        
    print("\n" + "=" * 70)

print("\n")
