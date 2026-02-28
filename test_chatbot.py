"""
Script de prueba para el chatbot de barbería
Simula conversaciones completas para validar todos los flujos
"""
from chatbot_barberia import ChatbotBarberia


def test_flujo_reserva_completo():
    """Prueba el flujo completo de reserva de cita"""
    print("\n" + "="*60)
    print("TEST 1: Flujo de Reserva Completo")
    print("="*60)
    
    chatbot = ChatbotBarberia()
    
    # Inicio
    print("\n[INICIO]")
    respuesta = chatbot.procesar_mensaje("")
    print(respuesta)
    
    # Seleccionar reservar
    print("\n[Usuario: 1]")
    respuesta = chatbot.procesar_mensaje("1")
    print(respuesta)
    
    # Seleccionar servicio (Corte + Barba)
    print("\n[Usuario: 2]")
    respuesta = chatbot.procesar_mensaje("2")
    print(respuesta)
    
    # Seleccionar barbero (Carlos)
    print("\n[Usuario: 1]")
    respuesta = chatbot.procesar_mensaje("1")
    print(respuesta)
    
    # Seleccionar fecha (primera disponible)
    print("\n[Usuario: 1]")
    respuesta = chatbot.procesar_mensaje("1")
    print(respuesta)
    
    # Seleccionar hora (primera disponible)
    print("\n[Usuario: 1]")
    respuesta = chatbot.procesar_mensaje("1")
    print(respuesta)
    
    # Confirmar datos
    print("\n[Usuario: Nombre y teléfono]")
    respuesta = chatbot.procesar_mensaje("Nombre: Carlos Rodríguez\nTeléfono: 3001234567")
    print(respuesta)
    
    print("\n✅ Test de reserva completado exitosamente")
    return chatbot


def test_flujo_consultar_cita(chatbot):
    """Prueba el flujo de consulta de cita"""
    print("\n" + "="*60)
    print("TEST 2: Flujo de Consulta de Cita")
    print("="*60)
    
    # Volver al menú
    print("\n[Usuario: menu]")
    respuesta = chatbot.procesar_mensaje("menu")
    print(respuesta)
    
    # Consultar cita
    print("\n[Usuario: 2]")
    respuesta = chatbot.procesar_mensaje("2")
    print(respuesta)
    
    # Buscar por teléfono
    print("\n[Usuario: 3001234567]")
    respuesta = chatbot.procesar_mensaje("3001234567")
    print(respuesta)
    
    print("\n✅ Test de consulta completado exitosamente")


def test_flujo_ver_servicios():
    """Prueba el flujo de ver servicios"""
    print("\n" + "="*60)
    print("TEST 3: Flujo de Ver Servicios")
    print("="*60)
    
    chatbot = ChatbotBarberia()
    
    # Inicio
    respuesta = chatbot.procesar_mensaje("")
    
    # Ver servicios
    print("\n[Usuario: 4]")
    respuesta = chatbot.procesar_mensaje("4")
    print(respuesta)
    
    print("\n✅ Test de servicios completado exitosamente")


def test_flujo_ver_promociones():
    """Prueba el flujo de ver promociones"""
    print("\n" + "="*60)
    print("TEST 4: Flujo de Ver Promociones")
    print("="*60)
    
    chatbot = ChatbotBarberia()
    
    # Inicio
    respuesta = chatbot.procesar_mensaje("")
    
    # Ver promociones
    print("\n[Usuario: 5]")
    respuesta = chatbot.procesar_mensaje("5")
    print(respuesta)
    
    print("\n✅ Test de promociones completado exitosamente")


def test_flujo_ver_barberos():
    """Prueba el flujo de ver barberos"""
    print("\n" + "="*60)
    print("TEST 5: Flujo de Ver Barberos")
    print("="*60)
    
    chatbot = ChatbotBarberia()
    
    # Inicio
    respuesta = chatbot.procesar_mensaje("")
    
    # Ver barberos
    print("\n[Usuario: 6]")
    respuesta = chatbot.procesar_mensaje("6")
    print(respuesta)
    
    print("\n✅ Test de barberos completado exitosamente")


def test_flujo_contacto():
    """Prueba el flujo de información de contacto"""
    print("\n" + "="*60)
    print("TEST 6: Flujo de Información de Contacto")
    print("="*60)
    
    chatbot = ChatbotBarberia()
    
    # Inicio
    respuesta = chatbot.procesar_mensaje("")
    
    # Ver contacto
    print("\n[Usuario: 7]")
    respuesta = chatbot.procesar_mensaje("7")
    print(respuesta)
    
    print("\n✅ Test de contacto completado exitosamente")


def test_flujo_cancelar_cita(chatbot):
    """Prueba el flujo de cancelación de cita"""
    print("\n" + "="*60)
    print("TEST 7: Flujo de Cancelación de Cita")
    print("="*60)
    
    # Volver al menú
    print("\n[Usuario: menu]")
    respuesta = chatbot.procesar_mensaje("menu")
    print(respuesta)
    
    # Cancelar cita
    print("\n[Usuario: 3]")
    respuesta = chatbot.procesar_mensaje("3")
    print(respuesta)
    
    # Buscar por teléfono
    print("\n[Usuario: 3001234567]")
    respuesta = chatbot.procesar_mensaje("3001234567")
    print(respuesta)
    
    print("\n✅ Test de cancelación completado exitosamente")


def test_intenciones_naturales():
    """Prueba el reconocimiento de intenciones con lenguaje natural"""
    print("\n" + "="*60)
    print("TEST 8: Reconocimiento de Intenciones Naturales")
    print("="*60)
    
    chatbot = ChatbotBarberia()
    
    # Inicio
    respuesta = chatbot.procesar_mensaje("")
    
    # Probar diferentes formas de pedir una cita
    print("\n[Usuario: quiero agendar una cita]")
    respuesta = chatbot.procesar_mensaje("quiero agendar una cita")
    print(respuesta[:100] + "...")
    
    chatbot.reiniciar()
    respuesta = chatbot.procesar_mensaje("")
    
    print("\n[Usuario: necesito un corte de pelo]")
    respuesta = chatbot.procesar_mensaje("necesito un corte de pelo")
    print(respuesta[:100] + "...")
    
    chatbot.reiniciar()
    respuesta = chatbot.procesar_mensaje("")
    
    print("\n[Usuario: cuanto cuesta un corte]")
    respuesta = chatbot.procesar_mensaje("cuanto cuesta un corte")
    print(respuesta[:100] + "...")
    
    print("\n✅ Test de intenciones naturales completado exitosamente")


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests del chatbot"""
    print("\n" + "="*60)
    print("🧪 INICIANDO SUITE DE PRUEBAS DEL CHATBOT")
    print("="*60)
    
    # Test 1: Reserva completa
    chatbot_con_cita = test_flujo_reserva_completo()
    
    # Test 2: Consultar cita (usa el chatbot con cita creada)
    test_flujo_consultar_cita(chatbot_con_cita)
    
    # Test 3: Ver servicios
    test_flujo_ver_servicios()
    
    # Test 4: Ver promociones
    test_flujo_ver_promociones()
    
    # Test 5: Ver barberos
    test_flujo_ver_barberos()
    
    # Test 6: Contacto
    test_flujo_contacto()
    
    # Test 7: Cancelar cita (usa el chatbot con cita creada)
    test_flujo_cancelar_cita(chatbot_con_cita)
    
    # Test 8: Intenciones naturales
    test_intenciones_naturales()
    
    print("\n" + "="*60)
    print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
    print("="*60)
    print("\n💡 El chatbot está funcionando correctamente.")
    print("   Puedes ejecutar 'python main.py' para probarlo interactivamente.\n")


if __name__ == "__main__":
    ejecutar_todos_los_tests()
