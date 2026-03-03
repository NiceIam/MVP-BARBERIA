"""Servicio de mensajería WhatsApp."""
from typing import Optional
from loguru import logger

from .evolution_api import EvolutionAPI


class WhatsAppService:
    """Servicio para enviar mensajes por WhatsApp."""
    
    def __init__(self):
        """Inicializa el servicio de WhatsApp."""
        self.evolution = EvolutionAPI()
    
    def enviar_mensaje(self, telefono: str, mensaje: str) -> bool:
        """Envía un mensaje por WhatsApp."""
        return self.evolution.send_message(telefono, mensaje)
    
    def enviar_menu_principal(self, telefono: str) -> bool:
        """Envía el menú principal."""
        mensaje = """
🏠 *Bienvenido a Barbería Churco*

¿Qué deseas hacer?

1️⃣ Agendar cita
2️⃣ Consultar mi cita
3️⃣ Cancelar cita
4️⃣ Reagendar cita

Responde con el número de la opción.
        """.strip()
        return self.enviar_mensaje(telefono, mensaje)
    
    def enviar_servicios(self, telefono: str, servicios: list) -> bool:
        """Envía la lista de servicios."""
        mensaje = "✂️ *Selecciona tu servicio:*\n\n"
        for idx, servicio in enumerate(servicios, 1):
            mensaje += f"{idx}️⃣ {servicio.nombre}\n"
            mensaje += f"   💰 ${servicio.precio:,} COP\n"
            mensaje += f"   ⏱️ {servicio.duracion_minutos} minutos\n\n"
        mensaje += "Responde con el número del servicio."
        return self.enviar_mensaje(telefono, mensaje)
    
    def enviar_fechas(self, telefono: str, fechas: list) -> bool:
        """Envía opciones de fechas disponibles."""
        mensaje = "📅 *¿Qué día prefieres?*\n\n"
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        for idx, fecha in enumerate(fechas, 1):
            dia_nombre = dias_semana[fecha.weekday()]
            mensaje += f"{idx}️⃣ {dia_nombre} {fecha.strftime('%d/%m/%Y')}\n"
        mensaje += "\nResponde con el número del día."
        return self.enviar_mensaje(telefono, mensaje)
    
    def enviar_horas(self, telefono: str, horas: list) -> bool:
        """Envía opciones de horas disponibles."""
        mensaje = "🕐 *¿A qué hora?*\n\n"
        for idx, hora in enumerate(horas, 1):
            mensaje += f"{idx}️⃣ {hora.strftime('%I:%M %p')}\n"
        mensaje += "\nResponde con el número de la hora."
        return self.enviar_mensaje(telefono, mensaje)
