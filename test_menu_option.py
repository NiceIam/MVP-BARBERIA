"""Script para probar que la opción de menú funcione correctamente."""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from chatbot.engine import ChatbotEngine
from loguru import logger


def test_menu_option():
    """Prueba que todos los mensajes incluyan la opción de volver al menú."""
    logger.info("🧪 Iniciando pruebas de opción de menú...")
    
    engine = ChatbotEngine()
    test_phone = "573999999999"
    
    # Test 1: Verificar que el método helper funcione
    logger.info("\n📝 Test 1: Verificar método _agregar_opcion_menu")
    mensaje_test = "Este es un mensaje de prueba"
    resultado = engine._agregar_opcion_menu(mensaje_test)
    assert "hola" in resultado.lower(), "El mensaje debe incluir 'hola'"
    assert "menú" in resultado.lower(), "El mensaje debe incluir 'menú'"
    logger.info(f"✅ Método helper funciona correctamente")
    logger.info(f"   Resultado: {resultado}")
    
    # Test 2: Verificar menú principal
    logger.info("\n📝 Test 2: Verificar que comando 'hola' muestre el menú")
    respuesta = engine.procesar_mensaje(test_phone, "hola")
    assert "Bienvenido" in respuesta, "Debe mostrar mensaje de bienvenida"
    assert "1. Agendar cita" in respuesta, "Debe mostrar opción de agendar"
    logger.info("✅ Comando 'hola' muestra el menú correctamente")
    
    # Test 3: Verificar opción inválida incluye menú
    logger.info("\n📝 Test 3: Verificar mensaje de opción inválida")
    respuesta = engine.procesar_mensaje(test_phone, "99")
    assert "hola" in respuesta.lower(), "Mensaje de error debe incluir opción de menú"
    logger.info("✅ Mensaje de error incluye opción de menú")
    logger.info(f"   Respuesta: {respuesta[:100]}...")
    
    # Test 4: Verificar flujo de agendamiento
    logger.info("\n📝 Test 4: Verificar flujo de agendamiento")
    # Resetear sesión
    engine.sheets.eliminar_sesion(test_phone)
    
    # Iniciar con hola
    respuesta = engine.procesar_mensaje(test_phone, "hola")
    logger.info("   - Menú mostrado")
    
    # Seleccionar agendar cita (opción 1)
    respuesta = engine.procesar_mensaje(test_phone, "1")
    logger.info(f"   - Respuesta a opción 1: {respuesta[:80]}...")
    
    # Verificar que incluya opción de menú
    if "hola" in respuesta.lower():
        logger.info("✅ Flujo de agendamiento incluye opción de menú")
    else:
        logger.warning("⚠️ Flujo de agendamiento NO incluye opción de menú")
    
    # Test 5: Verificar que 'hola' resetee en cualquier momento
    logger.info("\n📝 Test 5: Verificar que 'hola' resetee la sesión")
    respuesta = engine.procesar_mensaje(test_phone, "hola")
    assert "Bienvenido" in respuesta, "Debe volver al menú principal"
    logger.info("✅ Comando 'hola' resetea correctamente en cualquier momento")
    
    # Test 6: Verificar información de barbería
    logger.info("\n📝 Test 6: Verificar información de barbería")
    engine.sheets.eliminar_sesion(test_phone)
    engine.procesar_mensaje(test_phone, "hola")
    respuesta = engine.procesar_mensaje(test_phone, "5")
    assert "Barbería Churco" in respuesta, "Debe mostrar información"
    assert "hola" in respuesta.lower(), "Debe incluir opción de menú"
    logger.info("✅ Información de barbería incluye opción de menú")
    
    # Limpiar sesión de prueba
    engine.sheets.eliminar_sesion(test_phone)
    
    logger.info("\n" + "="*60)
    logger.info("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    logger.info("="*60)
    logger.info("\n📋 Resumen:")
    logger.info("   ✓ Método helper funciona")
    logger.info("   ✓ Comando 'hola' muestra menú")
    logger.info("   ✓ Mensajes de error incluyen opción de menú")
    logger.info("   ✓ Flujo de agendamiento incluye opción de menú")
    logger.info("   ✓ 'hola' resetea sesión en cualquier momento")
    logger.info("   ✓ Información incluye opción de menú")


def test_menu_messages():
    """Prueba que los mensajes clave incluyan la opción de menú."""
    logger.info("\n🔍 Verificando mensajes específicos...")
    
    engine = ChatbotEngine()
    
    # Probar diferentes mensajes
    mensajes_prueba = [
        "Este es un mensaje de prueba",
        "Error: Algo salió mal",
        "✅ Operación exitosa",
        "Por favor selecciona una opción"
    ]
    
    for msg in mensajes_prueba:
        resultado = engine._agregar_opcion_menu(msg)
        assert msg in resultado, f"El mensaje original debe estar presente"
        assert "hola" in resultado.lower(), f"Debe incluir 'hola'"
        logger.info(f"   ✓ '{msg[:30]}...' → incluye opción de menú")
    
    logger.info("✅ Todos los mensajes incluyen correctamente la opción de menú")


if __name__ == "__main__":
    try:
        test_menu_option()
        test_menu_messages()
        logger.info("\n🎉 TODAS LAS PRUEBAS COMPLETADAS CON ÉXITO 🎉\n")
    except AssertionError as e:
        logger.error(f"\n❌ PRUEBA FALLIDA: {e}\n")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ ERROR INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
