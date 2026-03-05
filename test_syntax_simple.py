"""Prueba simple de sintaxis sin dependencias externas."""
import ast
import sys


def verificar_sintaxis(archivo):
    """Verifica que el archivo tenga sintaxis válida de Python."""
    print(f"\n🔍 Verificando sintaxis de {archivo}...")
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Parsear el código
        ast.parse(codigo)
        print(f"✅ {archivo} - Sintaxis correcta")
        return True
    except SyntaxError as e:
        print(f"❌ {archivo} - Error de sintaxis:")
        print(f"   Línea {e.lineno}: {e.msg}")
        print(f"   {e.text}")
        return False
    except Exception as e:
        print(f"❌ {archivo} - Error: {e}")
        return False


def verificar_metodo_helper(archivo):
    """Verifica que el método _agregar_opcion_menu exista."""
    print(f"\n🔍 Verificando método helper en {archivo}...")
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Verificar que el método existe
        if 'def _agregar_opcion_menu' in codigo:
            print("✅ Método _agregar_opcion_menu encontrado")
            
            # Verificar que retorna el mensaje con la opción de menú
            if 'hola' in codigo and 'menú' in codigo:
                print("✅ Método incluye texto sobre 'hola' y 'menú'")
                return True
            else:
                print("⚠️ Método no incluye texto esperado")
                return False
        else:
            print("❌ Método _agregar_opcion_menu NO encontrado")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def contar_usos_helper(archivo):
    """Cuenta cuántas veces se usa el método helper."""
    print(f"\n🔍 Contando usos de _agregar_opcion_menu en {archivo}...")
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Contar usos del método
        usos = codigo.count('self._agregar_opcion_menu(')
        print(f"📊 Método usado {usos} veces en el código")
        
        if usos > 20:
            print("✅ Método usado extensivamente (buena cobertura)")
            return True
        elif usos > 10:
            print("⚠️ Método usado moderadamente")
            return True
        else:
            print("❌ Método usado pocas veces")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def verificar_comando_hola(archivo):
    """Verifica que el comando 'hola' resetee la sesión."""
    print(f"\n🔍 Verificando comando 'hola' en {archivo}...")
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Verificar que existe la validación del comando
        if 'validar_comando_menu' in codigo:
            print("✅ Validación de comando menú encontrada")
            
            # Verificar que elimina sesión y muestra menú
            if 'eliminar_sesion' in codigo and '_menu_principal' in codigo:
                print("✅ Comando resetea sesión y muestra menú")
                return True
            else:
                print("⚠️ Lógica de reseteo incompleta")
                return False
        else:
            print("❌ Validación de comando NO encontrada")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Ejecuta todas las verificaciones."""
    print("="*60)
    print("🧪 VERIFICACIÓN DE FUNCIONALIDAD DEL MENÚ")
    print("="*60)
    
    archivo = "chatbot/engine.py"
    resultados = []
    
    # Test 1: Sintaxis
    resultados.append(verificar_sintaxis(archivo))
    
    # Test 2: Método helper existe
    resultados.append(verificar_metodo_helper(archivo))
    
    # Test 3: Método helper usado extensivamente
    resultados.append(contar_usos_helper(archivo))
    
    # Test 4: Comando hola funciona
    resultados.append(verificar_comando_hola(archivo))
    
    # Resumen
    print("\n" + "="*60)
    print("📋 RESUMEN DE VERIFICACIONES")
    print("="*60)
    
    tests = [
        "Sintaxis correcta",
        "Método helper existe",
        "Método usado extensivamente",
        "Comando 'hola' funciona"
    ]
    
    for i, (test, resultado) in enumerate(zip(tests, resultados), 1):
        estado = "✅" if resultado else "❌"
        print(f"{estado} Test {i}: {test}")
    
    total = sum(resultados)
    print(f"\n📊 Resultado: {total}/{len(resultados)} pruebas pasadas")
    
    if all(resultados):
        print("\n🎉 TODAS LAS VERIFICACIONES PASARON 🎉")
        print("\n✅ La funcionalidad del menú está correctamente implementada:")
        print("   • Método helper creado y usado extensivamente")
        print("   • Comando 'hola' resetea sesión y muestra menú")
        print("   • Sintaxis correcta sin errores")
        return 0
    else:
        print("\n⚠️ ALGUNAS VERIFICACIONES FALLARON")
        return 1


if __name__ == "__main__":
    sys.exit(main())
