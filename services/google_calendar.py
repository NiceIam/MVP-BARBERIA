"""Cliente para Google Calendar API."""
import json
from datetime import datetime, date, time, timedelta
from typing import List, Optional, Dict, Any
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

from config.settings import (
    SERVICE_ACCOUNT_PATH, GOOGLE_CALENDAR_ID,
    GOOGLE_SCOPES, TIMEZONE
)
from config.constants import (
    COLOR_CONFIRMADA, COLOR_CANCELADA,
    COLOR_PENDIENTE, COLOR_COMPLETADA
)


class CalendarClient:
    """Cliente para interactuar con Google Calendar."""
    
    def __init__(self):
        """Inicializa el cliente de Google Calendar."""
        import os
        
        # Intentar leer desde variable de entorno primero
        service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
        
        if service_account_json and service_account_json.startswith('{'):
            # Es un JSON string en el .env
            try:
                service_account_info = json.loads(service_account_json)
                self.credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=GOOGLE_SCOPES
                )
                logger.info("✅ Credenciales Calendar cargadas desde variable de entorno")
            except json.JSONDecodeError as e:
                raise ValueError(f"❌ Error parseando JSON de credenciales: {e}")
        else:
            # Es un path a archivo
            if not SERVICE_ACCOUNT_PATH.exists():
                raise FileNotFoundError(
                    f"❌ Archivo de credenciales no encontrado: {SERVICE_ACCOUNT_PATH}\n"
                    f"   Opción 1: Descarga service_account.json y colócalo en la raíz\n"
                    f"   Opción 2: Pon el JSON completo en GOOGLE_SERVICE_ACCOUNT_FILE del .env"
                )
            
            self.credentials = service_account.Credentials.from_service_account_file(
                str(SERVICE_ACCOUNT_PATH),
                scopes=GOOGLE_SCOPES
            )
            logger.info("✅ Credenciales Calendar cargadas desde archivo")
        
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.calendar_id = GOOGLE_CALENDAR_ID
        self.timezone = pytz.timezone(TIMEZONE)
    
    def _crear_datetime_local(self, fecha: date, hora: time) -> datetime:
        """Crea un datetime con timezone correcto."""
        dt = datetime.combine(fecha, hora)
        return self.timezone.localize(dt)
    
    def crear_evento(
        self,
        cita_id: str,
        cliente_nombre: str,
        cliente_telefono: str,
        servicio_nombre: str,
        precio: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        estado: str = "confirmada"
    ) -> Optional[str]:
        """Crea un evento en Google Calendar."""
        try:
            dt_inicio = self._crear_datetime_local(fecha, hora_inicio)
            dt_fin = self._crear_datetime_local(fecha, hora_fin)
            
            logger.info(f"📅 Creando evento en Calendar para cita {cita_id}")
            logger.debug(f"   Fecha: {fecha}, Hora: {hora_inicio} - {hora_fin}")
            logger.debug(f"   Calendar ID: {self.calendar_id}")
            
            # Determinar color según estado
            color_map = {
                "confirmada": COLOR_CONFIRMADA,
                "pendiente": COLOR_PENDIENTE,
                "completada": COLOR_COMPLETADA,
                "cancelada": COLOR_CANCELADA
            }
            color_id = color_map.get(estado, COLOR_CONFIRMADA)

            
            evento = {
                "summary": f"{servicio_nombre} - {cliente_nombre}",
                "description": (
                    f"Cliente: {cliente_nombre}\n"
                    f"Teléfono: +{cliente_telefono}\n"
                    f"Servicio: {servicio_nombre}\n"
                    f"Precio: ${precio:,} COP\n"
                    f"ID Cita: {cita_id}"
                ),
                "start": {
                    "dateTime": dt_inicio.isoformat(),
                    "timeZone": TIMEZONE
                },
                "end": {
                    "dateTime": dt_fin.isoformat(),
                    "timeZone": TIMEZONE
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 60},
                        {"method": "popup", "minutes": 15}
                    ]
                },
                "colorId": color_id,
                "extendedProperties": {
                    "private": {
                        "cita_id": cita_id,
                        "cliente_telefono": cliente_telefono,
                        "precio": str(precio)
                    }
                }
            }
            
            result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=evento
            ).execute()
            
            event_id = result.get('id')
            if event_id:
                logger.info(f"✅ Evento creado en Calendar: {event_id}")
            else:
                logger.error(f"❌ Evento creado pero sin ID en respuesta: {result}")
            
            return event_id
            
        except HttpError as e:
            logger.error(f"❌ Error HTTP creando evento: {e}")
            logger.error(f"   Detalles: {e.content if hasattr(e, 'content') else 'N/A'}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado creando evento: {e}")
            return None
    
    def eliminar_evento(self, event_id: str) -> bool:
        """Elimina un evento de Google Calendar."""
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            logger.info(f"Evento eliminado: {event_id}")
            return True
        except HttpError as e:
            logger.error(f"Error eliminando evento {event_id}: {e}")
            return False

    
    def actualizar_evento(
        self,
        event_id: str,
        fecha: date,
        hora_inicio: time,
        hora_fin: time
    ) -> bool:
        """Actualiza la fecha/hora de un evento."""
        dt_inicio = self._crear_datetime_local(fecha, hora_inicio)
        dt_fin = self._crear_datetime_local(fecha, hora_fin)
        
        try:
            evento = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            evento['start'] = {
                "dateTime": dt_inicio.isoformat(),
                "timeZone": TIMEZONE
            }
            evento['end'] = {
                "dateTime": dt_fin.isoformat(),
                "timeZone": TIMEZONE
            }
            
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=evento
            ).execute()
            
            logger.info(f"Evento actualizado: {event_id}")
            return True
        except HttpError as e:
            logger.error(f"Error actualizando evento {event_id}: {e}")
            return False
    
    def get_eventos_dia(self, fecha: date) -> List[Dict[str, Any]]:
        """Obtiene todos los eventos de un día."""
        dt_inicio = self._crear_datetime_local(fecha, time(0, 0))
        dt_fin = self._crear_datetime_local(fecha, time(23, 59))
        
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=dt_inicio.isoformat(),
                timeMax=dt_fin.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            eventos = events_result.get('items', [])
            return [e for e in eventos if e.get('status') != 'cancelled']
        except HttpError as e:
            logger.error(f"Error obteniendo eventos del día {fecha}: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Google Calendar."""
        try:
            self.service.calendarList().get(
                calendarId=self.calendar_id
            ).execute()
            logger.info("Conexión a Google Calendar exitosa")
            return True
        except Exception as e:
            logger.error(f"Error conectando a Google Calendar: {e}")
            return False
