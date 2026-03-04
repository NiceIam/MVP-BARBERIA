"""Configuración del sistema desde variables de entorno."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
SERVICE_ACCOUNT_PATH = BASE_DIR / SERVICE_ACCOUNT_FILE

# Google Sheets
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID', '1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT')

# Google Calendar
GOOGLE_CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'churcobarberstudio@gmail.com')
TIMEZONE = os.getenv('TIMEZONE', 'America/Bogota')

# Google API Scopes
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar.events'
]

# Evolution API
EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', '')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY', '')
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME', '')

# Server
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Sesiones
SESSION_TIMEOUT_MINUTES = 15

# Validaciones
MAX_DIAS_ADELANTE = 30
SLOT_INTERVAL_MINUTES = 60
