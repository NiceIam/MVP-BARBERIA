"""Test rápido de las nuevas credenciales de Google."""
import os
import json
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🧪 TEST DE CREDENCIALES DE GOOGLE")
print("=" * 70)

# Verificar variables
service_account = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
sheets_id = os.getenv('GOOGLE_SHEETS_ID')
calendar_id = os.getenv('GOOGLE_CALENDAR_ID')

print("\n1️⃣ Variables de Entorno:")
print(f"   GOOGLE_SERVICE_ACCOUNT_FILE: {'✅ Configurada' if service_account else '❌ NO'}")
print(f"   GOOGLE_SHEETS_ID: {sheets_id if sheets_id else '❌ NO'}")
print(f"   GOOGLE_CALENDAR_ID: {calendar_id if calendar_id else '❌ NO'}")

if not all([service_account, sheets_id, calendar_id]):
    print("\n❌ Faltan variables de entorno")
    exit(1)

# Parsear JSON
print("\n2️⃣ Parseando Service Account JSON...")
try:
    creds_info = json.loads(service_account)
    print(f"   ✅ JSON válido")
    print(f"   Project: {creds_info.get('project_id')}")
    print(f"   Email: {creds_info.get('client_email')}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test Google Sheets
print("\n3️⃣ Probando Google Sheets API...")
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    credentials = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=SCOPES
    )
    
    service = build('sheets', 'v4', credentials=credentials)
    
    # Intentar leer metadata
    result = service.spreadsheets().get(spreadsheetId=sheets_id).execute()
    
    print(f"   ✅ Conexión exitosa!")
    print(f"   Spreadsheet: {result.get('properties', {}).get('title', 'N/A')}")
    
    # Intentar leer datos
    range_name = 'clientes!A1:C1'
    result = service.spreadsheets().values().get(
        spreadsheetId=sheets_id,
        range=range_name
    ).execute()
    
    print(f"   ✅ Lectura exitosa!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\n💡 Solución:")
    print("   1. Comparte el Google Sheet con:")
    print(f"      {creds_info.get('client_email')}")
    print("   2. Dale permisos de 'Editor'")

# Test Google Calendar
print("\n4️⃣ Probando Google Calendar API...")
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    # Usar scope más amplio que incluye lectura y escritura
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    credentials = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=SCOPES
    )
    
    service = build('calendar', 'v3', credentials=credentials)
    
    # Intentar leer el calendario
    calendar = service.calendars().get(calendarId=calendar_id).execute()
    
    print(f"   ✅ Conexión exitosa!")
    print(f"   Calendar: {calendar.get('summary', 'N/A')}")
    
    # Intentar listar eventos (prueba adicional)
    from datetime import datetime, timedelta
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=1,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    print(f"   ✅ Lectura de eventos exitosa!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\n💡 Solución:")
    print("   1. Comparte el Google Calendar con:")
    print(f"      {creds_info.get('client_email')}")
    print("   2. Dale permisos de 'Make changes to events'")
    print("   3. Verifica que Google Calendar API esté habilitada en:")
    print("      https://console.cloud.google.com/apis/library/calendar-json.googleapis.com")

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO")
print("=" * 70)
print()
