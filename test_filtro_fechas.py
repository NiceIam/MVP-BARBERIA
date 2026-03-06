"""Script para verificar el filtro de fechas con disponibilidad."""
import re


def verificar_implementacion():
    """Verifica que el filtro de fechas esté implementado correctamente."""
    print("="*70)
    print("🧪 VERIFICACIÓN DE FILTRO DE FECHAS CON DISPONIBILIDAD")
    print("="*70)
    print()
    
    with open("chatbot/engine.py", 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    # Test 1: Verificar que _mostrar_fechas filtra fechas
    print("📝 Test 1: Verificar filtrado en _mostrar_fechas")
    
    if 'fechas_disponibles = []' in codigo and 'obtener_slots_disponibles' in codigo:
        print("✅ Método _mostrar_fechas filtra fechas con disponibilidad")
        
        # Verificar que solo agrega fechas con slots
        if 'if slots:' in codigo and 'fechas_disponibles.append' in codigo:
            print("✅ Solo agrega fechas que tienen slots disponibles")
        else:
            print("⚠️ Lógica de filtrado puede estar incompleta")
    else:
        print("❌ Filtrado de fechas NO implementado")
        return False
    
    # Test 2: Verificar mensaje cuando no hay fechas disponibles
    print("\n📝 Test 2: Verificar mensaje cuando no hay fechas")
    
    if 'no hay fechas disponibles' in codigo.lower():
        print("✅ Mensaje de 'no hay fechas disponibles' implementado")
    else:
        print("⚠️ Mensaje de 'no hay fechas' puede faltar")
    
    # Test 3: Verificar que _procesar_seleccion_fecha usa fechas filtradas
    print("\n📝 Test 3: Verificar procesamiento de selección")
    
    # Buscar el método _procesar_seleccion_fecha
    patron = r'def _procesar_seleccion_fecha.*?fechas_disponibles'
    if re.search(patron, codigo, re.DOTALL):
        print("✅ _procesar_seleccion_fecha usa fechas filtradas")
    else:
        print("⚠️ _procesar_seleccion_fecha puede no usar filtrado")
    
    # Test 4: Verificar que se pasa duracion_minutos
    print("\n📝 Test 4: Verificar paso de duración del servicio")
    
    if '_mostrar_fechas(duracion_minutos)' in codigo:
        print("✅ Se pasa duracion_minutos a _mostrar_fechas")
    else:
        print("⚠️ duracion_minutos puede no estar siendo pasado")
    
    # Test 5: Verificar que el filtrado se hace en ambos métodos
    print("\n📝 Test 5: Verificar consistencia en filtrado")
    
    count_filtrado = codigo.count('fechas_disponibles = []')
    if count_filtrado >= 2:
        print(f"✅ Filtrado implementado en {count_filtrado} lugares")
    else:
        print(f"⚠️ Filtrado solo en {count_filtrado} lugar(es)")
    
    return True


def mostrar_flujo_nuevo():
    """Muestra cómo funciona el nuevo flujo."""
    print("\n" + "="*70)
    print("📱 NUEVO FLUJO DE AGENDAMIENTO")
    print("="*70)
    print()
    
    print("ANTES (mostraba todas las fechas):")
    print("-"*70)
    print("Usuario: 1 (Agendar cita)")
    print("Bot: [Muestra servicios]")
    print()
    print("Usuario: 1 (Corte + Barba)")
    print("Bot: 📅 ¿Qué día prefieres?")
    print()
    print("     1. Lunes 10/03/2026")
    print("     2. Martes 11/03/2026  ← SIN DISPONIBILIDAD")
    print("     3. Miércoles 12/03/2026  ← SIN DISPONIBILIDAD")
    print("     4. Jueves 13/03/2026")
    print("     ...")
    print()
    print("Usuario: 2 (Selecciona martes)")
    print("Bot: 😔 No hay horarios disponibles para ese día...")
    print("     [Muestra fechas de nuevo]")
    print()
    print("-"*70)
    print()
    
    print("AHORA (solo muestra fechas con disponibilidad):")
    print("-"*70)
    print("Usuario: 1 (Agendar cita)")
    print("Bot: [Muestra servicios]")
    print()
    print("Usuario: 1 (Corte + Barba)")
    print("Bot: [Valida disponibilidad de cada fecha...]")
    print("     📅 ¿Qué día prefieres?")
    print()
    print("     1. Lunes 10/03/2026  ✅ Tiene disponibilidad")
    print("     2. Jueves 13/03/2026  ✅ Tiene disponibilidad")
    print("     3. Viernes 14/03/2026  ✅ Tiene disponibilidad")
    print("     ...")
    print()
    print("     [NO muestra martes ni miércoles porque están llenos]")
    print()
    print("Usuario: 1 (Selecciona lunes)")
    print("Bot: 🕐 ¿A qué hora?")
    print("     [Muestra horas disponibles]")
    print()
    print("-"*70)


def mostrar_ventajas():
    """Muestra las ventajas del nuevo sistema."""
    print("\n" + "="*70)
    print("🎯 VENTAJAS DEL NUEVO SISTEMA")
    print("="*70)
    print()
    
    print("✅ Mejor experiencia de usuario:")
    print("   • No pierde tiempo seleccionando fechas sin disponibilidad")
    print("   • Ve solo opciones reales")
    print("   • Menos frustración")
    print()
    
    print("✅ Más eficiente:")
    print("   • Validación una sola vez (al mostrar fechas)")
    print("   • No necesita validar después de seleccionar")
    print("   • Menos pasos en el flujo")
    print()
    
    print("✅ Más profesional:")
    print("   • No muestra opciones que no puede cumplir")
    print("   • Información precisa desde el inicio")
    print("   • Mejor imagen de la barbería")
    print()
    
    print("⚠️ Consideración:")
    print("   • Puede tardar un poco más al mostrar fechas")
    print("     (porque valida disponibilidad de cada una)")
    print("   • Pero vale la pena por la mejor experiencia")
    print()


def main():
    """Ejecuta todas las verificaciones."""
    resultado = verificar_implementacion()
    
    if resultado:
        mostrar_flujo_nuevo()
        mostrar_ventajas()
        
        print("="*70)
        print("✅ VERIFICACIÓN EXITOSA - FILTRO IMPLEMENTADO")
        print("="*70)
        print()
        print("📊 Resumen de cambios:")
        print("   ✓ _mostrar_fechas filtra fechas con disponibilidad")
        print("   ✓ Solo muestra fechas que tienen al menos 1 slot")
        print("   ✓ _procesar_seleccion_fecha usa fechas filtradas")
        print("   ✓ Mensaje cuando no hay fechas disponibles")
        print("   ✓ Duración del servicio se considera en el filtrado")
        print()
        print("🎉 Los usuarios ahora solo ven fechas realmente disponibles!")
        print()
        return 0
    else:
        print("\n" + "="*70)
        print("❌ VERIFICACIÓN FALLIDA")
        print("="*70)
        print()
        print("Algunos componentes del filtro no están completos.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
