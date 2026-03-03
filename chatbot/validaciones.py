"""Validaciones para el chatbot."""
import re
from datetime import date, time


def validar_telefono(telefono: str) -> bool:
    """Valida que el teléfono sea válido."""
    # Remover caracteres no numéricos
    telefono_limpio = re.sub(r'\D', '', telefono)
    return 10 <= len(telefono_limpio) <= 13


def validar_nombre(nombre: str) -> bool:
    """Valida que el nombre sea válido."""
    if len(nombre) < 2:
        return False
    # Solo letras, espacios y algunos caracteres especiales
    return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre))


def validar_opcion_numerica(opcion: str, max_opciones: int) -> bool:
    """Valida que la opción sea un número válido."""
    try:
        num = int(opcion)
        return 1 <= num <= max_opciones
    except ValueError:
        return False


def validar_confirmacion(texto: str) -> bool:
    """Valida si el texto es una confirmación positiva."""
    texto_lower = texto.lower().strip()
    confirmaciones = ['si', 'sí', 'yes', 'confirmar', 'confirmo', 'ok', 'vale']
    return texto_lower in confirmaciones


def validar_cancelacion(texto: str) -> bool:
    """Valida si el texto es una cancelación."""
    texto_lower = texto.lower().strip()
    cancelaciones = ['no', 'cancelar', 'cancelo', 'nop', 'nope']
    return texto_lower in cancelaciones


def validar_comando_menu(texto: str) -> bool:
    """Valida si el texto es un comando para volver al menú."""
    texto_lower = texto.lower().strip()
    comandos = ['menu', 'inicio', 'hola', 'start', 'empezar']
    return texto_lower in comandos
