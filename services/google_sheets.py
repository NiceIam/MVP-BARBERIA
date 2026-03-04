"""Cliente para Google Sheets API."""
import uuid
import json
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

from config.settings import (
    SERVICE_ACCOUNT_PATH, GOOGLE_SHEETS_ID, GOOGLE_SCOPES
)
from config.constants import (
    SHEET_CLIENTES, SHEET_CITAS, SHEET_SERVICIOS,
    SHEET_DISPONIBILIDAD, SHEET_SESIONES
)
from models import Cliente, Cita, Servicio, Sesion


class SheetsClient:
    """Cliente para interactuar con Google Sheets."""
    
    def __init__(self):
        """Inicializa el cliente de Google Sheets."""
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
                logger.info("✅ Credenciales cargadas desde variable de entorno")
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
            logger.info("✅ Credenciales cargadas desde archivo")
        
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = GOOGLE_SHEETS_ID
    
    def _read_range(self, range_name: str) -> List[List[Any]]:
        """Lee un rango del sheet."""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except HttpError as e:
            logger.error(f"Error leyendo rango {range_name}: {e}")
            return []
    
    def _append_row(self, sheet_name: str, values: List[Any]) -> bool:
        """Agrega una fila al sheet."""
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:Z",
                valueInputOption='RAW',
                body={'values': [values]}
            ).execute()
            return True
        except HttpError as e:
            logger.error(f"Error agregando fila a {sheet_name}: {e}")
            return False
    
    def _update_row(self, range_name: str, values: List[Any]) -> bool:
        """Actualiza una fila específica."""
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': [values]}
            ).execute()
            return True
        except HttpError as e:
            logger.error(f"Error actualizando {range_name}: {e}")
            return False
    
    # === CLIENTES ===
    
    def get_cliente_por_telefono(self, telefono: str) -> Optional[Cliente]:
        """Busca un cliente por teléfono."""
        rows = self._read_range(f"{SHEET_CLIENTES}!A2:F")
        for row in rows:
            if len(row) > 1 and row[1] == telefono:
                return Cliente.from_sheet_row(row)
        return None
    
    def crear_cliente(self, telefono: str, nombre: str) -> Cliente:
        """Crea un nuevo cliente."""
        cliente = Cliente(
            id=f"cli_{uuid.uuid4().hex[:8]}",
            telefono=telefono,
            nombre=nombre,
            fecha_registro=datetime.now(),
            total_citas=0
        )
        self._append_row(SHEET_CLIENTES, cliente.to_sheet_row())
        logger.info(f"Cliente creado: {cliente.id}")
        return cliente

    
    def actualizar_cliente(self, cliente: Cliente, row_index: int) -> bool:
        """Actualiza un cliente existente."""
        range_name = f"{SHEET_CLIENTES}!A{row_index}:F{row_index}"
        return self._update_row(range_name, cliente.to_sheet_row())
    
    # === CITAS ===
    
    def get_citas_por_telefono(self, telefono: str, solo_activas: bool = False) -> List[Cita]:
        """Obtiene todas las citas de un cliente."""
        rows = self._read_range(f"{SHEET_CITAS}!A2:O")
        citas = []
        for row in rows:
            if len(row) > 2 and row[2] == telefono:
                cita = Cita.from_sheet_row(row)
                if not solo_activas or cita.estado in ['confirmada', 'pendiente']:
                    citas.append(cita)
        return sorted(citas, key=lambda c: c.fecha)
    
    def get_citas_por_fecha(self, fecha: date) -> List[Cita]:
        """Obtiene todas las citas de una fecha."""
        rows = self._read_range(f"{SHEET_CITAS}!A2:O")
        citas = []
        fecha_str = fecha.strftime('%d/%m/%Y')
        for row in rows:
            if len(row) > 7 and row[7] == fecha_str:
                citas.append(Cita.from_sheet_row(row))
        return citas
    
    def crear_cita(self, cita: Cita) -> bool:
        """Crea una nueva cita."""
        cita.id = f"cita_{uuid.uuid4().hex[:8]}"
        cita.fecha_creacion = datetime.now()
        cita.fecha_modificacion = datetime.now()
        success = self._append_row(SHEET_CITAS, cita.to_sheet_row())
        if success:
            logger.info(f"Cita creada: {cita.id}")
        return success
    
    def actualizar_cita(self, cita: Cita, row_index: int) -> bool:
        """Actualiza una cita existente."""
        cita.fecha_modificacion = datetime.now()
        range_name = f"{SHEET_CITAS}!A{row_index}:O{row_index}"
        return self._update_row(range_name, cita.to_sheet_row())
    
    def get_cita_por_id(self, cita_id: str) -> Optional[tuple]:
        """Busca una cita por ID y retorna (cita, row_index)."""
        rows = self._read_range(f"{SHEET_CITAS}!A2:O")
        for idx, row in enumerate(rows, start=2):
            if len(row) > 0 and row[0] == cita_id:
                return Cita.from_sheet_row(row), idx
        return None

    
    # === SERVICIOS ===
    
    def get_servicios_activos(self) -> List[Servicio]:
        """Obtiene todos los servicios activos."""
        rows = self._read_range(f"{SHEET_SERVICIOS}!A2:F")
        servicios = []
        for row in rows:
            servicio = Servicio.from_sheet_row(row)
            if servicio.activo:
                servicios.append(servicio)
        return sorted(servicios, key=lambda s: s.orden)
    
    def get_servicio_por_id(self, servicio_id: str) -> Optional[Servicio]:
        """Busca un servicio por ID."""
        rows = self._read_range(f"{SHEET_SERVICIOS}!A2:F")
        for row in rows:
            if len(row) > 0 and row[0] == servicio_id:
                return Servicio.from_sheet_row(row)
        return None
    
    # === SESIONES ===
    
    def get_sesion(self, telefono: str) -> Optional[tuple]:
        """Obtiene la sesión de un usuario. Retorna (sesion, row_index)."""
        rows = self._read_range(f"{SHEET_SESIONES}!A2:E")
        for idx, row in enumerate(rows, start=2):
            if len(row) > 0 and row[0] == telefono:
                return Sesion.from_sheet_row(row), idx
        return None
    
    def crear_sesion(self, sesion: Sesion) -> bool:
        """Crea una nueva sesión."""
        return self._append_row(SHEET_SESIONES, sesion.to_sheet_row())
    
    def actualizar_sesion(self, sesion: Sesion, row_index: int) -> bool:
        """Actualiza una sesión existente."""
        sesion.ultima_actividad = datetime.now()
        range_name = f"{SHEET_SESIONES}!A{row_index}:E{row_index}"
        return self._update_row(range_name, sesion.to_sheet_row())
    
    def eliminar_sesion(self, telefono: str) -> bool:
        """Elimina una sesión."""
        result = self.get_sesion(telefono)
        if result:
            _, row_index = result
            # Limpiar la fila
            range_name = f"{SHEET_SESIONES}!A{row_index}:E{row_index}"
            return self._update_row(range_name, ["", "", "", "", ""])
        return False
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Google Sheets."""
        try:
            self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            logger.info("Conexión a Google Sheets exitosa")
            return True
        except Exception as e:
            logger.error(f"Error conectando a Google Sheets: {e}")
            return False
