"""Test simple de servicios de Google."""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging simple
import logging
logging.basicConfig(level=logging.INFO, filename='test_output.log', filemode='w', encoding='utf-8')

print("=" * 70)
print("🧪 TEST SIMPLE DE SERVICIOS")
print("=" * 70)

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n1️⃣ Importando servicios...")
try:
    from services.google_sheets import SheetsClient
    from services.google_calendar import CalendarClient
    print("   ✅ Imports exitosos")
except Exception as e:
    print(f"   ❌ Error en imports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2️⃣ Inicializando SheetsClient...")
try:
    sheets = SheetsClient()
    print("   ✅ SheetsClient inicializado")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3️⃣ Inicializando CalendarClient...")
try:
    calendar = CalendarClient()
    print("   ✅ CalendarClient inicializado")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4️⃣ Probando conexión a Sheets...")
try:
    result = sheets.test_connection()
    if result:
        print("   ✅ Conexión exitosa")
    else:
        print("   ❌ Conexión fallida")
except Exception as e:
    print(f"   ❌ Error: {e}")

from datetime import datetime, date, time, timedelta
from models import Cita

print("\n5️⃣ Creando cita de prueba...")
try:
    manana = date.today() + timedelta(days=1)
    hora_inicio = time(10, 0)
    hora_fin = time(10, 50)
    
    cita_test = Cita(
        id="", # El ID se genera en crear_cita
        cliente_id="TEST_CLI",
        cliente_telefono="573001234567",
        cliente_nombre="Usuario Test",
        servicio_id="SERV_TEST",
        servicio_nombre="Corte de Prueba",
        precio=35000,
        fecha=manana,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        estado="confirmada"
    )
    
    if sheets.crear_cita(cita_test):
        print(f"   ✅ Cita guardada en Sheets con ID: {cita_test.id}")
        
        print("\n6️⃣ Agendando en Calendar...")
        event_id = calendar.crear_evento(
            cita_id=cita_test.id,
            cliente_nombre=cita_test.cliente_nombre,
            cliente_telefono=cita_test.cliente_telefono,
            servicio_nombre=cita_test.servicio_nombre,
            precio=cita_test.precio,
            fecha=cita_test.fecha,
            hora_inicio=cita_test.hora_inicio,
            hora_fin=cita_test.hora_fin,
            estado=cita_test.estado
        )
        if event_id:
            print(f"   ✅ Evento creado en Calendar con ID: {event_id}")
            
            # Buscar la cita para actualizarla con el event_id
            resultado_busqueda = sheets.get_cita_por_id(cita_test.id)
            if resultado_busqueda:
                cita_db, row_index = resultado_busqueda
                cita_db.calendar_event_id = event_id
                sheets.actualizar_cita(cita_db, row_index)
                print("   ✅ Cita actualizada en Sheets con event_id")
            else:
                print("   ❌ No se encontró la cita en Sheets para actualizar")
        else:
            print("   ❌ Error creando evento en Calendar")
    else:
        print("   ❌ Error guardando cita en Sheets")
        
except Exception as e:
    print(f"   ❌ Error en paso 5 o 6: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO")
print("=" * 70)
