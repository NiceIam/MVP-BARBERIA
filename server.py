"""Servidor FastAPI para el chatbot."""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Set
from loguru import logger
import sys
import time

from config.settings import HOST, PORT, DEBUG
from chatbot import ChatbotEngine
from services import SheetsClient, CalendarClient, EvolutionAPI

# Configurar logging
logger.remove()
logger.add(sys.stderr, level="INFO" if not DEBUG else "DEBUG")
logger.add("logs/barberia_{time}.log", rotation="1 day", retention="30 days", level="INFO")

# Inicializar FastAPI
app = FastAPI(
    title="Barbería Churco Chatbot",
    description="Sistema de agendamiento por WhatsApp",
    version="2.0.0"
)

# Cache para evitar mensajes duplicados
mensaje_cache: Dict[str, float] = {}
CACHE_TIMEOUT = 5  # segundos

# Inicializar servicios
try:
    chatbot = ChatbotEngine()
    sheets = SheetsClient()
    calendar = CalendarClient()
    evolution = EvolutionAPI()
except FileNotFoundError as e:
    logger.error(str(e))
    logger.error("\n⚠️  SOLUCIÓN:")
    logger.error("   1. Ve a Google Cloud Console")
    logger.error("   2. Crea un Service Account")
    logger.error("   3. Descarga las credenciales JSON")
    logger.error("   4. Guárdalo como 'service_account.json' en la raíz del proyecto")
    sys.exit(1)
except Exception as e:
    logger.error(f"❌ Error inicializando servicios: {e}")
    sys.exit(1)


class SendMessageRequest(BaseModel):
    """Modelo para enviar mensajes."""
    telefono: str
    mensaje: str


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "status": "online",
        "service": "Barbería Churco Chatbot",
        "version": "2.0.0"
    }


@app.post("/")
async def root_webhook(request: Request):
    """Webhook en raíz (redirige a /webhook)."""
    return await webhook(request)


@app.get("/health")
async def health_check():
    """Verifica el estado del sistema."""
    status = {
        "status": "healthy",
        "sheets": "unknown",
        "calendar": "unknown",
        "evolution": "unknown"
    }
    
    # Verificar Google Sheets
    try:
        if sheets.test_connection():
            status["sheets"] = "connected"
        else:
            status["sheets"] = "error"
    except Exception as e:
        status["sheets"] = f"error: {str(e)}"
    
    # Verificar Google Calendar
    try:
        if calendar.test_connection():
            status["calendar"] = "connected"
        else:
            status["calendar"] = "error"
    except Exception as e:
        status["calendar"] = f"error: {str(e)}"
    
    # Verificar Evolution API
    try:
        instance_status = evolution.get_instance_status()
        if instance_status:
            status["evolution"] = "connected"
        else:
            status["evolution"] = "error"
    except Exception as e:
        status["evolution"] = f"error: {str(e)}"
    
    return status


@app.post("/webhook")
async def webhook(request: Request):
    """Recibe mensajes de WhatsApp vía Evolution API."""
    try:
        data = await request.json()
        logger.info(f"📨 Webhook recibido: {data}")
        return await procesar_webhook_interno(data)
    except Exception as e:
        logger.error(f"❌ Error procesando webhook: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/send-message")
async def send_message(request: SendMessageRequest):
    """Envía un mensaje manualmente."""
    try:
        success = evolution.send_message(request.telefono, request.mensaje)
        if success:
            return {"status": "sent", "telefono": request.telefono}
        else:
            raise HTTPException(status_code=500, detail="Error enviando mensaje")
    except Exception as e:
        logger.error(f"Error enviando mensaje: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Obtiene estadísticas del sistema."""
    # TODO: Implementar estadísticas desde Sheets
    return {
        "total_citas": 0,
        "citas_hoy": 0,
        "citas_pendientes": 0
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Iniciando servidor en {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
