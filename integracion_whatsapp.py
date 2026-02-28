"""
Ejemplo de integración del chatbot con WhatsApp usando Twilio
Este archivo muestra cómo conectar el chatbot a WhatsApp Business API
"""
from chatbot_barberia import ChatbotBarberia
from typing import Dict

# Nota: Necesitarás instalar: pip install twilio flask
# from twilio.twiml.messaging_response import MessagingResponse
# from flask import Flask, request

class WhatsAppIntegration:
    """Integración del chatbot con WhatsApp"""
    
    def __init__(self):
        self.sesiones = {}  # Almacena sesiones por número de teléfono
    
    def obtener_chatbot(self, numero_telefono: str) -> ChatbotBarberia:
        """Obtiene o crea una sesión de chatbot para un número"""
        if numero_telefono not in self.sesiones:
            self.sesiones[numero_telefono] = ChatbotBarberia()
        return self.sesiones[numero_telefono]
    
    def procesar_mensaje_whatsapp(self, numero_telefono: str, mensaje: str) -> str:
        """Procesa un mensaje de WhatsApp y retorna la respuesta"""
        chatbot = self.obtener_chatbot(numero_telefono)
        
        # Si es el primer mensaje, iniciar el chatbot
        if chatbot.estado.value == "inicio":
            respuesta = chatbot.procesar_mensaje("")
        else:
            respuesta = chatbot.procesar_mensaje(mensaje)
        
        return respuesta
    
    def limpiar_sesion(self, numero_telefono: str):
        """Limpia la sesión de un usuario"""
        if numero_telefono in self.sesiones:
            del self.sesiones[numero_telefono]


# Ejemplo de uso con Flask y Twilio
"""
app = Flask(__name__)
whatsapp_integration = WhatsAppIntegration()

@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    # Obtener datos del mensaje
    numero_entrante = request.values.get('From', '')
    mensaje_entrante = request.values.get('Body', '').strip()
    
    # Procesar mensaje
    respuesta_texto = whatsapp_integration.procesar_mensaje_whatsapp(
        numero_entrante, 
        mensaje_entrante
    )
    
    # Crear respuesta de Twilio
    resp = MessagingResponse()
    resp.message(respuesta_texto)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
"""

# Configuración necesaria en Twilio:
# 1. Crear cuenta en Twilio (https://www.twilio.com)
# 2. Configurar WhatsApp Sandbox o WhatsApp Business API
# 3. Configurar webhook URL: https://tu-dominio.com/whatsapp
# 4. Agregar credenciales de Twilio en variables de entorno:
#    - TWILIO_ACCOUNT_SID
#    - TWILIO_AUTH_TOKEN
#    - TWILIO_WHATSAPP_NUMBER

print("""
📱 GUÍA DE INTEGRACIÓN CON WHATSAPP

Para integrar el chatbot con WhatsApp, sigue estos pasos:

1. INSTALAR DEPENDENCIAS:
   pip install twilio flask

2. CONFIGURAR TWILIO:
   - Crear cuenta en https://www.twilio.com
   - Activar WhatsApp Sandbox o WhatsApp Business API
   - Obtener credenciales (Account SID y Auth Token)

3. CONFIGURAR WEBHOOK:
   - Desplegar la aplicación Flask en un servidor (Heroku, AWS, etc.)
   - Configurar la URL del webhook en Twilio: https://tu-dominio.com/whatsapp
   - Twilio enviará los mensajes a esta URL

4. VARIABLES DE ENTORNO:
   export TWILIO_ACCOUNT_SID="tu_account_sid"
   export TWILIO_AUTH_TOKEN="tu_auth_token"
   export TWILIO_WHATSAPP_NUMBER="whatsapp:+14155238886"

5. EJECUTAR:
   python integracion_whatsapp.py

6. PROBAR:
   - Enviar mensaje de WhatsApp al número de Twilio
   - El chatbot responderá automáticamente

ALTERNATIVAS:
- Baileys (Node.js): Conexión directa sin Twilio
- WhatsApp Business API oficial
- Plataformas como Twilio, MessageBird, Vonage
""")
