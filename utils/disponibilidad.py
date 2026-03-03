"""Utilidades para calcular disponibilidad de horarios."""
from datetime import datetime, date, time, timedelta
from typing import List, Tuple
from loguru import logger

from config.constants import HORARIOS_ATENCION
from config.settings import SLOT_INTERVAL_MINUTES


def hay_solapamiento(
    a_inicio: time,
    a_fin: time,
    b_inicio: time,
    b_fin: time
) -> bool:
    """Verifica si dos rangos de tiempo se solapan."""
    # Convertir a minutos desde medianoche para comparar
    a_inicio_min = a_inicio.hour * 60 + a_inicio.minute
    a_fin_min = a_fin.hour * 60 + a_fin.minute
    b_inicio_min = b_inicio.hour * 60 + b_inicio.minute
    b_fin_min = b_fin.hour * 60 + b_fin.minute
    
    return a_inicio_min < b_fin_min and b_inicio_min < a_fin_min


def generar_slots_dia(duracion_minutos: int) -> List[time]:
    """Genera todos los slots posibles para un día según horarios de atención."""
    slots = []
    
    for bloque in HORARIOS_ATENCION:
        hora_actual = bloque['hora_inicio']
        hora_fin_bloque = bloque['hora_fin']
        
        # Convertir a datetime para hacer aritmética
        dt_actual = datetime.combine(date.today(), hora_actual)
        dt_fin_bloque = datetime.combine(date.today(), hora_fin_bloque)
        
        while True:
            # Verificar que el slot completo quepa en el bloque
            dt_fin_slot = dt_actual + timedelta(minutes=duracion_minutos)
            
            if dt_fin_slot <= dt_fin_bloque:
                slots.append(dt_actual.time())
                dt_actual += timedelta(minutes=SLOT_INTERVAL_MINUTES)
            else:
                break
    
    return slots


def filtrar_slots_ocupados(
    slots_disponibles: List[time],
    citas_dia: list,
    eventos_calendar: list,
    duracion_minutos: int
) -> List[time]:
    """Filtra los slots que están ocupados."""
    slots_libres = []
    
    for slot in slots_disponibles:
        slot_fin = (datetime.combine(date.today(), slot) + 
                   timedelta(minutes=duracion_minutos)).time()
        
        ocupado = False
        
        # Verificar contra citas en Sheets
        for cita in citas_dia:
            if cita.estado in ['confirmada', 'pendiente']:
                if hay_solapamiento(slot, slot_fin, cita.hora_inicio, cita.hora_fin):
                    ocupado = True
                    break
        
        # Verificar contra eventos en Calendar
        if not ocupado:
            for evento in eventos_calendar:
                # Verificar si es evento de todo el día
                if 'date' in evento.get('start', {}):
                    # Evento de todo el día - bloquea todos los slots
                    ocupado = True
                    break
                
                # Extraer hora de inicio y fin del evento con hora específica
                start_str = evento.get('start', {}).get('dateTime', '')
                end_str = evento.get('end', {}).get('dateTime', '')
                
                if start_str and end_str:
                    try:
                        # Manejar diferentes formatos de timezone
                        if 'Z' in start_str:
                            start_str = start_str.replace('Z', '+00:00')
                        if 'Z' in end_str:
                            end_str = end_str.replace('Z', '+00:00')
                        
                        evento_inicio = datetime.fromisoformat(start_str).time()
                        evento_fin = datetime.fromisoformat(end_str).time()
                        
                        if hay_solapamiento(slot, slot_fin, evento_inicio, evento_fin):
                            ocupado = True
                            break
                    except (ValueError, AttributeError) as e:
                        logger.warning(f"Error parseando evento de Calendar: {e}")
                        continue
        
        if not ocupado:
            slots_libres.append(slot)
    
    return slots_libres


def obtener_slots_disponibles(
    fecha: date,
    duracion_minutos: int,
    citas_dia: list,
    eventos_calendar: list
) -> List[time]:
    """
    Obtiene todos los slots disponibles para una fecha.
    
    Args:
        fecha: Fecha para la cual calcular disponibilidad
        duracion_minutos: Duración del servicio en minutos
        citas_dia: Lista de citas existentes en esa fecha
        eventos_calendar: Lista de eventos de Calendar en esa fecha
    
    Returns:
        Lista de horas disponibles
    """
    # Generar todos los slots posibles
    slots_posibles = generar_slots_dia(duracion_minutos)
    
    # Filtrar slots ocupados
    slots_disponibles = filtrar_slots_ocupados(
        slots_posibles,
        citas_dia,
        eventos_calendar,
        duracion_minutos
    )
    
    # Si es hoy, filtrar horas pasadas
    from utils.datetime_utils import get_fecha_actual, get_datetime_actual
    if fecha == get_fecha_actual():
        ahora = get_datetime_actual().time()
        slots_disponibles = [s for s in slots_disponibles if s > ahora]
    
    logger.info(f"Slots disponibles para {fecha}: {len(slots_disponibles)}")
    return slots_disponibles
