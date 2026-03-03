"""Script para probar la conexión con Google Calendar."""
from datetime import datetime, date, time, timedelta
from services import CalendarClient
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")

def test_calendar():
    """Prueba la conexión y creación de eventos en Calendar."""
    print("\n" + "="*50)
    print("PRUEBA DE GOOGLE CALENDAR")
    print("="*50 + "\n")
    
    # Inicializar cliente
    try:
        calendar = CalendarClient()
        print("✅ Cliente de Calendar inicializado")
    except Exception as e:
        print(f"❌ Error inicializando cliente: {e}")
        return
    
    # Probar conexión
    print("\n1. Probando conexión...")
    if calendar.test_connection():
        print("✅ Conexión exitosa")
    else:
        print("❌ Error de conexión")
        return
    
    # Intentar crear un evento de prueba
    print("\n2. Creando evento de prueba...")
    fecha_prueba = date.today() + timedelta(days=1)
    hora_inicio = time(10, 0)
    hora_fin = time(11, 0)
    
    event_id = calendar.crear_evento(
        cita_id="test_001",
        cliente_nombre="Cliente Prueba",
        cliente_telefono="573001234567",
        servicio_nombre="Corte Normal",
        precio=20000,
        fecha=fecha_prueba,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        estado="confirmada"
    )
    
    if event_id:
        print(f"✅ Evento creado exitosamente!")
        print(f"   Event ID: {event_id}")
        
        # Intentar eliminar el evento de prueba
        print("\n3. Eliminando evento de prueba...")
        if calendar.eliminar_evento(event_id):
            print("✅ Evento eliminado exitosamente")
        else:
            print("⚠️  No se pudo eliminar el evento (puede que necesites eliminarlo manualmente)")
    else:
        print("❌ No se pudo crear el evento")
        print("\nPosibles causas:")
        print("1. El calendario no está compartido con el Service Account")
        print("2. El Service Account no tiene permisos de escritura")
        print("3. El Calendar ID es incorrecto")
        print(f"\nCalendar ID configurado: {calendar.calendar_id}")
        print(f"Service Account email: {calendar.credentials.service_account_email}")
        print("\nSOLUCIÓN:")
        print(f"1. Ve a Google Calendar: https://calendar.google.com")
        print(f"2. Busca el calendario: {calendar.calendar_id}")
        print(f"3. Compártelo con: {calendar.credentials.service_account_email}")
        print(f"4. Dale permisos de 'Hacer cambios en los eventos'")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_calendar()
