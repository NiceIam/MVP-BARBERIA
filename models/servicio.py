"""Modelo de Servicio."""
from dataclasses import dataclass


@dataclass
class Servicio:
    """Representa un servicio de la barbería."""
    
    id: str
    nombre: str
    precio: int
    duracion_minutos: int
    activo: bool
    orden: int
    
    @classmethod
    def from_sheet_row(cls, row: list) -> 'Servicio':
        """Crea un Servicio desde una fila de Google Sheets."""
        return cls(
            id=row[0] if len(row) > 0 else "",
            nombre=row[1] if len(row) > 1 else "",
            precio=int(row[2]) if len(row) > 2 and row[2] else 0,
            duracion_minutos=int(row[3]) if len(row) > 3 and row[3] else 0,
            activo=row[4].upper() == 'TRUE' if len(row) > 4 else True,
            orden=int(row[5]) if len(row) > 5 and row[5] else 0
        )
    
    def to_sheet_row(self) -> list:
        """Convierte el Servicio a una fila para Google Sheets."""
        return [
            self.id,
            self.nombre,
            self.precio,
            self.duracion_minutos,
            'TRUE' if self.activo else 'FALSE',
            self.orden
        ]
