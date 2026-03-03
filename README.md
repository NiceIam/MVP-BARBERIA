# 💈 Chatbot para Barbería - WhatsApp Bot

Sistema completo de chatbot para gestión de citas y atención al cliente en barberías, integrado con WhatsApp Business API (Evolution API) y PostgreSQL.

## ⚠️ Configuración Inicial

Antes de empezar, debes configurar tus credenciales:

1. Copia el archivo de ejemplo: `cp .env.example .env`
2. Edita `.env` con tus credenciales
3. Ver [CONFIGURACION_INICIAL.md](CONFIGURACION_INICIAL.md) para más detalles

## 🚀 Características

- ✅ Reserva de citas con selección de servicio, barbero, fecha y hora
- 📋 Consulta de servicios y precios
- 👨‍💼 Información de barberos y especialidades
- 🔍 Consulta y cancelación de citas existentes
- 🎁 Sistema de promociones
- 📍 Información de contacto y ubicación
- 💬 Interfaz conversacional natural
- 📱 Integración completa con WhatsApp
- 🗄️ Persistencia de datos en PostgreSQL
- 🔄 Gestión de sesiones por usuario
- 🌐 API REST para administración

## 📦 Instalación Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Verificar base de datos
python check_database.py

# 3. Si hay errores, resetear base de datos
python reset_database.py

# 4. Iniciar servidor (todo en uno)
python start.py
```

**O usa el inicio automático:**
```bash
python start.py
```
Este script verifica todo automáticamente y inicia el servidor.

## 🔧 Configuración

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:
- PostgreSQL: URL de conexión a tu base de datos
- Evolution API: URL, API Key e Instancia
- Puerto: Puerto donde correrá el servidor (default: 8000)

Ver [GUIA_INSTALACION.md](GUIA_INSTALACION.md) para instrucciones detalladas.

## 🎯 Uso

### Servidor WhatsApp (Producción)
```bash
python server.py
```

### Modo Consola (Desarrollo)
```bash
python main.py
```

### Pruebas Automatizadas
```bash
python test_chatbot.py
python test_integration.py
```

## 🔄 Flujos Implementados

1. **Reservar Cita**: Servicio → Barbero → Fecha → Hora → Confirmación
2. **Consultar Cita**: Búsqueda por nombre/teléfono (desde BD)
3. **Cancelar Cita**: Verificación y cancelación (actualiza BD)
4. **Ver Servicios**: Lista completa con precios
5. **Ver Promociones**: Ofertas actuales
6. **Ver Barberos**: Equipo y especialidades
7. **Contacto**: Ubicación, horarios y redes sociales

## 📊 Arquitectura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  WhatsApp   │ ───> │ Evolution API│ ───> │   Server    │
│   Cliente   │ <─── │   (Webhook)  │ <─── │  (FastAPI)  │
└─────────────┘      └──────────────┘      └─────────────┘
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │  Chatbot    │
                                            │  Integrado  │
                                            └─────────────┘
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │ PostgreSQL  │
                                            │  Database   │
                                            └─────────────┘
```

## 📁 Estructura del Proyecto

```
.
├── chatbot_barberia.py      # Motor del chatbot (lógica base)
├── chatbot_integrado.py     # Chatbot con persistencia
├── database.py              # Gestión de PostgreSQL
├── evolution_api.py         # Cliente de Evolution API
├── server.py                # Servidor FastAPI + Webhooks
├── main.py                  # Modo consola
├── test_chatbot.py          # Tests del chatbot
├── test_integration.py      # Tests de integración
├── setup_database.py        # Inicialización de BD
├── requirements.txt         # Dependencias
├── .env                     # Variables de entorno
├── Dockerfile               # Imagen Docker
├── docker-compose.yml       # Orquestación
├── README.md                # Este archivo
├── GUIA_INSTALACION.md      # Guía detallada
└── diagrama_flujos.md       # Documentación de flujos
```

## 🌐 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Estado del servidor |
| `/health` | GET | Verificación de salud |
| `/webhook` | POST | Recibe mensajes de WhatsApp |
| `/send-message` | POST | Envía mensajes manualmente |
| `/instance/status` | GET | Estado de la instancia |
| `/instance/qr` | GET | Obtiene código QR |
| `/instance/connect` | POST | Conecta la instancia |
| `/webhook/configure` | POST | Configura webhook |
| `/stats` | GET | Estadísticas del chatbot |

## 🗄️ Base de Datos

### Tablas

- **clientes**: Información de clientes (nombre, teléfono)
- **citas**: Citas agendadas (servicio, barbero, fecha, hora)
- **sesiones_chat**: Sesiones activas del chatbot

### Consultas Útiles

```sql
-- Ver todas las citas
SELECT * FROM citas ORDER BY fecha DESC;

-- Citas por cliente
SELECT c.*, cl.nombre FROM citas c 
JOIN clientes cl ON c.cliente_id = cl.id 
WHERE cl.telefono = '1234567890';

-- Estadísticas
SELECT COUNT(*) FROM citas WHERE estado = 'confirmada';
```

## 🐳 Docker

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f chatbot

# Detener
docker-compose down
```

## 🛠️ Personalización

Edita estos archivos para personalizar:

- `chatbot_barberia.py`: Servicios, barberos, promociones, horarios
- `.env`: Credenciales y configuración
- `database.py`: Esquema de base de datos
- `server.py`: Endpoints y lógica del servidor

## 🧪 Testing

```bash
# Tests del chatbot base
python test_chatbot.py

# Tests de integración completa
python test_integration.py

# Enviar mensaje de prueba
curl -X POST http://localhost:8001/send-message \
  -H "Content-Type: application/json" \
  -d '{"telefono": "1234567890", "mensaje": "Hola"}'
```

## 📱 Conectar WhatsApp

### Configuración Rápida

```bash
# 1. Verificar que el servidor esté corriendo
python test_webhook.py

# 2. Configurar webhook en Evolution API
python configurar_webhook.py
# Selecciona opción 5 (Todo)

# 3. Escanear código QR con WhatsApp
```

### Verificar Estado

```bash
curl http://localhost:8001/health
```

### Obtener Código QR

```bash
python configurar_webhook.py
# Selecciona opción 4
```

Escanea el QR con WhatsApp:
1. Abre WhatsApp en tu teléfono
2. Ve a Configuración > Dispositivos vinculados
3. Toca "Vincular un dispositivo"
4. Escanea el código QR

Ver [CONFIGURAR_WHATSAPP.md](CONFIGURAR_WHATSAPP.md) para guía completa.

## 🔐 Seguridad

- Las credenciales están en `.env` (no compartir)
- Usa HTTPS en producción
- Implementa rate limiting si es necesario
- Mantén las dependencias actualizadas

## 📈 Monitoreo

```bash
# Ver estadísticas
curl http://localhost:8001/stats

# Verificar salud
curl http://localhost:8001/health

# Ver logs
tail -f logs/chatbot.log  # Si configuras logging
```

## 🚀 Despliegue

Ver [GUIA_INSTALACION.md](GUIA_INSTALACION.md) para:
- Despliegue en VPS
- Configuración de Nginx
- SSL con Let's Encrypt
- Gestión de procesos con PM2/systemd

## 📞 Soporte

Para problemas o dudas:
1. Revisa [GUIA_INSTALACION.md](GUIA_INSTALACION.md)
2. Ejecuta `python test_integration.py`
3. Verifica los logs del servidor
4. Consulta [diagrama_flujos.md](diagrama_flujos.md)

## 🎉 ¡Listo para Usar!

Tu chatbot está completamente integrado con:
- ✅ WhatsApp Business (Evolution API)
- ✅ PostgreSQL (persistencia de datos)
- ✅ API REST (administración)
- ✅ Webhooks (mensajes en tiempo real)

¡Disfruta de tu chatbot automatizado! 💈✨
