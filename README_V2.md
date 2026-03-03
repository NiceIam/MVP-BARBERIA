# 💈 Barbería Churco - Sistema de Agendamiento v2.0

Sistema completo de chatbot para gestión de citas por WhatsApp, ahora con **Google Sheets** como base de datos y **Google Calendar** para sincronización automática.

## 🚀 Características

- ✅ Agendamiento de citas por WhatsApp
- 📊 Google Sheets como base de datos (sin infraestructura)
- 📅 Sincronización automática con Google Calendar
- 🤖 Chatbot conversacional con máquina de estados
- ⏰ Cálculo inteligente de disponibilidad
- 🔄 Consulta, cancelación y reagendamiento de citas
- 📱 Integración completa con Evolution API

## 📦 Instalación Rápida

### 1. Clonar repositorio

```bash
git clone <tu-repo>
cd barberia-churco
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Google Cloud

Ver [MIGRACION_GOOGLE.md](MIGRACION_GOOGLE.md) para pasos detallados.

Resumen:
1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API y Google Calendar API
3. Crear Service Account
4. Descargar credenciales JSON → `service_account.json`

### 4. Crear Google Sheet

1. Crear nuevo Google Sheet: `Barberia_Churco_DB`
2. Crear 5 sheets: `clientes`, `citas`, `servicios`, `disponibilidad`, `sesiones_chat`
3. Agregar headers según [ARQUITECTURA_GOOGLE.md](ARQUITECTURA_GOOGLE.md)
4. Compartir con Service Account (Editor)
5. Copiar ID del Sheet (desde URL)

### 5. Configurar Calendar

1. Usar calendario de `churcobarberstudio@gmail.com`
2. Compartir con Service Account (Hacer cambios en eventos)

### 6. Configurar .env

```bash
cp .env.example .env
# Editar .env con tus valores
```

```env
GOOGLE_SHEETS_ID=tu_sheet_id_aqui
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
GOOGLE_CALENDAR_ID=churcobarberstudio@gmail.com
TIMEZONE=America/Bogota

EVOLUTION_API_URL=https://tu-evolution-api.com/
EVOLUTION_API_KEY=tu_api_key
EVOLUTION_INSTANCE_NAME=tu_instancia

HOST=0.0.0.0
PORT=8001
DEBUG=True
```

### 7. Poblar datos iniciales

```bash
python scripts/seed_data.py
```

### 8. Probar sistema

```bash
python test_sistema.py
```

### 9. Iniciar servidor

```bash
python server.py
```

## 🎯 Uso

### Servidor en producción

```bash
python server.py
```

El servidor estará disponible en `http://localhost:8000`

### Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Estado del servidor |
| `/health` | GET | Verificación de salud |
| `/webhook` | POST | Recibe mensajes de WhatsApp |
| `/send-message` | POST | Envía mensajes manualmente |
| `/stats` | GET | Estadísticas del sistema |

### Probar manualmente

```bash
curl -X POST http://localhost:8000/send-message \
  -H "Content-Type: application/json" \
  -d '{"telefono": "573001234567", "mensaje": "hola"}'
```

## 🔄 Flujos del Chatbot

### 1. Agendar Cita

```
Usuario: "hola"
Bot: Menú principal
Usuario: "1" (Agendar)
Bot: Selecciona servicio
Usuario: "1" (Corte + Barba)
Bot: Selecciona fecha
Usuario: "3" (Miércoles)
Bot: Selecciona hora
Usuario: "5" (09:00 AM)
Bot: Confirma tu cita
Usuario: "SI"
Bot: ✅ Cita confirmada
```

### 2. Consultar Cita

```
Usuario: "2"
Bot: Muestra citas activas
```

### 3. Cancelar Cita

```
Usuario: "3"
Bot: ¿Qué cita cancelar?
Usuario: "1"
Bot: ¿Confirmas cancelación?
Usuario: "SI"
Bot: ✅ Cita cancelada
```

### 4. Reagendar Cita

```
Usuario: "4"
Bot: ¿Qué cita reagendar?
Usuario: "1"
Bot: Selecciona nueva fecha...
```

## 📊 Arquitectura

```
WhatsApp → Evolution API → FastAPI → Chatbot Engine
                                    ↓
                            Google Sheets (DB)
                            Google Calendar (Sync)
```

Ver [ARQUITECTURA_GOOGLE.md](ARQUITECTURA_GOOGLE.md) para detalles completos.

## 🗄️ Estructura de Datos

### Google Sheets

- **clientes**: Información de clientes
- **citas**: Citas agendadas
- **servicios**: Servicios disponibles
- **disponibilidad**: Horarios de atención
- **sesiones_chat**: Sesiones activas del chatbot

### Google Calendar

Cada cita crea automáticamente un evento en Calendar con:
- Título: `Servicio - Cliente`
- Descripción: Detalles de la cita
- Recordatorios: 60 min y 15 min antes
- Color según estado

## 🛠️ Personalización

### Cambiar servicios

Editar `config/constants.py`:

```python
SERVICIOS = {
    "srv_corte_barba": {
        "nombre": "Corte + Barba",
        "precio": 28000,
        "duracion_minutos": 45
    }
}
```

### Cambiar horarios

Editar `config/constants.py`:

```python
HORARIOS_ATENCION = [
    {"hora_inicio": time(8, 0), "hora_fin": time(12, 0)},
    {"hora_inicio": time(14, 0), "hora_fin": time(20, 0)}
]
```

## 🧪 Testing

```bash
# Probar sistema completo
python test_sistema.py

# Probar conexión a Sheets
python -c "from services import SheetsClient; SheetsClient().test_connection()"

# Probar conexión a Calendar
python -c "from services import CalendarClient; CalendarClient().test_connection()"

# Probar chatbot
python -c "from chatbot import ChatbotEngine; print(ChatbotEngine().procesar_mensaje('test', 'hola'))"
```

## 📈 Monitoreo

Los logs se guardan en `logs/barberia_{fecha}.log`

```bash
# Ver logs en tiempo real
tail -f logs/barberia_*.log
```

## 🔐 Seguridad

- ✅ `service_account.json` en `.gitignore`
- ✅ `.env` en `.gitignore`
- ✅ Credenciales nunca en código
- ✅ Service Account con permisos mínimos

## 🚀 Despliegue

### Docker

```bash
docker build -t barberia-churco .
docker run -p 8000:8000 --env-file .env barberia-churco
```

### VPS

```bash
# Instalar dependencias
pip install -r requirements.txt

# Usar systemd o PM2 para mantener el servidor corriendo
```

## 📚 Documentación

- [ARQUITECTURA_GOOGLE.md](ARQUITECTURA_GOOGLE.md) - Arquitectura técnica completa
- [MIGRACION_GOOGLE.md](MIGRACION_GOOGLE.md) - Guía de migración desde PostgreSQL
- [CONFIGURACION_INICIAL.md](CONFIGURACION_INICIAL.md) - Setup inicial

## 🆘 Troubleshooting

### Error: "Permission denied"
```bash
# Verificar que Service Account tenga permisos en Sheet y Calendar
```

### Error: "Quota exceeded"
```bash
# Implementar caché o reducir frecuencia de requests
```

### Error: "Invalid credentials"
```bash
# Verificar que service_account.json esté en la raíz
# Regenerar credenciales si es necesario
```

## 📞 Soporte

Para problemas o dudas:
1. Revisar [ARQUITECTURA_GOOGLE.md](ARQUITECTURA_GOOGLE.md)
2. Ejecutar `python test_sistema.py`
3. Verificar logs en `logs/`

## 🎉 ¡Listo!

Tu chatbot está completamente funcional con:
- ✅ Google Sheets (base de datos)
- ✅ Google Calendar (sincronización)
- ✅ WhatsApp (Evolution API)
- ✅ Chatbot conversacional

¡Disfruta de tu sistema automatizado! 💈✨
