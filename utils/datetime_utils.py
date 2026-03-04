"""Utilidades para manejo de fechas y horas."""
from datetime import datetime, date, time, timedelta
from typing import List
import pytz

from config.settings import TIMEZONE


def get_timezone():
    """Retorna el timezone configurado."""
    return pytz.timezone(TIMEZONE)


def get_fecha_actual() -> date:
    """Retorna la fecha actual en el timezone configurado."""
    tz = get_timezone()
    return datetime.now(tz).date()


def get_datetime_actual() -> datetime:
    """Retorna el datetime actual en el timezone configurado."""
    tz = get_timezone()
    return datetime.now(tz)


def get_proximas_fechas(dias: int = 7) -> List[date]:
    """Retorna las próximas N fechas desde hoy."""
    fecha_actual = get_fecha_actual()
    fecha_inicio_agendamiento = date(2026, 3, 9)  # Primer día disponible para agendar
    
    # Si estamos antes del 09/03/2026, comenzar desde esa fecha
    if fecha_actual < fecha_inicio_agendamiento:
        fecha_inicio = fecha_inicio_agendamiento
    else:
        fecha_inicio = fecha_actual
    
    return [fecha_inicio + timedelta(days=i) for i in range(dias)]


def es_fecha_valida(fecha: date) -> bool:
    """Verifica si una fecha es válida para agendar."""
    fecha_minima = date(2026, 3, 9)  # Primer día disponible para agendar
    hoy = get_fecha_actual()
    
    # La fecha mínima es la mayor entre hoy y el 09/03/2026
    fecha_inicio = max(hoy, fecha_minima)
    max_fecha = fecha_inicio + timedelta(days=30)
    
    return fecha_inicio <= fecha <= max_fecha


def es_hora_futura(fecha: date, hora: time) -> bool:
    """Verifica si una hora es futura (si la fecha es hoy)."""
    if fecha == get_fecha_actual():
        ahora = get_datetime_actual().time()
        return hora > ahora
    return True


def calcular_hora_fin(hora_inicio: time, duracion_minutos: int) -> time:
    """Calcula la hora de fin dado un inicio y duración."""
    dt = datetime.combine(date.today(), hora_inicio)
    dt_fin = dt + timedelta(minutes=duracion_minutos)
    return dt_fin.time()


def formatear_fecha(fecha: date) -> str:
    """Formatea una fecha para mostrar al usuario."""
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dia_nombre = dias_semana[fecha.weekday()]
    return f"{dia_nombre} {fecha.strftime('%d/%m/%Y')}"


def formatear_hora(hora: time) -> str:
    """Formatea una hora para mostrar al usuario."""
    return hora.strftime('%I:%M %p')
