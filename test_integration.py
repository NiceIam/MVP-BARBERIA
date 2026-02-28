"""
Script de prueba para verificar la integración completa
"""
from dotenv import load_dotenv
from database import get_database
from evolution_api import get_evolution_api
from chatbot_integrado import get_gestor_chatbots

load_dotenv()

def test_database():
    """Prueba la conexión a la base de datos"""
    print("\n" + "=" * 60)
    print("TEST 1: Conexión a Base de Datos")
    print("=" * 60)
    
    try:
        db = get_database()
        print("✅ Conexión exitosa a PostgreSQL")
        
        # Crear cliente de prueba
        cliente_id = db.crear_cliente("Test Usuario", "3009999999")
        print(f"✅ Cliente de prueba creado (ID: {cliente_id})")
        
        # Buscar cliente
        cliente = db.obtener_cliente_por_telefono("3009999999")
        if cliente:
            print(f"✅ Cliente encontrado: {cliente['nombre']}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_evolution_api():
    """Prueba la conexión a Evolution API"""
    print("\n" + "=" * 60)
    print("TEST 2: Conexión a Evolution API")
    print("=" * 60)
    
    try:
        evolution = get_evolution_api()
        print("✅ Cliente Evolution API inicializado")
        
        # Verificar instancia
        estado = evolution.verificar_instancia()
        print(f"✅ Estado de instancia: {estado}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_chatbot():
    """Prueba el chatbot integrado"""
    print("\n" + "=" * 60)
    print("TEST 3: Chatbot Integrado")
    print("=" * 60)
    
    try:
        gestor = get_gestor_chatbots()
        print("✅ Gestor de chatbots inicializado")
        
        # Simular conversación
        telefono_test = "3001111111"
        
        # Mensaje 1: Inicio
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "")
        print(f"✅ Respuesta de inicio recibida ({len(respuesta)} caracteres)")
        
        # Mensaje 2: Ver servicios
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "4")
        print(f"✅ Respuesta de servicios recibida ({len(respuesta)} caracteres)")
        
        # Limpiar sesión
        gestor.limpiar_sesion(telefono_test)
        print("✅ Sesión limpiada")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flujo_completo():
    """Prueba un flujo completo de reserva"""
    print("\n" + "=" * 60)
    print("TEST 4: Flujo Completo de Reserva")
    print("=" * 60)
    
    try:
        gestor = get_gestor_chatbots()
        telefono_test = "3002222222"
        
        # Inicio
        print("\n[1] Inicio")
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "")
        print(f"✅ Respuesta: {respuesta[:100]}...")
        
        # Reservar
        print("\n[2] Seleccionar reservar")
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "1")
        print(f"✅ Respuesta: {respuesta[:100]}...")
        
        # Servicio
        print("\n[3] Seleccionar servicio")
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "2")
        print(f"✅ Respuesta: {respuesta[:100]}...")
        
        # Barbero
        print("\n[4] Seleccionar barbero")
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "1")
        print(f"✅ Respuesta: {respuesta[:100]}...")
        
        # Fecha
        print("\n[5] Seleccionar fecha")
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "1")
        print(f"✅ Respuesta: {respuesta[:100]}...")
        
        # Hora
        print("\n[6] Seleccionar hora")
        respuesta = gestor.procesar_mensaje_whatsapp(telefono_test, "1")
        print(f"✅ Respuesta: {respuesta[:100]}...")
        
        # Confirmar
        print("\n[7] Confirmar datos")
        respuesta = gestor.procesar_mensaje_whatsapp(
            telefono_test, 
            "Nombre: Test Completo\nTeléfono: 3002222222"
        )
        print(f"✅ Respuesta: {respuesta[:200]}...")
        
        # Verificar en base de datos
        db = get_database()
        citas = db.obtener_citas_por_telefono("3002222222")
        print(f"\n✅ Citas creadas en BD: {len(citas)}")
        
        # Limpiar
        gestor.limpiar_sesion(telefono_test)
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("🧪 SUITE DE PRUEBAS DE INTEGRACIÓN")
    print("=" * 60)
    
    resultados = []
    
    # Test 1: Base de datos
    resultados.append(("Base de Datos", test_database()))
    
    # Test 2: Evolution API
    resultados.append(("Evolution API", test_evolution_api()))
    
    # Test 3: Chatbot
    resultados.append(("Chatbot Integrado", test_chatbot()))
    
    # Test 4: Flujo completo
    resultados.append(("Flujo Completo", test_flujo_completo()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for nombre, resultado in resultados:
        estado = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{estado} - {nombre}")
    
    total = len(resultados)
    exitosos = sum(1 for _, r in resultados if r)
    
    print("\n" + "=" * 60)
    print(f"Resultado: {exitosos}/{total} pruebas exitosas")
    print("=" * 60)
    
    if exitosos == total:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\nPuedes iniciar el servidor con:")
        print("  python server.py")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisa la configuración.")


if __name__ == "__main__":
    main()
