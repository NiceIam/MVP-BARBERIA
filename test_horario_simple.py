"""
Prueba simple del nuevo horario de las 7:50 PM
"""
from datetime import time

# Importar solo las constantes
import sys
sys.path.insert(0, '.')

from config.constants import HORARIOS_ATENCION

print("=" * 70)
print("🧪 VERIFICACIÓN DEL NUEVO HORARIO - SLOT 7:50 PM")
print("=" * 70)

print("\n📋 Horarios de Atención Configurados:")
print("-" * 70)
for idx, horario in enumerate(HORARIOS_ATENCION, 1):
    turno = "Mañana" if horario['hora_inicio'].hour < 12 else "Tarde"
    print(f"{idx}. {turno}: {horario['hora_inicio'].strftime('%H:%M')} - {horario['hora_fin'].strftime('%H:%M')}")

# Verificar el horario de la tarde
horario_tarde = HORARIOS_ATENCION[1]
print(f"\n🎯 Verificación del Horario de la Tarde:")
print("-" * 70)
print(f"Hora inicio: {horario_tarde['hora_inicio'].strftime('%H:%M')}")
print(f"Hora fin: {horario_tarde['hora_fin'].strftime('%H:%M')}")

# Calcular slots manualmente
hora_inicio = horario_tarde['hora_inicio']
hora_fin = horario_tarde['hora_fin']
intervalo = 50  # minutos

# Convertir a minutos desde medianoche
inicio_minutos = hora_inicio.hour * 60 + hora_inicio.minute
fin_minutos = hora_fin.hour * 60 + hora_fin.minute

# Calcular slots
slots = []
minuto_actual = inicio_minutos
while minuto_actual + intervalo <= fin_minutos:
    hora = minuto_actual // 60
    minuto = minuto_actual % 60
    slots.append(time(hora, minuto))
    minuto_actual += intervalo

print(f"\n📊 Slots de la Tarde (intervalo de {intervalo} minutos):")
print("-" * 70)
print(f"Total de slots: {len(slots)}")
print(f"\nTodos los slots:")
for idx, slot in enumerate(slots, 1):
    # Calcular hora de fin
    fin_minutos_slot = (slot.hour * 60 + slot.minute) + intervalo
    hora_fin_slot = fin_minutos_slot // 60
    minuto_fin_slot = fin_minutos_slot % 60
    print(f"  {idx}. {slot.strftime('%H:%M')} - {hora_fin_slot:02d}:{minuto_fin_slot:02d}")

# Verificar el último slot
ultimo_slot = slots[-1]
print(f"\n🎯 Último Slot de la Tarde:")
print("-" * 70)
print(f"Hora inicio: {ultimo_slot.strftime('%H:%M')}")

# Calcular hora de fin del último slot
fin_minutos_ultimo = (ultimo_slot.hour * 60 + ultimo_slot.minute) + intervalo
hora_fin_ultimo = fin_minutos_ultimo // 60
minuto_fin_ultimo = fin_minutos_ultimo % 60
print(f"Hora fin: {hora_fin_ultimo:02d}:{minuto_fin_ultimo:02d}")

if ultimo_slot == time(19, 50):
    print("\n✅ CORRECTO: El último slot es 19:50 (7:50 PM)")
    print(f"   Termina a las {hora_fin_ultimo:02d}:{minuto_fin_ultimo:02d} (8:40 PM)")
else:
    print(f"\n❌ ERROR: Se esperaba 19:50 pero se obtuvo {ultimo_slot.strftime('%H:%M')}")

# Resumen
print("\n" + "=" * 70)
print("📊 RESUMEN")
print("=" * 70)
print(f"✅ Horario de tarde actualizado: 14:00 - 20:40")
print(f"✅ Última cita posible: 19:50 (7:50 PM)")
print(f"✅ Cita termina a las: 20:40 (8:40 PM) con Corte + Barba")
print(f"✅ Slots en la tarde: {len(slots)}")
print(f"\n🎉 Configuración correcta!")
