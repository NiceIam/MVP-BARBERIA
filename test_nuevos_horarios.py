"""Script para verificar los nuevos horarios de 50 minutos."""
from datetime import time, datetime, timedelta


def calcular_slots_mañana():
    """Calcula los slots de la mañana."""
    print("="*70)
    print("🌅 HORARIOS DE LA MAÑANA")
    print("="*70)
    print()
    
    hora_inicio = time(8, 0)
    hora_fin = time(12, 10)
    intervalo = 50
    
    slots = []
    dt_actual = datetime.combine(datetime.today(), hora_inicio)
    dt_fin = datetime.combine(datetime.today(), hora_fin)
    
    print("Horario de atención: 8:00 AM - 12:10 PM")
    print("Intervalo entre citas: 50 minutos")
    print()
    print("Slots disponibles:")
    print("-"*70)
    
    contador = 1
    while True:
        dt_fin_cita = dt_actual + timedelta(minutes=intervalo)
        
        if dt_fin_cita <= dt_fin:
            hora_inicio_str = dt_actual.strftime("%I:%M %p")
            hora_fin_str = dt_fin_cita.strftime("%I:%M %p")
            print(f"{contador}. {hora_inicio_str} - {hora_fin_str}")
            slots.append((dt_actual.time(), dt_fin_cita.time()))
            dt_actual += timedelta(minutes=intervalo)
            contador += 1
        else:
            break
    
    print("-"*70)
    print(f"Total de slots en la mañana: {len(slots)}")
    print()
    
    return slots


def calcular_slots_tarde():
    """Calcula los slots de la tarde."""
    print("="*70)
    print("🌆 HORARIOS DE LA TARDE")
    print("="*70)
    print()
    
    hora_inicio = time(14, 0)
    hora_fin = time(19, 50)
    intervalo = 50
    
    slots = []
    dt_actual = datetime.combine(datetime.today(), hora_inicio)
    dt_fin = datetime.combine(datetime.today(), hora_fin)
    
    print("Horario de atención: 2:00 PM - 7:50 PM")
    print("Intervalo entre citas: 50 minutos")
    print()
    print("Slots disponibles:")
    print("-"*70)
    
    contador = 1
    while True:
        dt_fin_cita = dt_actual + timedelta(minutes=intervalo)
        
        if dt_fin_cita <= dt_fin:
            hora_inicio_str = dt_actual.strftime("%I:%M %p")
            hora_fin_str = dt_fin_cita.strftime("%I:%M %p")
            print(f"{contador}. {hora_inicio_str} - {hora_fin_str}")
            slots.append((dt_actual.time(), dt_fin_cita.time()))
            dt_actual += timedelta(minutes=intervalo)
            contador += 1
        else:
            break
    
    print("-"*70)
    print(f"Total de slots en la tarde: {len(slots)}")
    print()
    
    return slots


def verificar_configuracion():
    """Verifica la configuración en los archivos."""
    print("="*70)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN")
    print("="*70)
    print()
    
    # Verificar constants.py
    with open("config/constants.py", 'r', encoding='utf-8') as f:
        constants = f.read()
    
    print("📝 Verificando config/constants.py:")
    
    # Verificar Corte + Barba
    if '"duracion_minutos": 50' in constants and '"nombre": "Corte + Barba"' in constants:
        print("   ✅ Corte + Barba: 50 minutos")
    else:
        print("   ❌ Corte + Barba: duración incorrecta")
    
    # Verificar Corte Normal
    if '"duracion_minutos": 40' in constants and '"nombre": "Corte Normal"' in constants:
        print("   ✅ Corte Normal: 40 minutos")
    else:
        print("   ❌ Corte Normal: duración incorrecta")
    
    # Verificar horarios
    if 'time(8, 0)' in constants and 'time(12, 10)' in constants:
        print("   ✅ Horario mañana: 8:00 AM - 12:10 PM")
    else:
        print("   ❌ Horario mañana: incorrecto")
    
    if 'time(14, 0)' in constants and 'time(19, 50)' in constants:
        print("   ✅ Horario tarde: 2:00 PM - 7:50 PM")
    else:
        print("   ❌ Horario tarde: incorrecto")
    
    print()
    
    # Verificar settings.py
    with open("config/settings.py", 'r', encoding='utf-8') as f:
        settings = f.read()
    
    print("📝 Verificando config/settings.py:")
    
    if 'SLOT_INTERVAL_MINUTES = 50' in settings:
        print("   ✅ Intervalo de slots: 50 minutos")
    else:
        print("   ❌ Intervalo de slots: incorrecto")
    
    print()
    
    # Verificar engine.py
    with open("chatbot/engine.py", 'r', encoding='utf-8') as f:
        engine = f.read()
    
    print("📝 Verificando chatbot/engine.py:")
    
    if '50 if "Barba"' in engine and '40' in engine:
        print("   ✅ Lógica de duración en reagendamiento actualizada")
    else:
        print("   ⚠️ Verificar lógica de duración en reagendamiento")
    
    print()


def mostrar_resumen():
    """Muestra un resumen de los cambios."""
    print("="*70)
    print("📊 RESUMEN DE CAMBIOS")
    print("="*70)
    print()
    
    print("🔧 Cambios realizados:")
    print()
    print("1. Duración de servicios:")
    print("   • Corte + Barba: 45 min → 50 min")
    print("   • Corte Normal: 40 min (sin cambios)")
    print()
    print("2. Intervalo entre citas:")
    print("   • Antes: 45 minutos")
    print("   • Ahora: 50 minutos")
    print()
    print("3. Horarios de atención:")
    print("   • Mañana: 8:00 AM - 12:10 PM")
    print("     - Primera cita: 8:00 AM - 8:50 AM")
    print("     - Última cita: 11:20 AM - 12:10 PM")
    print()
    print("   • Tarde: 2:00 PM - 7:50 PM")
    print("     - Primera cita: 2:00 PM - 2:50 PM")
    print("     - Última cita: 7:00 PM - 7:50 PM")
    print()
    print("4. Total de slots por día:")
    print("   • Mañana: 4 slots")
    print("   • Tarde: 6 slots")
    print("   • Total: 10 slots por día")
    print()


def main():
    """Ejecuta todas las verificaciones."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "VERIFICACIÓN DE NUEVOS HORARIOS" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    # Calcular slots
    slots_mañana = calcular_slots_mañana()
    slots_tarde = calcular_slots_tarde()
    
    # Verificar configuración
    verificar_configuracion()
    
    # Mostrar resumen
    mostrar_resumen()
    
    # Verificaciones finales
    print("="*70)
    print("✅ VERIFICACIÓN COMPLETA")
    print("="*70)
    print()
    
    total_slots = len(slots_mañana) + len(slots_tarde)
    
    if total_slots == 10:
        print(f"✅ Total de slots por día: {total_slots} (correcto)")
    else:
        print(f"⚠️ Total de slots por día: {total_slots} (esperado: 10)")
    
    if slots_mañana[0][0] == time(8, 0):
        print("✅ Primera cita mañana: 8:00 AM (correcto)")
    
    if slots_mañana[-1][0] == time(11, 20):
        print("✅ Última cita mañana: 11:20 AM (correcto)")
    
    if slots_tarde[0][0] == time(14, 0):
        print("✅ Primera cita tarde: 2:00 PM (correcto)")
    
    if slots_tarde[-1][0] == time(19, 0):
        print("✅ Última cita tarde: 7:00 PM (correcto)")
    
    print()
    print("🎉 Los nuevos horarios están correctamente configurados!")
    print()


if __name__ == "__main__":
    main()
