"""Modelo de Cliente."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    """Representa un cliente de la barbería."""
    
    id: str
    telefono: str
    nombre: str
    fecha_registro: datetime
    total_citas: int = 0
    ultima_cita: Optional[str] = None
    
    @classmethod
    def from_sheet_row(cls, row: list) -> 'Cliente':
        """Crea un Cliente desde una fila de Google Sheets."""
        return cls(
            id=row[0] if len(row) > 0 else "",
            telefono=row[1] if len(row) > 1 else "",
            nombre=row[2] if len(row) > 2 else "",
            fecha_registro=datetime.fromisoformat(row[3]) if len(row) > 3 else datetime.now(),
            total_citas=int(row[4]) if len(row) > 4 and row[4] else 0,
            ultima_cita=row[5] if len(row) > 5 and row[5] else None
        )
    
    def to_sheet_row(self) -> list:
        """Convierte el Cliente a una fila para Google Sheets."""
        return [
            self.id,
            self.telefono,
            self.nombre,
            self.fecha_registro.isoformat(),
            self.total_citas,
            self.ultima_cita or ""
        ]
