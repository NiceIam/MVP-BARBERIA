"""
Servidor FastAPI para recibir webhooks de Evolution API
"""
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn
from chatbot_integrado import get_gestor_chatbots
from evolution_api import get_evolution_api
from database import get_database

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Chatbot Barbería - WhatsApp Bot")

# Inicializar servicios
gestor = get_gestor_chatbots()
evolution = get_evolution_api()
db = get_database()


@app.on_event("startup")
async def startup_event():
    """Evento de inicio del servidor"""
    print("=" * 60)
    print("🚀 Iniciando servidor del chatbot...")
    print("=" * 60)
    
    # Verificar conexión a base de datos
    try:
        print("✅ Base de datos conectada")
    except Exception as e:
        print(f"❌ Error conectando a base de datos: {e}")
    
    # Verificar instancia de Evolution API
    try:
        estado = evolution.verificar_instancia()
        print(f"✅ Evolution API conectada: {estado}")
    except Exception as e:
        print(f"❌ Error conectando a Evolution API: {e}")
    
    print("=" * 60)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "status": "online",
        "service": "Chatbot Barbería",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    try:
        # Verificar base de datos
        db_status = "connected"
        
        # Verificar Evolution API
        evolution_status = evolution.verificar_instancia()
        
        return {
            "status": "healthy",
            "database": db_status,
            "evolution_api": evolution_status
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/webhook")
async def webhook_evolution(request: Request):
    """
    Webhook para recibir mensajes de Evolution API
    """
    try:
        data = await request.json()
        
        # Log del webhook recibido
        print(f"📨 Webhook recibido: {data.get('event', 'unknown')}")
        
        # Verificar que sea un mensaje
        event = data.get('event')
        
        if event == 'messages.upsert':
            # Extraer información del mensaje
            message_data = data.get('data', {})
            
            # Verificar que no sea un mensaje propio
            if message_data.get('key', {}).get('fromMe'):
                return {"status": "ignored", "reason": "own_message"}
            
            # Extraer datos del remitente y mensaje
            remote_jid = message_data.get('key', {}).get('remoteJid', '')
            message_type = message_data.get('messageType', '')
            
            # Extraer número de teléfono
            telefono = remote_jid.split('@')[0] if '@' in remote_jid else remote_jid
            
            # Extraer texto del mensaje
            mensaje_texto = ""
            if message_type == 'conversation':
                mensaje_texto = message_data.get('message', {}).get('conversation', '')
            elif message_type == 'extendedTextMessage':
                mensaje_texto = message_data.get('message', {}).get('extendedTextMessage', {}).get('text', '')
            elif message_type == 'imageMessage':
                mensaje_texto = message_data.get('message', {}).get('imageMessage', {}).get('caption', '')
            
            if not mensaje_texto:
                return {"status": "ignored", "reason": "no_text"}
            
            print(f"👤 Mensaje de {telefono}: {mensaje_texto}")
            
            # Procesar mensaje con el chatbot
            respuesta = gestor.procesar_mensaje_whatsapp(telefono, mensaje_texto)
            
            # Enviar respuesta
            resultado = gestor.enviar_respuesta(telefono, respuesta)
            
            print(f"🤖 Respuesta enviada a {telefono}")
            
            return {
                "status": "success",
                "telefono": telefono,
                "mensaje_recibido": mensaje_texto,
                "respuesta_enviada": True
            }
        
        return {"status": "ignored", "event": event}
    
    except Exception as e:
        print(f"❌ Error procesando webhook: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/send-message")
async def send_message(request: Request):
    """
    Endpoint para enviar mensajes manualmente
    Body: {"telefono": "3001234567", "mensaje": "Hola"}
    """
    try:
        data = await request.json()
        telefono = data.get('telefono')
        mensaje = data.get('mensaje')
        
        if not telefono or not mensaje:
            raise HTTPException(status_code=400, detail="Faltan parámetros")
        
        resultado = evolution.enviar_mensaje_texto(telefono, mensaje)
        
        return {
            "status": "success",
            "resultado": resultado
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.get("/instance/status")
async def instance_status():
    """Obtiene el estado de la instancia de WhatsApp"""
    try:
        estado = evolution.verificar_instancia()
        return {
            "status": "success",
            "data": estado
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.get("/instance/qr")
async def get_qr():
    """Obtiene el código QR para conectar WhatsApp"""
    try:
        qr_data = evolution.obtener_qr()
        return {
            "status": "success",
            "data": qr_data
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/instance/connect")
async def connect_instance():
    """Conecta la instancia de WhatsApp"""
    try:
        resultado = evolution.conectar_instancia()
        return {
            "status": "success",
            "data": resultado
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/webhook/configure")
async def configure_webhook(request: Request):
    """
    Configura el webhook en Evolution API
    Body: {"webhook_url": "https://tu-dominio.com/webhook"}
    """
    try:
        data = await request.json()
        webhook_url = data.get('webhook_url')
        
        if not webhook_url:
            raise HTTPException(status_code=400, detail="Falta webhook_url")
        
        resultado = evolution.configurar_webhook(webhook_url)
        
        return {
            "status": "success",
            "resultado": resultado
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.get("/stats")
async def get_stats():
    """Obtiene estadísticas del chatbot"""
    try:
        # Aquí puedes agregar consultas a la base de datos para obtener estadísticas
        return {
            "status": "success",
            "sesiones_activas": len(gestor.chatbots),
            "message": "Estadísticas básicas"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          💈 CHATBOT BARBERÍA - WHATSAPP BOT 💈          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🌐 Servidor: http://{host}:{port}
📡 Webhook: http://{host}:{port}/webhook
🔧 Health: http://{host}:{port}/health
📊 Stats: http://{host}:{port}/stats

Presiona CTRL+C para detener el servidor
""")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=debug
    )
