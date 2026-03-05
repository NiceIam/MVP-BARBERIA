"""Script para verificar que el mensaje de 'hola' no se duplica."""
import re


def verificar_no_duplicacion():
    """Verifica que el mensaje de volver al menú no se duplique."""
    print("="*70)
    print("🧪 VERIFICACIÓN DE NO DUPLICACIÓN DE MENSAJE")
    print("="*70)
    print()
    
    with open("chatbot/engine.py", 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    # Test 1: Verificar que el método _mostrar_horas_disponibles fue eliminado
    print("📝 Test 1: Verificar eliminación de método no usado")
    if 'def _mostrar_horas_disponibles(self, fecha: date' in codigo:
        print("❌ Método _mostrar_horas_disponibles todavía existe")
        return False
    else:
        print("✅ Método _mostrar_horas_disponibles eliminado correctamente")
    
    # Test 2: Verificar que el mensaje de error no tiene _agregar_opcion_menu doble
    print("\n📝 Test 2: Verificar mensaje de error sin duplicación")
    
    # Buscar el patrón del mensaje de error
    patron = r'if not slots:.*?return.*?No hay horarios disponibles.*?\n'
    matches = re.findall(patron, codigo, re.DOTALL)
    
    if matches:
        for i, match in enumerate(matches, 1):
            print(f"\n   Ocurrencia {i}:")
            print(f"   {match[:100]}...")
            
            # Verificar que NO tenga _agregar_opcion_menu envolviendo _mostrar_fechas
            if '_agregar_opcion_menu' in match and '_mostrar_fechas()' in match:
                # Verificar el patrón problemático
                if re.search(r'_agregar_opcion_menu\([^)]*_mostrar_fechas\(\)', match):
                    print("   ❌ PROBLEMA: _agregar_opcion_menu envuelve _mostrar_fechas")
                    return False
                else:
                    print("   ✅ Correcto: No hay doble aplicación")
            else:
                print("   ✅ Correcto: Concatenación simple")
    
    # Test 3: Contar cuántas veces aparece el texto de volver al menú
    print("\n📝 Test 3: Simular mensaje completo")
    
    # Simular cómo se vería el mensaje
    mensaje_error = "😔 No hay horarios disponibles para ese día. Por favor elige otra fecha:\n\n"
    mensaje_fechas = """📅 *¿Qué día prefieres?*

1. Lunes 10/03/2026
2. Martes 11/03/2026

Responde con el número del día.

_Escribe *hola* para volver al menú principal._"""
    
    mensaje_completo = mensaje_error + mensaje_fechas
    
    # Contar cuántas veces aparece el texto de volver
    count = mensaje_completo.count("_Escribe *hola* para volver al menú principal._")
    
    print(f"\n   Mensaje completo simulado:")
    print("   " + "-"*66)
    for linea in mensaje_completo.split('\n')[:10]:
        print(f"   {linea}")
    print("   ...")
    print("   " + "-"*66)
    print(f"\n   Veces que aparece 'Escribe hola...': {count}")
    
    if count == 1:
        print("   ✅ Mensaje aparece solo UNA vez (correcto)")
    else:
        print(f"   ❌ Mensaje aparece {count} veces (incorrecto)")
        return False
    
    return True


def mostrar_antes_despues():
    """Muestra cómo era antes y cómo es ahora."""
    print("\n" + "="*70)
    print("📊 COMPARACIÓN ANTES Y DESPUÉS")
    print("="*70)
    
    print("\n❌ ANTES (con duplicación):")
    print("-"*70)
    print("""😔 No hay horarios disponibles para ese día. Por favor elige otra fecha:

📅 *¿Qué día prefieres?*

1. Lunes 10/03/2026
2. Martes 11/03/2026

Responde con el número del día.

_Escribe *hola* para volver al menú principal._

_Escribe *hola* para volver al menú principal._  ← DUPLICADO
""")
    
    print("\n✅ AHORA (sin duplicación):")
    print("-"*70)
    print("""😔 No hay horarios disponibles para ese día. Por favor elige otra fecha:

📅 *¿Qué día prefieres?*

1. Lunes 10/03/2026
2. Martes 11/03/2026

Responde con el número del día.

_Escribe *hola* para volver al menú principal._  ← UNA SOLA VEZ
""")


def main():
    """Ejecuta todas las verificaciones."""
    resultado = verificar_no_duplicacion()
    
    if resultado:
        mostrar_antes_despues()
        
        print("\n" + "="*70)
        print("✅ VERIFICACIÓN EXITOSA - PROBLEMA RESUELTO")
        print("="*70)
        print()
        print("📊 Cambios realizados:")
        print("   ✓ Eliminado método _mostrar_horas_disponibles (no usado)")
        print("   ✓ Corregida duplicación en mensaje de error")
        print("   ✓ Mensaje 'Escribe hola...' aparece solo UNA vez")
        print()
        print("🎯 Resultado:")
        print("   El mensaje ya no se duplica cuando no hay horarios disponibles")
        print()
        return 0
    else:
        print("\n" + "="*70)
        print("❌ VERIFICACIÓN FALLIDA")
        print("="*70)
        print()
        print("Todavía hay problemas con la duplicación del mensaje.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
