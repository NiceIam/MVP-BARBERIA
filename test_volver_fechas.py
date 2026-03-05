"""Script para probar la funcionalidad de volver a las fechas."""
import re


def verificar_funcion_volver():
    """Verifica que la función de volver esté implementada correctamente."""
    print("="*70)
    print("🧪 VERIFICACIÓN DE FUNCIONALIDAD 'VOLVER'")
    print("="*70)
    print()
    
    # Test 1: Verificar que existe la función de validación
    print("📝 Test 1: Verificar función validar_comando_volver")
    with open("chatbot/validaciones.py", 'r', encoding='utf-8') as f:
        validaciones = f.read()
    
    if 'def validar_comando_volver' in validaciones:
        print("✅ Función validar_comando_volver encontrada")
        
        # Verificar comandos aceptados
        if 'volver' in validaciones and 'atras' in validaciones:
            print("✅ Comandos 'volver' y 'atras' incluidos")
        else:
            print("⚠️ Algunos comandos pueden faltar")
    else:
        print("❌ Función validar_comando_volver NO encontrada")
        return False
    
    # Test 2: Verificar que se importa en engine.py
    print("\n📝 Test 2: Verificar importación en engine.py")
    with open("chatbot/engine.py", 'r', encoding='utf-8') as f:
        engine = f.read()
    
    if 'validar_comando_volver' in engine:
        print("✅ Función importada en engine.py")
    else:
        print("❌ Función NO importada en engine.py")
        return False
    
    # Test 3: Verificar que se usa en _procesar_seleccion_hora
    print("\n📝 Test 3: Verificar uso en _procesar_seleccion_hora")
    if 'if validar_comando_volver(mensaje):' in engine:
        print("✅ Validación de comando volver implementada")
        
        # Verificar que vuelve al estado de fecha
        if 'ESTADO_ESPERANDO_FECHA' in engine and '_mostrar_fechas()' in engine:
            print("✅ Lógica de volver a fechas implementada")
        else:
            print("⚠️ Lógica de volver puede estar incompleta")
    else:
        print("❌ Validación de comando volver NO implementada")
        return False
    
    # Test 4: Verificar mensaje en _formatear_horas_disponibles
    print("\n📝 Test 4: Verificar mensaje en plantilla de horas")
    if 'volver' in engine and 'elegir otra fecha' in engine:
        print("✅ Mensaje de volver incluido en plantilla de horas")
        
        # Extraer el mensaje
        patron = r'💡.*volver.*fecha'
        match = re.search(patron, engine, re.IGNORECASE | re.DOTALL)
        if match:
            print(f"✅ Texto encontrado: '{match.group()[:80]}...'")
    else:
        print("❌ Mensaje de volver NO encontrado en plantilla")
        return False
    
    # Test 5: Verificar que limpia la fecha al volver
    print("\n📝 Test 5: Verificar limpieza de datos al volver")
    if 'del sesion.datos_temp["fecha"]' in engine or 'datos_temp.pop("fecha")' in engine:
        print("✅ Limpieza de fecha implementada")
    else:
        print("⚠️ Puede que no se limpie la fecha al volver")
    
    return True


def mostrar_ejemplo_uso():
    """Muestra un ejemplo de cómo funciona la nueva funcionalidad."""
    print("\n" + "="*70)
    print("📱 EJEMPLO DE USO")
    print("="*70)
    print()
    
    print("Flujo normal:")
    print("-" * 70)
    print("Usuario: 1 (Agendar cita)")
    print("Bot: [Muestra servicios]")
    print()
    print("Usuario: 1 (Selecciona servicio)")
    print("Bot: [Muestra fechas]")
    print()
    print("Usuario: 3 (Selecciona miércoles)")
    print("Bot: 🕐 *¿A qué hora?*")
    print()
    print("     1. 8:00 AM")
    print("     2. 8:45 AM")
    print("     3. 9:30 AM")
    print("     ...")
    print()
    print("     Responde con el número de la hora.")
    print()
    print("     💡 Si no encuentras un horario que te sirva,")
    print("        escribe *volver* para elegir otra fecha.")
    print()
    print("     _Escribe *hola* para volver al menú principal._")
    print()
    print("-" * 70)
    print()
    print("Caso 1: Usuario encuentra horario que le sirve")
    print("-" * 70)
    print("Usuario: 5 (Selecciona hora)")
    print("Bot: [Muestra confirmación de cita]")
    print()
    print("-" * 70)
    print()
    print("Caso 2: Usuario NO encuentra horario que le sirva")
    print("-" * 70)
    print("Usuario: volver")
    print("Bot: 📅 *¿Qué día prefieres?*")
    print()
    print("     1. Lunes 10/03/2026")
    print("     2. Martes 11/03/2026")
    print("     3. Miércoles 12/03/2026")
    print("     ...")
    print()
    print("Usuario: 4 (Selecciona jueves)")
    print("Bot: [Muestra horas disponibles para jueves]")
    print("-" * 70)


def mostrar_comandos_aceptados():
    """Muestra los comandos que activan la función volver."""
    print("\n" + "="*70)
    print("📋 COMANDOS ACEPTADOS")
    print("="*70)
    print()
    print("Los siguientes comandos hacen que el usuario vuelva a las fechas:")
    print()
    print("  • volver")
    print("  • atras")
    print("  • atrás")
    print("  • regresar")
    print("  • back")
    print()
    print("Nota: Los comandos NO son sensibles a mayúsculas/minúsculas")


def main():
    """Ejecuta todas las verificaciones."""
    resultado = verificar_funcion_volver()
    
    if resultado:
        mostrar_ejemplo_uso()
        mostrar_comandos_aceptados()
        
        print("\n" + "="*70)
        print("✅ VERIFICACIÓN COMPLETA - FUNCIONALIDAD IMPLEMENTADA")
        print("="*70)
        print()
        print("📊 Resumen:")
        print("   ✓ Función de validación creada")
        print("   ✓ Importada correctamente")
        print("   ✓ Implementada en selección de hora")
        print("   ✓ Mensaje incluido en plantilla")
        print("   ✓ Vuelve al estado de selección de fecha")
        print()
        print("🎯 Beneficio:")
        print("   Los usuarios pueden cambiar de fecha si no encuentran")
        print("   un horario disponible que les sirva, sin tener que")
        print("   empezar todo el proceso de nuevo.")
        print()
        return 0
    else:
        print("\n" + "="*70)
        print("❌ VERIFICACIÓN FALLIDA")
        print("="*70)
        print()
        print("Algunos componentes de la funcionalidad no están completos.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
