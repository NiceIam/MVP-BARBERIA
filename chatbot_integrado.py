"""
Chatbot integrado con PostgreSQL y Evolution API
"""
import json
from datetime import datetime
from typing import Dict, Optional
from chatbot_barberia import ChatbotBarberia, EstadoConversacion
from database import get_database
from evolution_api import get_evolution_api


class ChatbotIntegrado(ChatbotBarberia):
    """Chatbot con persistencia en base de datos"""
    
    def __init__(self, telefono: str):
        super().__init__()
        self.telefono = telefono
        self.db = get_database()
        self._cargar_sesion()
    
    def _cargar_sesion(self):
        """Carga la sesión desde la base de datos"""
        sesion = self.db.obtener_sesion(self.telefono)
        
        if sesion:
            # Restaurar estado
            try:
                self.estado = EstadoConversacion(sesion['estado'])
                self.datos_temporales = sesion['datos_temporales'] or {}
            except (ValueError, KeyError):
                # Si hay error, reiniciar sesión
                self.estado = EstadoConversacion.INICIO
                self.datos_temporales = {}
        else:
            # Nueva sesión
            self.estado = EstadoConversacion.INICIO
            self.datos_temporales = {}
    
    def _guardar_sesion(self):
        """Guarda la sesión en la base de datos"""
        self.db.guardar_sesion(
            telefono=self.telefono,
            estado=self.estado.value,
            datos_temporales=self.datos_temporales
        )
    
    def procesar_mensaje(self, mensaje: str) -> str:
        """Procesa el mensaje y guarda la sesión"""
        respuesta = super().procesar_mensaje(mensaje)
        self._guardar_sesion()
        return respuesta
    
    def _estado_confirmar_datos(self, mensaje: str) -> str:
        """Confirma los datos y guarda en base de datos"""
        import re
        
        # Extraer nombre y teléfono
        nombre_match = re.search(r'nombre:\s*(.+?)(?:\n|teléfono|telefono|$)', mensaje, re.IGNORECASE)
        telefono_match = re.search(r'(?:teléfono|telefono):\s*(\d+)', mensaje, re.IGNORECASE)
        
        if nombre_match and telefono_match:
            nombre = nombre_match.group(1).strip()
            telefono = telefono_match.group(1).strip()
            
            try:
                # Crear o obtener cliente
                cliente_id = self.db.crear_cliente(nombre, telefono)
                
                # Crear la cita en la base de datos
                cita_id = self.db.crear_cita(
                    cliente_id=cliente_id,
                    servicio=self.datos_temporales["servicio"]["nombre"],
                    precio=self.datos_temporales["servicio"]["precio"],
                    duracion=self.datos_temporales["servicio"]["duracion"],
                    barbero=self.datos_temporales["barbero"]["nombre"],
                    fecha=self.datos_temporales["fecha"],
                    hora=self.datos_temporales["hora"]
                )
                
                fecha_obj = datetime.strptime(self.datos_temporales["fecha"], "%Y-%m-%d")
                fecha_formato = fecha_obj.strftime("%d/%m/%Y")
                
                respuesta = f"""
✅ ¡Cita confirmada exitosamente!

📋 Resumen de tu cita:
━━━━━━━━━━━━━━━━━━━━
👤 Cliente: {nombre}
📞 Teléfono: {telefono}
✂️ Servicio: {self.datos_temporales["servicio"]["nombre"]}
💰 Precio: ${self.datos_temporales["servicio"]["precio"]:,}
👨‍💼 Barbero: {self.datos_temporales["barbero"]["nombre"]}
📅 Fecha: {fecha_formato}
🕐 Hora: {self.datos_temporales["hora"]}
━━━━━━━━━━━━━━━━━━━━

📱 Te enviaremos un recordatorio 24 horas antes.
💡 Si necesitas cancelar, hazlo con al menos 2 horas de anticipación.

¿Necesitas algo más? Escribe 'menu' para volver al inicio.
"""
                self.estado = EstadoConversacion.MENU_PRINCIPAL
                self.datos_temporales = {}
                return respuesta
                
            except Exception as e:
                print(f"Error al guardar cita: {e}")
                return f"""
❌ Hubo un error al guardar tu cita. Por favor, intenta nuevamente.

Error: {str(e)}

Escribe 'menu' para volver al inicio.
"""
        else:
            return """
No pude identificar tus datos. Por favor, usa este formato:

Nombre: [Tu nombre completo]
Teléfono: [Tu número de teléfono]

Ejemplo:
Nombre: Juan Pérez
Teléfono: 3001234567
"""
    
    def _estado_consultar_cita(self, mensaje: str) -> str:
        """Consulta citas desde la base de datos"""
        try:
            # Buscar clientes
            clientes = self.db.buscar_clientes(mensaje)
            
            if not clientes:
                self.estado = EstadoConversacion.MENU_PRINCIPAL
                return """
❌ No encontré citas con esa información.

Verifica que hayas escrito correctamente tu nombre o teléfono.

Escribe 'menu' para volver al inicio.
"""
            
            # Obtener citas de todos los clientes encontrados
            todas_citas = []
            for cliente in clientes:
                citas = self.db.obtener_citas_cliente(cliente['id'])
                todas_citas.extend(citas)
            
            if not todas_citas:
                self.estado = EstadoConversacion.MENU_PRINCIPAL
                return """
❌ No encontré citas activas con esa información.

Escribe 'menu' para volver al inicio.
"""
            
            texto = "📋 Citas encontradas:\n\n"
            for cita in todas_citas:
                fecha_obj = datetime.strptime(str(cita['fecha']), "%Y-%m-%d")
                fecha_formato = fecha_obj.strftime("%d/%m/%Y")
                
                texto += f"""
━━━━━━━━━━━━━━━━━━━━
👤 Cliente: {cita['cliente_nombre']}
📞 Teléfono: {cita['cliente_telefono']}
✂️ Servicio: {cita['servicio']}
💰 Precio: ${float(cita['precio']):,.0f}
👨‍💼 Barbero: {cita['barbero']}
📅 Fecha: {fecha_formato}
🕐 Hora: {str(cita['hora'])[:-3]}
━━━━━━━━━━━━━━━━━━━━

"""
            texto += "\n¿Necesitas algo más? Escribe 'menu' para volver al inicio."
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return texto
            
        except Exception as e:
            print(f"Error al consultar citas: {e}")
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return f"""
❌ Hubo un error al consultar las citas.

Error: {str(e)}

Escribe 'menu' para volver al inicio.
"""
    
    def _estado_cancelar_cita(self, mensaje: str) -> str:
        """Cancela citas desde la base de datos"""
        try:
            # Buscar clientes
            clientes = self.db.buscar_clientes(mensaje)
            
            if not clientes:
                self.estado = EstadoConversacion.MENU_PRINCIPAL
                return """
❌ No encontré citas con esa información.

Verifica que hayas escrito correctamente tu nombre o teléfono.

Escribe 'menu' para volver al inicio.
"""
            
            # Cancelar citas de todos los clientes encontrados
            total_canceladas = 0
            for cliente in clientes:
                canceladas = self.db.cancelar_citas_cliente(cliente['id'])
                total_canceladas += canceladas
            
            if total_canceladas == 0:
                self.estado = EstadoConversacion.MENU_PRINCIPAL
                return """
❌ No encontré citas activas para cancelar.

Escribe 'menu' para volver al inicio.
"""
            
            texto = f"""
✅ Cita(s) cancelada(s) exitosamente.

Se cancelaron {total_canceladas} cita(s).

💡 Recuerda que puedes agendar una nueva cita cuando lo desees.

¿Necesitas algo más? Escribe 'menu' para volver al inicio.
"""
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return texto
            
        except Exception as e:
            print(f"Error al cancelar citas: {e}")
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return f"""
❌ Hubo un error al cancelar las citas.

Error: {str(e)}

Escribe 'menu' para volver al inicio.
"""
    
    def _mostrar_horas(self, fecha: str) -> str:
        """Muestra horas disponibles excluyendo las ocupadas"""
        horas_ocupadas = self.db.obtener_horarios_ocupados(fecha)
        horas_disponibles = [h for h in self.horarios_disponibles.get(fecha, []) 
                            if h not in horas_ocupadas]
        
        if not horas_disponibles:
            return """
❌ No hay horarios disponibles para esta fecha.

Por favor, selecciona otra fecha. Escribe 'menu' para volver al inicio.
"""
        
        texto = "🕐 Selecciona la hora de tu cita:\n\n"
        for i, hora in enumerate(horas_disponibles, 1):
            texto += f"{i}. {hora}\n"
        
        # Actualizar horarios disponibles temporalmente
        self.horarios_disponibles[fecha] = horas_disponibles
        
        texto += "\nEscribe el número de la hora que prefieres."
        return texto
    
    def reiniciar(self):
        """Reinicia el chatbot y limpia la sesión"""
        super().reiniciar()
        self.db.eliminar_sesion(self.telefono)


class GestorChatbots:
    """Gestor de múltiples instancias de chatbot"""
    
    def __init__(self):
        self.chatbots: Dict[str, ChatbotIntegrado] = {}
        self.evolution = get_evolution_api()
    
    def obtener_chatbot(self, telefono: str) -> ChatbotIntegrado:
        """Obtiene o crea un chatbot para un número de teléfono"""
        if telefono not in self.chatbots:
            self.chatbots[telefono] = ChatbotIntegrado(telefono)
        return self.chatbots[telefono]
    
    def procesar_mensaje_whatsapp(self, telefono: str, mensaje: str) -> str:
        """Procesa un mensaje de WhatsApp y retorna la respuesta"""
        chatbot = self.obtener_chatbot(telefono)
        
        # Si es el primer mensaje, iniciar el chatbot
        if chatbot.estado == EstadoConversacion.INICIO:
            respuesta = chatbot.procesar_mensaje("")
        else:
            respuesta = chatbot.procesar_mensaje(mensaje)
        
        return respuesta
    
    def enviar_respuesta(self, telefono: str, mensaje: str) -> Dict:
        """Envía una respuesta por WhatsApp"""
        return self.evolution.enviar_mensaje_texto(telefono, mensaje)
    
    def limpiar_sesion(self, telefono: str):
        """Limpia la sesión de un usuario"""
        if telefono in self.chatbots:
            self.chatbots[telefono].reiniciar()
            del self.chatbots[telefono]


# Singleton del gestor
_gestor_instance = None

def get_gestor_chatbots() -> GestorChatbots:
    """Obtiene la instancia singleton del gestor"""
    global _gestor_instance
    if _gestor_instance is None:
        _gestor_instance = GestorChatbots()
    return _gestor_instance
