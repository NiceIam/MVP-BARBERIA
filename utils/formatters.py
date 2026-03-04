"""Utilidades para formatear mensajes."""
from datetime import date, time
from models import Cita, Servicio


def formatear_precio(precio: int) -> str:
    """Formatea un precio en COP."""
    return f"${precio:,} COP"


def formatear_cita_resumen(cita: Cita) -> str:
    """Formatea un resumen de cita para mostrar al usuario."""
    from utils.datetime_utils import formatear_fecha, formatear_hora
    
    mensaje = f"""
📅 *Resumen de tu cita*

📆 Fecha: {formatear_fecha(cita.fecha)}
🕐 Hora: {formatear_hora(cita.hora_inicio)} - {formatear_hora(cita.hora_fin)}
✂️ Servicio: {cita.servicio_nombre}
💰 Precio: {formatear_precio(cita.precio)}
👨‍💼 Barbero: Churco
    """.strip()
    return mensaje


def formatear_confirmacion_cita(cita: Cita) -> str:
    """Formatea el mensaje de confirmación de cita."""
    from utils.datetime_utils import formatear_fecha, formatear_hora
    
    mensaje = f"""
✅ *¡Cita confirmada!*

📆 {formatear_fecha(cita.fecha)}
🕐 {formatear_hora(cita.hora_inicio)}
✂️ {cita.servicio_nombre}
💰 {formatear_precio(cita.precio)}

Te esperamos en Barbería Churco.
Recuerda llegar 5 minutos antes.

*No es necesario que respondas este mensaje*
    """.strip()
    return mensaje


def formatear_lista_citas(citas: list) -> str:
    """Formatea una lista de citas."""
    from utils.datetime_utils import formatear_fecha, formatear_hora
    
    if not citas:
        return "No tienes citas agendadas."
    
    if len(citas) == 1:
        return formatear_cita_resumen(citas[0])
    
    mensaje = f"*Tienes {len(citas)} citas agendadas:*\n\n"
    for idx, cita in enumerate(citas, 1):
        mensaje += f"{idx}. {formatear_fecha(cita.fecha)}\n"
        mensaje += f"   🕐 {formatear_hora(cita.hora_inicio)}\n"
        mensaje += f"   ✂️ {cita.servicio_nombre}\n\n"
    
    mensaje += "Responde con el número para ver detalles."
    return mensaje
