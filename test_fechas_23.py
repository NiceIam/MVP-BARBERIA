import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import date, time, datetime, timedelta
import pytz

def main():
    from dotenv import load_dotenv
    load_dotenv()

    from utils.datetime_utils import get_fecha_actual, get_datetime_actual
    from utils.disponibilidad import obtener_slots_disponibles, generar_slots_dia
    from chatbot.engine import ChatbotEngine

    engine = ChatbotEngine()
    tz = pytz.timezone("America/Bogota")
    ahora = datetime.now(tz)

    print("=" * 60)
    print("DIAGNOSTICO DE SLOTS - Dias proximos")
    print("=" * 60)
    print(f"Hora actual Bogota: {ahora.strftime('%H:%M:%S')}")
    print(f"Fecha actual:       {get_fecha_actual()}")

    # Servicio "Corte" = 45 min (segun lo seleccionado en el bot)
    duracion = 45

    print(f"\nDuracion servicio: {duracion} min")
    print("\n--- Slots base del dia (sin ocupados) ---")
    slots_base = generar_slots_dia(duracion)
    for s in slots_base:
        print(f"  {s.strftime('%I:%M %p')}")

    # Revisar 16 y 17 de marzo
    fechas_a_diagnosticar = [
        date(2026, 3, 16),
        date(2026, 3, 17),
        date(2026, 3, 18),
    ]

    print("\n--- Citas activas en el sistema ---")
    todas_citas = engine.sheets.get_todas_citas_activas()
    print(f"Total citas activas: {len(todas_citas)}")
    for c in todas_citas:
        print(f"  {c.fecha} {c.hora_inicio}-{c.hora_fin} | {c.servicio_nombre} | {c.estado}")

    print("\n--- Analisis por fecha ---")
    for fecha in fechas_a_diagnosticar:
        dias_semana = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
        print(f"\n[{dias_semana[fecha.weekday()]} {fecha.strftime('%d/%m/%Y')}]")

        citas_dia = [c for c in todas_citas if c.fecha == fecha]
        print(f"  Citas ese dia: {len(citas_dia)}")
        for c in citas_dia:
            print(f"    - {c.hora_inicio}-{c.hora_fin} {c.servicio_nombre} ({c.estado})")

        eventos_dia = engine.calendar.get_eventos_dia(fecha)
        print(f"  Eventos en Calendar ese dia: {len(eventos_dia)}")
        for e in eventos_dia:
            start = e.get('start', {})
            print(f"    - {start.get('dateTime') or start.get('date')} | {e.get('summary','')}")

        slots = obtener_slots_disponibles(fecha, duracion, citas_dia, eventos_dia)
        print(f"  Slots disponibles: {len(slots)}")
        for s in slots:
            print(f"    {s.strftime('%I:%M %p')}")

if __name__ == '__main__':
    main()
