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
    """Webhook en raíz (procesa igual que /webhook)."""
    try:
        data = await request.json()
        logger.info(f"📨 Webhook recibido en /: {data}")
        return await procesar_webhook_interno(data)
    except Exception as e:
        logger.error(f"❌ Error procesando webhook en /: {e}")
        return {"status": "error", "message": str(e)}


async def procesar_webhook_interno(data: dict) -> dict:
    """Procesa el webhook internamente."""
    event_type = data.get("event")
    
    if event_type == "messages.upsert":
        message_data = data.get("data", {})
        key = message_data.get("key", {})
        message = message_data.get("message", {})
        
        # Obtener teléfono del remitente
        telefono = key.get("remoteJid", "").replace("@s.whatsapp.net", "")
        
        # Obtener texto del mensaje
        texto = ""
        if "conversation" in message:
            texto = message["conversation"]
        elif "extendedTextMessage" in message:
            texto = message["extendedTextMessage"].get("text", "")
        
        if telefono and texto:
            # Crear ID único para este mensaje
            message_id = key.get("id", "")
            cache_key = f"{telefono}:{message_id}:{texto}"
            
            # Verificar si ya procesamos este mensaje recientemente
            now = time.time()
            if cache_key in mensaje_cache:
                if now - mensaje_cache[cache_key] < CACHE_TIMEOUT:
                    logger.info(f"⏭️  Mensaje duplicado ignorado: {telefono}")
                    return {"status": "ok", "message": "duplicado"}
            
            # Guardar en cache
            mensaje_cache[cache_key] = now
            
            # Limpiar cache antiguo
            keys_to_delete = [k for k, v in mensaje_cache.items() if now - v > CACHE_TIMEOUT]
            for k in keys_to_delete:
                del mensaje_cache[k]
            
            logger.info(f"💬 Mensaje de {telefono}: {texto}")
            
            # Procesar mensaje con el chatbot
            respuesta = chatbot.procesar_mensaje(telefono, texto)
            
            # Enviar respuesta
            evolution.send_message(telefono, respuesta)
            logger.info(f"✅ Respuesta enviada a {telefono}")
    
    return {"status": "ok"}


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
