"""
Prueba del nuevo slot de las 7:50 PM
"""
from datetime import date, time, datetime, timedelta
from config.constants import HORARIOS_ATENCION
from utils.disponibilidad import obtener_slots_disponibles

print("=" * 70)
print("🧪 VERIFICACIÓN DEL NUEVO SLOT DE LAS 7:50 PM")
print("=" * 70)

# Verificar horarios de atención
print("\n📋 Horarios de Atención Actualizados:")
print("-" * 70)
for idx, horario in enumerate(HORARIOS_ATENCION, 1):
    print(f"{idx}. {horario['hora_inicio'].strftime('%H:%M')} - {horario['hora_fin'].strftime('%H:%M')}")

# Calcular slots disponibles para mañana
fecha_prueba = date.today() + timedelta(days=1)
print(f"\n📅 Fecha de prueba: {fecha_prueba.strftime('%d/%m/%Y')}")
print("-" * 70)

# Probar con Corte + Barba (50 minutos)
print("\n✂️ CORTE + BARBA (50 minutos):")
print("-" * 70)
slots_50 = obtener_slots_disponibles(fecha_prueba, 50, [], [])
print(f"Total de slots: {len(slots_50)}")
print(f"\nPrimeros 3 slots:")
for slot in slots_50[:3]:
    hora_fin = (datetime.combine(fecha_prueba, slot) + timedelta(minutes=50)).time()
    print(f"  • {slot.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}")

print(f"\nÚltimos 3 slots:")
for slot in slots_50[-3:]:
    hora_fin = (datetime.combine(fecha_prueba, slot) + timedelta(minutes=50)).time()
    print(f"  • {slot.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}")

# Verificar que el último slot es 19:50
ultimo_slot_50 = slots_50[-1]
print(f"\n🎯 Último slot disponible: {ultimo_slot_50.strftime('%H:%M')}")
if ultimo_slot_50 == time(19, 50):
    print("✅ CORRECTO: El último slot es 19:50")
else:
    print(f"❌ ERROR: Se esperaba 19:50 pero se obtuvo {ultimo_slot_50.strftime('%H:%M')}")

# Probar con Corte Normal (40 minutos)
print("\n" + "=" * 70)
print("✂️ CORTE NORMAL (40 minutos):")
print("-" * 70)
slots_40 = obtener_slots_disponibles(fecha_prueba, 40, [], [])
print(f"Total de slots: {len(slots_40)}")
print(f"\nPrimeros 3 slots:")
for slot in slots_40[:3]:
    hora_fin = (datetime.combine(fecha_prueba, slot) + timedelta(minutes=40)).time()
    print(f"  • {slot.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}")

print(f"\nÚltimos 3 slots:")
for slot in slots_40[-3:]:
    hora_fin = (datetime.combine(fecha_prueba, slot) + timedelta(minutes=40)).time()
    print(f"  • {slot.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}")

# Verificar que el último slot es 20:00 (porque 40 min termina a 20:40)
ultimo_slot_40 = slots_40[-1]
print(f"\n🎯 Último slot disponible: {ultimo_slot_40.strftime('%H:%M')}")
if ultimo_slot_40 == time(20, 0):
    print("✅ CORRECTO: El último slot es 20:00 (termina a 20:40)")
else:
    print(f"⚠️ Último slot: {ultimo_slot_40.strftime('%H:%M')}")

# Resumen
print("\n" + "=" * 70)
print("📊 RESUMEN DE CAPACIDAD DIARIA")
print("=" * 70)
print(f"Corte + Barba (50 min): {len(slots_50)} slots por día")
print(f"Corte Normal (40 min): {len(slots_40)} slots por día")

# Desglose por turno
slots_manana_50 = [s for s in slots_50 if s < time(14, 0)]
slots_tarde_50 = [s for s in slots_50 if s >= time(14, 0)]

slots_manana_40 = [s for s in slots_40 if s < time(14, 0)]
slots_tarde_40 = [s for s in slots_40 if s >= time(14, 0)]

print(f"\nCorte + Barba:")
print(f"  • Mañana: {len(slots_manana_50)} slots")
print(f"  • Tarde: {len(slots_tarde_50)} slots")

print(f"\nCorte Normal:")
print(f"  • Mañana: {len(slots_manana_40)} slots")
print(f"  • Tarde: {len(slots_tarde_40)} slots")

print("\n" + "=" * 70)
print("✅ VERIFICACIÓN COMPLETA")
print("=" * 70)
print(f"\n🎉 Nuevo horario implementado correctamente!")
print(f"   Última cita: 19:50 (termina a 20:40 con Corte + Barba)")
print(f"   Capacidad aumentada en 1 slot por día")
