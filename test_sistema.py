"""Script para probar el sistema completo."""
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


def test_google_sheets():
    """Prueba conexión a Google Sheets."""
    logger.info("🧪 Probando Google Sheets...")
    try:
        from services import SheetsClient
        sheets = SheetsClient()
        if sheets.test_connection():
            logger.info("✅ Google Sheets: OK")
            return True
        else:
            logger.error("❌ Google Sheets: FAIL")
            return False
    except Exception as e:
        logger.error(f"❌ Google Sheets: ERROR - {e}")
        return False


def test_google_calendar():
    """Prueba conexión a Google Calendar."""
    logger.info("🧪 Probando Google Calendar...")
    try:
        from services import CalendarClient
        calendar = CalendarClient()
        if calendar.test_connection():
            logger.info("✅ Google Calendar: OK")
            return True
        else:
            logger.error("❌ Google Calendar: FAIL")
            return False
    except Exception as e:
        logger.error(f"❌ Google Calendar: ERROR - {e}")
        return False


def test_evolution_api():
    """Prueba conexión a Evolution API."""
    logger.info("🧪 Probando Evolution API...")
    try:
        from services import EvolutionAPI
        evolution = EvolutionAPI()
        status = evolution.get_instance_status()
        if status:
            logger.info("✅ Evolution API: OK")
            return True
        else:
            logger.error("❌ Evolution API: FAIL")
            return False
    except Exception as e:
        logger.error(f"❌ Evolution API: ERROR - {e}")
        return False


def test_chatbot():
    """Prueba el motor del chatbot."""
    logger.info("🧪 Probando Chatbot Engine...")
    try:
        from chatbot import ChatbotEngine
        chatbot = ChatbotEngine()
        
        # Simular mensaje
        respuesta = chatbot.procesar_mensaje("573001234567", "hola")
        
        if "Bienvenido" in respuesta:
            logger.info("✅ Chatbot Engine: OK")
            return True
        else:
            logger.error("❌ Chatbot Engine: FAIL")
            return False
    except Exception as e:
        logger.error(f"❌ Chatbot Engine: ERROR - {e}")
        return False


def main():
    """Ejecuta todas las pruebas."""
    logger.info("🚀 Iniciando pruebas del sistema...\n")
    
    resultados = {
        "Google Sheets": test_google_sheets(),
        "Google Calendar": test_google_calendar(),
        "Evolution API": test_evolution_api(),
        "Chatbot Engine": test_chatbot()
    }
    
    logger.info("\n📊 Resumen de pruebas:")
    for nombre, resultado in resultados.items():
        estado = "✅ OK" if resultado else "❌ FAIL"
        logger.info(f"  {nombre}: {estado}")
    
    total = len(resultados)
    exitosas = sum(resultados.values())
    
    logger.info(f"\n🎯 Total: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        logger.info("✅ Sistema listo para usar")
        return 0
    else:
        logger.error("❌ Hay problemas que resolver")
        return 1


if __name__ == "__main__":
    sys.exit(main())
