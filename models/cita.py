"""Modelo de Cita."""
from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional


@dataclass
class Cita:
    """Representa una cita en la barbería."""
    
    id: str
    cliente_id: str
    cliente_telefono: str
    cliente_nombre: str
    servicio_id: str
    servicio_nombre: str
    precio: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str
    calendar_event_id: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    notas: str = ""
    
    @classmethod
    def from_sheet_row(cls, row: list) -> 'Cita':
        """Crea una Cita desde una fila de Google Sheets."""
        # Parsear fecha con soporte para ambos formatos
        fecha_obj = date.today()
        if len(row) > 7 and row[7]:
            try:
                # Intentar formato nuevo DD/MM/YYYY
                fecha_obj = datetime.strptime(row[7], '%d/%m/%Y').date()
            except ValueError:
                try:
                    # Intentar formato antiguo YYYY-MM-DD
                    fecha_obj = datetime.strptime(row[7], '%Y-%m-%d').date()
                except ValueError:
                    # Si falla ambos, usar fecha actual
                    fecha_obj = date.today()
        
        return cls(
            id=row[0] if len(row) > 0 else "",
            cliente_id=row[1] if len(row) > 1 else "",
            cliente_telefono=row[2] if len(row) > 2 else "",
            cliente_nombre=row[3] if len(row) > 3 else "",
            servicio_id=row[4] if len(row) > 4 else "",
            servicio_nombre=row[5] if len(row) > 5 else "",
            precio=int(row[6]) if len(row) > 6 and row[6] else 0,
            fecha=fecha_obj,
            hora_inicio=datetime.strptime(row[8], '%H:%M').time() if len(row) > 8 else time(0, 0),
            hora_fin=datetime.strptime(row[9], '%H:%M').time() if len(row) > 9 else time(0, 0),
            estado=row[10] if len(row) > 10 else "",
            calendar_event_id=row[11] if len(row) > 11 and row[11] else None,
            fecha_creacion=datetime.fromisoformat(row[12]) if len(row) > 12 and row[12] else None,
            fecha_modificacion=datetime.fromisoformat(row[13]) if len(row) > 13 and row[13] else None,
            notas=row[14] if len(row) > 14 else ""
        )
    
    def to_sheet_row(self) -> list:
        """Convierte la Cita a una fila para Google Sheets."""
        return [
            self.id,
            self.cliente_id,
            self.cliente_telefono,
            self.cliente_nombre,
            self.servicio_id,
            self.servicio_nombre,
            self.precio,
            self.fecha.strftime('%d/%m/%Y'),
            self.hora_inicio.strftime('%H:%M'),
            self.hora_fin.strftime('%H:%M'),
            self.estado,
            self.calendar_event_id or "",
            self.fecha_creacion.isoformat() if self.fecha_creacion else "",
            self.fecha_modificacion.isoformat() if self.fecha_modificacion else "",
            self.notas
        ]
