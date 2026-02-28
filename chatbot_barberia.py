"""
Chatbot para Barbería - Sistema de Gestión de Citas y Atención al Cliente
"""
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum


class EstadoConversacion(Enum):
    """Estados posibles de la conversación"""
    INICIO = "inicio"
    MENU_PRINCIPAL = "menu_principal"
    RESERVAR_CITA = "reservar_cita"
    SELECCIONAR_SERVICIO = "seleccionar_servicio"
    SELECCIONAR_BARBERO = "seleccionar_barbero"
    SELECCIONAR_FECHA = "seleccionar_fecha"
    SELECCIONAR_HORA = "seleccionar_hora"
    CONFIRMAR_DATOS = "confirmar_datos"
    CONSULTAR_CITA = "consultar_cita"
    CANCELAR_CITA = "cancelar_cita"
    VER_SERVICIOS = "ver_servicios"
    VER_PROMOCIONES = "ver_promociones"
    VER_BARBEROS = "ver_barberos"
    CONTACTO = "contacto"
    FINALIZADO = "finalizado"


class ChatbotBarberia:
    """Chatbot principal para gestión de barbería"""
    
    def __init__(self):
        self.estado = EstadoConversacion.INICIO
        self.datos_temporales = {}
        self.citas_agendadas = {}  # En producción, usar base de datos
        
        # Configuración de la barbería
        self.servicios = {
            "1": {"nombre": "Corte de Cabello", "precio": 15000, "duracion": 30},
            "2": {"nombre": "Corte + Barba", "precio": 25000, "duracion": 45},
            "3": {"nombre": "Barba", "precio": 12000, "duracion": 20},
            "4": {"nombre": "Corte Niño", "precio": 12000, "duracion": 25},
            "5": {"nombre": "Diseño/Degradado", "precio": 20000, "duracion": 40},
            "6": {"nombre": "Afeitado Clásico", "precio": 18000, "duracion": 35},
            "7": {"nombre": "Tratamiento Capilar", "precio": 30000, "duracion": 50},
        }
        
        self.barberos = {
            "1": {"nombre": "Carlos", "especialidad": "Cortes modernos"},
            "2": {"nombre": "Miguel", "especialidad": "Barbas y afeitados"},
            "3": {"nombre": "Juan", "especialidad": "Diseños y degradados"},
            "4": {"nombre": "Cualquier barbero disponible", "especialidad": "Todos los servicios"},
        }
        
        self.horarios_disponibles = self._generar_horarios()
        
        self.promociones = [
            "🎉 Lunes y Martes: 15% descuento en todos los servicios",
            "👨‍👦 Combo Padre e Hijo: 2x1 en cortes los domingos",
            "💳 Paga 5 cortes, lleva 6 (tarjeta de fidelidad)",
            "🎂 Descuento especial del 20% en tu cumpleaños",
        ]
        
        self.info_contacto = {
            "direccion": "Calle Principal #123, Centro",
            "telefono": "+57 300 123 4567",
            "horario": "Lunes a Sábado: 9:00 AM - 7:00 PM\nDomingo: 10:00 AM - 4:00 PM",
            "redes": "Instagram: @barberia_style\nFacebook: Barbería Style",
        }
    
    def _generar_horarios(self) -> Dict:
        """Genera horarios disponibles para los próximos 7 días"""
        horarios = {}
        hoy = datetime.now()
        
        for i in range(1, 8):
            fecha = hoy + timedelta(days=i)
            fecha_str = fecha.strftime("%Y-%m-%d")
            dia_semana = fecha.strftime("%A")
            
            # Horarios según el día
            if dia_semana == "Sunday":
                horas = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
            else:
                horas = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
            
            horarios[fecha_str] = horas
        
        return horarios

    
    def procesar_mensaje(self, mensaje: str) -> str:
        """Procesa el mensaje del usuario y retorna la respuesta"""
        mensaje = mensaje.strip().lower()
        
        if self.estado == EstadoConversacion.INICIO:
            return self._estado_inicio()
        
        elif self.estado == EstadoConversacion.MENU_PRINCIPAL:
            return self._estado_menu_principal(mensaje)
        
        elif self.estado == EstadoConversacion.SELECCIONAR_SERVICIO:
            return self._estado_seleccionar_servicio(mensaje)
        
        elif self.estado == EstadoConversacion.SELECCIONAR_BARBERO:
            return self._estado_seleccionar_barbero(mensaje)
        
        elif self.estado == EstadoConversacion.SELECCIONAR_FECHA:
            return self._estado_seleccionar_fecha(mensaje)
        
        elif self.estado == EstadoConversacion.SELECCIONAR_HORA:
            return self._estado_seleccionar_hora(mensaje)
        
        elif self.estado == EstadoConversacion.CONFIRMAR_DATOS:
            return self._estado_confirmar_datos(mensaje)
        
        elif self.estado == EstadoConversacion.VER_SERVICIOS:
            return self._estado_ver_servicios(mensaje)
        
        elif self.estado == EstadoConversacion.VER_PROMOCIONES:
            return self._estado_ver_promociones(mensaje)
        
        elif self.estado == EstadoConversacion.VER_BARBEROS:
            return self._estado_ver_barberos(mensaje)
        
        elif self.estado == EstadoConversacion.CONSULTAR_CITA:
            return self._estado_consultar_cita(mensaje)
        
        elif self.estado == EstadoConversacion.CANCELAR_CITA:
            return self._estado_cancelar_cita(mensaje)
        
        elif self.estado == EstadoConversacion.CONTACTO:
            return self._estado_contacto(mensaje)
        
        return "Lo siento, algo salió mal. Escribe 'menu' para volver al inicio."
    
    def _estado_inicio(self) -> str:
        """Estado inicial del chatbot"""
        self.estado = EstadoConversacion.MENU_PRINCIPAL
        return """
¡Bienvenido a Barbería Style! 💈✨

Soy tu asistente virtual y estoy aquí para ayudarte.

¿Qué te gustaría hacer hoy?

1️⃣ Reservar una cita
2️⃣ Consultar mi cita
3️⃣ Cancelar mi cita
4️⃣ Ver servicios y precios
5️⃣ Ver promociones
6️⃣ Conocer nuestros barberos
7️⃣ Información de contacto

Escribe el número de la opción que deseas o describe lo que necesitas.
"""
    
    def _estado_menu_principal(self, mensaje: str) -> str:
        """Maneja el menú principal"""
        # Detectar intención por palabras clave
        if any(word in mensaje for word in ["1", "reservar", "agendar", "cita", "turno"]):
            self.estado = EstadoConversacion.SELECCIONAR_SERVICIO
            self.datos_temporales = {}
            return self._mostrar_servicios()
        
        elif any(word in mensaje for word in ["2", "consultar", "ver cita", "mi cita"]):
            self.estado = EstadoConversacion.CONSULTAR_CITA
            return """
Para consultar tu cita, por favor proporciona:
- Tu nombre completo, o
- Tu número de teléfono

Ejemplo: "Juan Pérez" o "3001234567"
"""
        
        elif any(word in mensaje for word in ["3", "cancelar", "eliminar"]):
            self.estado = EstadoConversacion.CANCELAR_CITA
            return """
Para cancelar tu cita, necesito:
- Tu nombre completo, o
- Tu número de teléfono

Ejemplo: "Juan Pérez" o "3001234567"
"""
        
        elif any(word in mensaje for word in ["4", "servicios", "precios", "cuanto"]):
            self.estado = EstadoConversacion.VER_SERVICIOS
            return self._mostrar_servicios_detallados()
        
        elif any(word in mensaje for word in ["5", "promociones", "ofertas", "descuentos"]):
            self.estado = EstadoConversacion.VER_PROMOCIONES
            return self._mostrar_promociones()
        
        elif any(word in mensaje for word in ["6", "barberos", "estilistas", "equipo"]):
            self.estado = EstadoConversacion.VER_BARBEROS
            return self._mostrar_barberos()
        
        elif any(word in mensaje for word in ["7", "contacto", "ubicacion", "direccion", "telefono"]):
            self.estado = EstadoConversacion.CONTACTO
            return self._mostrar_contacto()
        
        else:
            return """
No entendí tu solicitud. Por favor, elige una opción:

1️⃣ Reservar una cita
2️⃣ Consultar mi cita
3️⃣ Cancelar mi cita
4️⃣ Ver servicios y precios
5️⃣ Ver promociones
6️⃣ Conocer nuestros barberos
7️⃣ Información de contacto

Escribe el número o describe lo que necesitas.
"""
    
    def _mostrar_servicios(self) -> str:
        """Muestra los servicios disponibles para reservar"""
        texto = "📋 Selecciona el servicio que deseas:\n\n"
        for key, servicio in self.servicios.items():
            texto += f"{key}. {servicio['nombre']} - ${servicio['precio']:,} ({servicio['duracion']} min)\n"
        texto += "\nEscribe el número del servicio que deseas."
        return texto
    
    def _estado_seleccionar_servicio(self, mensaje: str) -> str:
        """Maneja la selección de servicio"""
        if mensaje in self.servicios:
            self.datos_temporales["servicio"] = self.servicios[mensaje]
            self.estado = EstadoConversacion.SELECCIONAR_BARBERO
            return self._mostrar_barberos_seleccion()
        else:
            return "Por favor, selecciona un número válido de servicio:\n\n" + self._mostrar_servicios()
    
    def _mostrar_barberos_seleccion(self) -> str:
        """Muestra barberos para selección"""
        texto = "👨‍💼 ¿Con qué barbero prefieres tu cita?\n\n"
        for key, barbero in self.barberos.items():
            texto += f"{key}. {barbero['nombre']} - {barbero['especialidad']}\n"
        texto += "\nEscribe el número del barbero que prefieres."
        return texto
    
    def _estado_seleccionar_barbero(self, mensaje: str) -> str:
        """Maneja la selección de barbero"""
        if mensaje in self.barberos:
            self.datos_temporales["barbero"] = self.barberos[mensaje]
            self.estado = EstadoConversacion.SELECCIONAR_FECHA
            return self._mostrar_fechas()
        else:
            return "Por favor, selecciona un número válido de barbero:\n\n" + self._mostrar_barberos_seleccion()
    
    def _mostrar_fechas(self) -> str:
        """Muestra fechas disponibles"""
        texto = "📅 Selecciona la fecha de tu cita:\n\n"
        fechas_lista = list(self.horarios_disponibles.keys())
        
        for i, fecha in enumerate(fechas_lista, 1):
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            dia_semana = self._traducir_dia(fecha_obj.strftime("%A"))
            fecha_formato = fecha_obj.strftime("%d/%m/%Y")
            texto += f"{i}. {dia_semana} {fecha_formato}\n"
        
        texto += "\nEscribe el número de la fecha que prefieres."
        return texto
    
    def _traducir_dia(self, dia_ingles: str) -> str:
        """Traduce días de la semana"""
        dias = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }
        return dias.get(dia_ingles, dia_ingles)
    
    def _estado_seleccionar_fecha(self, mensaje: str) -> str:
        """Maneja la selección de fecha"""
        try:
            indice = int(mensaje) - 1
            fechas_lista = list(self.horarios_disponibles.keys())
            
            if 0 <= indice < len(fechas_lista):
                fecha_seleccionada = fechas_lista[indice]
                self.datos_temporales["fecha"] = fecha_seleccionada
                self.estado = EstadoConversacion.SELECCIONAR_HORA
                return self._mostrar_horas(fecha_seleccionada)
            else:
                return "Por favor, selecciona un número válido de fecha:\n\n" + self._mostrar_fechas()
        except ValueError:
            return "Por favor, escribe el número de la fecha:\n\n" + self._mostrar_fechas()
    
    def _mostrar_horas(self, fecha: str) -> str:
        """Muestra horas disponibles para una fecha"""
        horas = self.horarios_disponibles.get(fecha, [])
        texto = "🕐 Selecciona la hora de tu cita:\n\n"
        
        for i, hora in enumerate(horas, 1):
            texto += f"{i}. {hora}\n"
        
        texto += "\nEscribe el número de la hora que prefieres."
        return texto
    
    def _estado_seleccionar_hora(self, mensaje: str) -> str:
        """Maneja la selección de hora"""
        try:
            fecha = self.datos_temporales["fecha"]
            horas = self.horarios_disponibles.get(fecha, [])
            indice = int(mensaje) - 1
            
            if 0 <= indice < len(horas):
                self.datos_temporales["hora"] = horas[indice]
                self.estado = EstadoConversacion.CONFIRMAR_DATOS
                return self._solicitar_datos_cliente()
            else:
                return "Por favor, selecciona un número válido de hora:\n\n" + self._mostrar_horas(fecha)
        except ValueError:
            return "Por favor, escribe el número de la hora:\n\n" + self._mostrar_horas(self.datos_temporales["fecha"])
    
    def _solicitar_datos_cliente(self) -> str:
        """Solicita datos del cliente para confirmar"""
        return """
Para confirmar tu cita, necesito tus datos:

Por favor, proporciona tu información en este formato:
Nombre: [Tu nombre completo]
Teléfono: [Tu número de teléfono]

Ejemplo:
Nombre: Juan Pérez
Teléfono: 3001234567
"""
    
    def _estado_confirmar_datos(self, mensaje: str) -> str:
        """Confirma los datos y agenda la cita"""
        # Extraer nombre y teléfono
        nombre_match = re.search(r'nombre:\s*(.+?)(?:\n|teléfono|telefono|$)', mensaje, re.IGNORECASE)
        telefono_match = re.search(r'(?:teléfono|telefono):\s*(\d+)', mensaje, re.IGNORECASE)
        
        if nombre_match and telefono_match:
            nombre = nombre_match.group(1).strip()
            telefono = telefono_match.group(1).strip()
            
            # Crear la cita
            cita_id = f"{telefono}_{self.datos_temporales['fecha']}"
            
            self.citas_agendadas[cita_id] = {
                "nombre": nombre,
                "telefono": telefono,
                "servicio": self.datos_temporales["servicio"]["nombre"],
                "precio": self.datos_temporales["servicio"]["precio"],
                "barbero": self.datos_temporales["barbero"]["nombre"],
                "fecha": self.datos_temporales["fecha"],
                "hora": self.datos_temporales["hora"],
            }
            
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
        else:
            return """
No pude identificar tus datos. Por favor, usa este formato:

Nombre: [Tu nombre completo]
Teléfono: [Tu número de teléfono]

Ejemplo:
Nombre: Juan Pérez
Teléfono: 3001234567
"""

    
    def _mostrar_servicios_detallados(self) -> str:
        """Muestra todos los servicios con detalles"""
        texto = """
💈 NUESTROS SERVICIOS Y PRECIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for servicio in self.servicios.values():
            texto += f"✂️ {servicio['nombre']}\n"
            texto += f"   💰 Precio: ${servicio['precio']:,}\n"
            texto += f"   ⏱️ Duración: {servicio['duracion']} minutos\n\n"
        
        texto += "\n¿Deseas reservar una cita? Escribe 'reservar' o 'menu' para volver."
        return texto
    
    def _estado_ver_servicios(self, mensaje: str) -> str:
        """Maneja el estado de ver servicios"""
        if "reservar" in mensaje or "agendar" in mensaje:
            self.estado = EstadoConversacion.SELECCIONAR_SERVICIO
            self.datos_temporales = {}
            return self._mostrar_servicios()
        elif "menu" in mensaje:
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return self._estado_inicio()
        else:
            return "Escribe 'reservar' para agendar una cita o 'menu' para volver al inicio."
    
    def _mostrar_promociones(self) -> str:
        """Muestra las promociones actuales"""
        texto = """
🎁 PROMOCIONES ESPECIALES
━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for promo in self.promociones:
            texto += f"{promo}\n\n"
        
        texto += "\n💡 ¡Aprovecha nuestras ofertas!\n"
        texto += "\n¿Deseas reservar una cita? Escribe 'reservar' o 'menu' para volver."
        return texto
    
    def _estado_ver_promociones(self, mensaje: str) -> str:
        """Maneja el estado de ver promociones"""
        if "reservar" in mensaje or "agendar" in mensaje:
            self.estado = EstadoConversacion.SELECCIONAR_SERVICIO
            self.datos_temporales = {}
            return self._mostrar_servicios()
        elif "menu" in mensaje:
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return self._estado_inicio()
        else:
            return "Escribe 'reservar' para agendar una cita o 'menu' para volver al inicio."
    
    def _mostrar_barberos(self) -> str:
        """Muestra información de los barberos"""
        texto = """
👨‍💼 NUESTRO EQUIPO DE BARBEROS
━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for barbero in list(self.barberos.values())[:-1]:  # Excluir "cualquier barbero"
            texto += f"✂️ {barbero['nombre']}\n"
            texto += f"   🎯 Especialidad: {barbero['especialidad']}\n\n"
        
        texto += "\n💡 Todos nuestros barberos están altamente capacitados.\n"
        texto += "\n¿Deseas reservar una cita? Escribe 'reservar' o 'menu' para volver."
        return texto
    
    def _estado_ver_barberos(self, mensaje: str) -> str:
        """Maneja el estado de ver barberos"""
        if "reservar" in mensaje or "agendar" in mensaje:
            self.estado = EstadoConversacion.SELECCIONAR_SERVICIO
            self.datos_temporales = {}
            return self._mostrar_servicios()
        elif "menu" in mensaje:
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return self._estado_inicio()
        else:
            return "Escribe 'reservar' para agendar una cita o 'menu' para volver al inicio."
    
    def _mostrar_contacto(self) -> str:
        """Muestra información de contacto"""
        texto = f"""
📍 INFORMACIÓN DE CONTACTO
━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Dirección:
   {self.info_contacto['direccion']}

📞 Teléfono:
   {self.info_contacto['telefono']}

🕐 Horario de Atención:
   {self.info_contacto['horario']}

📱 Redes Sociales:
   {self.info_contacto['redes']}

━━━━━━━━━━━━━━━━━━━━━━━━━

¿Deseas reservar una cita? Escribe 'reservar' o 'menu' para volver.
"""
        return texto
    
    def _estado_contacto(self, mensaje: str) -> str:
        """Maneja el estado de contacto"""
        if "reservar" in mensaje or "agendar" in mensaje:
            self.estado = EstadoConversacion.SELECCIONAR_SERVICIO
            self.datos_temporales = {}
            return self._mostrar_servicios()
        elif "menu" in mensaje:
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return self._estado_inicio()
        else:
            return "Escribe 'reservar' para agendar una cita o 'menu' para volver al inicio."
    
    def _estado_consultar_cita(self, mensaje: str) -> str:
        """Consulta una cita existente"""
        # Buscar por teléfono o nombre
        citas_encontradas = []
        
        for cita_id, cita in self.citas_agendadas.items():
            if mensaje in cita["telefono"].lower() or mensaje in cita["nombre"].lower():
                citas_encontradas.append(cita)
        
        if citas_encontradas:
            texto = "📋 Citas encontradas:\n\n"
            for cita in citas_encontradas:
                fecha_obj = datetime.strptime(cita["fecha"], "%Y-%m-%d")
                fecha_formato = fecha_obj.strftime("%d/%m/%Y")
                
                texto += f"""
━━━━━━━━━━━━━━━━━━━━
👤 Cliente: {cita['nombre']}
📞 Teléfono: {cita['telefono']}
✂️ Servicio: {cita['servicio']}
💰 Precio: ${cita['precio']:,}
👨‍💼 Barbero: {cita['barbero']}
📅 Fecha: {fecha_formato}
🕐 Hora: {cita['hora']}
━━━━━━━━━━━━━━━━━━━━

"""
            texto += "\n¿Necesitas algo más? Escribe 'menu' para volver al inicio."
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return texto
        else:
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return """
❌ No encontré citas con esa información.

Verifica que hayas escrito correctamente tu nombre o teléfono.

Escribe 'menu' para volver al inicio.
"""
    
    def _estado_cancelar_cita(self, mensaje: str) -> str:
        """Cancela una cita existente"""
        # Buscar citas por teléfono o nombre
        citas_encontradas = []
        citas_ids = []
        
        for cita_id, cita in self.citas_agendadas.items():
            if mensaje in cita["telefono"].lower() or mensaje in cita["nombre"].lower():
                citas_encontradas.append(cita)
                citas_ids.append(cita_id)
        
        if citas_encontradas:
            # Cancelar todas las citas encontradas
            for cita_id in citas_ids:
                del self.citas_agendadas[cita_id]
            
            texto = f"""
✅ Cita(s) cancelada(s) exitosamente.

Se cancelaron {len(citas_encontradas)} cita(s).

💡 Recuerda que puedes agendar una nueva cita cuando lo desees.

¿Necesitas algo más? Escribe 'menu' para volver al inicio.
"""
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return texto
        else:
            self.estado = EstadoConversacion.MENU_PRINCIPAL
            return """
❌ No encontré citas con esa información.

Verifica que hayas escrito correctamente tu nombre o teléfono.

Escribe 'menu' para volver al inicio.
"""
    
    def reiniciar(self):
        """Reinicia el chatbot al estado inicial"""
        self.estado = EstadoConversacion.INICIO
        self.datos_temporales = {}


def main():
    """Función principal para ejecutar el chatbot en consola"""
    print("=" * 60)
    print("💈 CHATBOT BARBERÍA STYLE 💈")
    print("=" * 60)
    print("\nEscribe 'salir' en cualquier momento para terminar.\n")
    
    chatbot = ChatbotBarberia()
    print(chatbot.procesar_mensaje(""))
    
    while True:
        try:
            mensaje_usuario = input("\n👤 Tú: ").strip()
            
            if mensaje_usuario.lower() in ["salir", "exit", "quit", "adios", "chao"]:
                print("\n👋 ¡Gracias por usar Barbería Style! ¡Hasta pronto!\n")
                break
            
            if mensaje_usuario.lower() == "menu":
                chatbot.reiniciar()
                respuesta = chatbot.procesar_mensaje("")
            else:
                respuesta = chatbot.procesar_mensaje(mensaje_usuario)
            
            print(f"\n🤖 Asistente:\n{respuesta}")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Escribe 'menu' para volver al inicio.\n")


if __name__ == "__main__":
    main()
