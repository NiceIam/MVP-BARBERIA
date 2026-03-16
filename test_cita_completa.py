"""Test completo: Crear cita en Sheets y agendar en Google Calendar."""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.cliente import Cliente
from models.cita import Cita
from services.google_sheets import SheetsClient
from services.google_calendar import CalendarClient

print("=" * 70)
print("🧪 TEST COMPLETO: CREAR CITA EN SHEETS Y CALENDAR")
print("=" * 70)

# Inicializar servicios
print("\n1️⃣ Inicializando servicios...")
try:
    sheets_service = SheetsClient()
    calendar_service = CalendarClient()
    print("   ✅ Servicios inicializados")
except Exception as e:
    print(f"   ❌ Error al inicializar servicios: {e}")
    sys.exit(1)

# Crear cliente de prueba
print("\n2️⃣ Creando cliente de prueba...")
cliente_test = Cliente(
    telefono="573123613840",  # Tu número de prueba
    nombre="Test Usuario",
    estado="activo"
)

try:
    # Verificar si el cliente ya existe
    cliente_existente = sheets_service.obtener_cliente("573123613840")
    if cliente_existente:
        print(f"   ℹ️  Cliente ya existe: {cliente_existente.nombre}")
        cliente_test = cliente_existente
    else:
        sheets_service.guardar_cliente(cliente_test)
        print(f"   ✅ Cliente creado: {cliente_test.nombre}")
except Exception as e:
    print(f"   ❌ Error al crear cliente: {e}")
    sys.exit(1)

# Crear cita de prueba (mañana a las 10:00 AM)
print("\n3️⃣ Creando cita de prueba...")
manana = datetime.now() + timedelta(days=1)
fecha_cita = manana.strftime("%d/%m/%Y")
hora_cita = "10:00"

cita_test = Cita(
    id_cita=f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    telefono_cliente=cliente_test.telefono,
    nombre_cliente=cliente_test.nombre,
    servicio="Corte + Barba",
    fecha=fecha_cita,
    hora=hora_cita,
    duracion_minutos=50,
    estado="confirmada"
)

print(f"   📅 Fecha: {fecha_cita}")
print(f"   🕐 Hora: {hora_cita}")
print(f"   ✂️  Servicio: {cita_test.servicio}")
print(f"   ⏱️  Duración: {cita_test.duracion_minutos} minutos")

# Guardar cita en Google Sheets
print("\n4️⃣ Guardando cita en Google Sheets...")
try:
    sheets_service.guardar_cita(cita_test)
    print(f"   ✅ Cita guardada en Sheets con ID: {cita_test.id_cita}")
except Exception as e:
    print(f"   ❌ Error al guardar en Sheets: {e}")
    sys.exit(1)

# Crear evento en Google Calendar
print("\n5️⃣ Creando evento en Google Calendar...")
try:
    event_id = calendar_service.crear_evento(cita_test)
    print(f"   ✅ Evento creado en Calendar con ID: {event_id}")
    
    # Actualizar la cita con el event_id
    cita_test.event_id = event_id
    sheets_service.actualizar_cita(cita_test)
    print(f"   ✅ Cita actualizada con event_id en Sheets")
except Exception as e:
    print(f"   ❌ Error al crear evento en Calendar: {e}")
    sys.exit(1)

# Verificar que la cita se guardó correctamente
print("\n6️⃣ Verificando cita guardada...")
try:
    cita_recuperada = sheets_service.obtener_cita(cita_test.id_cita)
    if cita_recuperada:
        print(f"   ✅ Cita recuperada de Sheets:")
        print(f"      - ID: {cita_recuperada.id_cita}")
        print(f"      - Cliente: {cita_recuperada.nombre_cliente}")
        print(f"      - Fecha: {cita_recuperada.fecha}")
        print(f"      - Hora: {cita_recuperada.hora}")
        print(f"      - Servicio: {cita_recuperada.servicio}")
        print(f"      - Event ID: {cita_recuperada.event_id}")
    else:
        print(f"   ❌ No se pudo recuperar la cita")
except Exception as e:
    print(f"   ❌ Error al verificar cita: {e}")

# Verificar evento en Calendar
print("\n7️⃣ Verificando evento en Google Calendar...")
try:
    evento = calendar_service.obtener_evento(event_id)
    if evento:
        print(f"   ✅ Evento recuperado de Calendar:")
        print(f"      - Título: {evento.get('summary')}")
        print(f"      - Inicio: {evento.get('start', {}).get('dateTime')}")
        print(f"      - Fin: {evento.get('end', {}).get('dateTime')}")
        print(f"      - Descripción: {evento.get('description', 'N/A')}")
    else:
        print(f"   ❌ No se pudo recuperar el evento")
except Exception as e:
    print(f"   ❌ Error al verificar evento: {e}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO EXITOSAMENTE")
print("=" * 70)
print("\n💡 Verifica:")
print(f"   1. Google Sheets: https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SHEETS_ID')}")
print(f"   2. Google Calendar: https://calendar.google.com")
print()
