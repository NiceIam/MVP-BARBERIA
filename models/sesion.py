"""Modelo de Sesión de Chat."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import json


@dataclass
class Sesion:
    """Representa una sesión de chat activa."""
    
    telefono: str
    estado: str
    datos_temp: Dict[str, Any] = field(default_factory=dict)
    ultima_actividad: datetime = field(default_factory=datetime.now)
    cita_en_proceso: str = ""
    
    @classmethod
    def from_sheet_row(cls, row: list) -> 'Sesion':
        """Crea una Sesión desde una fila de Google Sheets."""
        datos_temp = {}
        if len(row) > 2 and row[2]:
            try:
                datos_temp = json.loads(row[2])
            except json.JSONDecodeError:
                datos_temp = {}
        
        return cls(
            telefono=row[0] if len(row) > 0 else "",
            estado=row[1] if len(row) > 1 else "",
            datos_temp=datos_temp,
            ultima_actividad=datetime.fromisoformat(row[3]) if len(row) > 3 and row[3] else datetime.now(),
            cita_en_proceso=row[4] if len(row) > 4 else ""
        )
    
    def to_sheet_row(self) -> list:
        """Convierte la Sesión a una fila para Google Sheets."""
        return [
            self.telefono,
            self.estado,
            json.dumps(self.datos_temp, ensure_ascii=False),
            self.ultima_actividad.isoformat(),
            self.cita_en_proceso
        ]
