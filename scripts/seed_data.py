"""Script para poblar datos iniciales en Google Sheets."""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services import SheetsClient
from config.constants import SERVICIOS, HORARIOS_ATENCION
from config.constants import SHEET_SERVICIOS, SHEET_DISPONIBILIDAD
from loguru import logger


def seed_servicios(sheets: SheetsClient):
    """Pobla la sheet de servicios."""
    logger.info("Poblando servicios...")
    
    for servicio_data in SERVICIOS.values():
        row = [
            servicio_data["id"],
            servicio_data["nombre"],
            servicio_data["precio"],
            servicio_data["duracion_minutos"],
            "TRUE" if servicio_data["activo"] else "FALSE",
            servicio_data["orden"]
        ]
        sheets._append_row(SHEET_SERVICIOS, row)
    
    logger.info("✅ Servicios poblados")


def seed_disponibilidad(sheets: SheetsClient):
    """Pobla la sheet de disponibilidad."""
    logger.info("Poblando disponibilidad...")
    
    # Para cada día de la semana (0=Lunes, 6=Domingo)
    for dia in range(7):
        for idx, bloque in enumerate(HORARIOS_ATENCION):
            row = [
                f"disp_dia{dia}_bloque{idx}",
                dia,
                bloque["hora_inicio"].strftime("%H:%M"),
                bloque["hora_fin"].strftime("%H:%M"),
                "TRUE"
            ]
            sheets._append_row(SHEET_DISPONIBILIDAD, row)
    
    logger.info("✅ Disponibilidad poblada")


def main():
    """Función principal."""
    logger.info("🌱 Iniciando seed de datos...")
    
    sheets = SheetsClient()
    
    # Verificar conexión
    if not sheets.test_connection():
        logger.error("❌ No se pudo conectar a Google Sheets")
        return
    
    # Poblar datos
    seed_servicios(sheets)
    seed_disponibilidad(sheets)
    
    logger.info("✅ Seed completado exitosamente")


if __name__ == "__main__":
    main()
