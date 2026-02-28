# 🚀 Guía de Instalación y Configuración

## 📋 Requisitos Previos

- Python 3.11+
- PostgreSQL (ya configurado en tu servidor)
- Evolution API (ya configurado)
- Acceso a internet

## 🔧 Instalación Paso a Paso

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

El archivo `.env` ya está configurado con tus credenciales:

```env
DATABASE_URL=postgresql://postgres:Olinky2025@n8n_postgres_odontologia:5432/chatbot?sslmode=disable
EVOLUTION_API_URL=https://n8n-evolution-api-nueva-odonto.dtbfmw.easypanel.host/
EVOLUTION_API_KEY=429683C4C977415CAAFCCE10F7D57E11
EVOLUTION_INSTANCE_NAME=OdontologiaBot
HOST=0.0.0.0
PORT=8001
DEBUG=True
```

### 3. Inicializar Base de Datos

```bash
python setup_database.py
```

Esto creará las tablas necesarias:
- `clientes` - Información de clientes
- `citas` - Citas agendadas
- `sesiones_chat` - Sesiones activas del chatbot

### 4. Verificar Integración

```bash
python test_integration.py
```

Este script verificará:
- ✅ Conexión a PostgreSQL
- ✅ Conexión a Evolution API
- ✅ Funcionamiento del chatbot
- ✅ Flujo completo de reserva

### 5. Iniciar el Servidor

```bash
python server.py
```

El servidor estará disponible en: `http://0.0.0.0:8001`

## 🌐 Configurar Webhook en Evolution API

### Opción 1: Usando el endpoint del servidor

```bash
curl -X POST http://localhost:8001/webhook/configure \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://tu-dominio.com/webhook"}'
```

### Opción 2: Manualmente en Evolution API

1. Accede a tu panel de Evolution API
2. Ve a la configuración de la instancia `OdontologiaBot`
3. Configura el webhook URL: `https://tu-dominio.com/webhook`
4. Activa los eventos:
   - `MESSAGES_UPSERT`
   - `MESSAGES_UPDATE`
   - `CONNECTION_UPDATE`

## 📱 Conectar WhatsApp

### Verificar Estado de la Instancia

```bash
curl http://localhost:8001/instance/status
```

### Obtener Código QR

```bash
curl http://localhost:8001/instance/qr
```

### Conectar Instancia

```bash
curl -X POST http://localhost:8001/instance/connect
```

Escanea el código QR con WhatsApp:
1. Abre WhatsApp en tu teléfono
2. Ve a Configuración > Dispositivos vinculados
3. Toca "Vincular un dispositivo"
4. Escanea el código QR

## 🐳 Despliegue con Docker

### Construir y Ejecutar

```bash
docker-compose up -d
```

### Ver Logs

```bash
docker-compose logs -f chatbot
```

### Detener

```bash
docker-compose down
```

## 🧪 Probar el Chatbot

### Enviar Mensaje de Prueba

```bash
curl -X POST http://localhost:8001/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "3001234567",
    "mensaje": "Hola"
  }'
```

### Verificar Salud del Servidor

```bash
curl http://localhost:8001/health
```

### Ver Estadísticas

```bash
curl http://localhost:8001/stats
```

## 📊 Endpoints Disponibles

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

## 🔍 Solución de Problemas

### Error de Conexión a PostgreSQL

```bash
# Verificar que PostgreSQL esté corriendo
docker ps | grep postgres

# Probar conexión manual
psql postgresql://postgres:Olinky2025@n8n_postgres_odontologia:5432/chatbot
```

### Error de Conexión a Evolution API

```bash
# Verificar URL y API Key
curl -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" \
  https://n8n-evolution-api-nueva-odonto.dtbfmw.easypanel.host/instance/connectionState/OdontologiaBot
```

### Webhook No Recibe Mensajes

1. Verifica que el webhook esté configurado correctamente
2. Asegúrate de que tu servidor sea accesible públicamente
3. Revisa los logs del servidor: `docker-compose logs -f`
4. Verifica que la instancia esté conectada

### Limpiar Sesiones Antiguas

```python
from database import get_database
db = get_database()
db.limpiar_sesiones_antiguas(horas=24)
```

## 📈 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Con Docker
docker-compose logs -f chatbot

# Sin Docker
python server.py
```

### Consultar Base de Datos

```sql
-- Ver clientes
SELECT * FROM clientes;

-- Ver citas
SELECT * FROM citas ORDER BY fecha DESC;

-- Ver sesiones activas
SELECT * FROM sesiones_chat;

-- Estadísticas
SELECT COUNT(*) as total_citas FROM citas WHERE estado = 'confirmada';
SELECT COUNT(*) as total_clientes FROM clientes;
```

## 🔐 Seguridad

### Recomendaciones

1. Cambia las credenciales por defecto en producción
2. Usa HTTPS para el webhook
3. Implementa rate limiting
4. Agrega autenticación a los endpoints administrativos
5. Mantén las dependencias actualizadas

### Variables de Entorno Sensibles

Nunca compartas públicamente:
- `DATABASE_URL`
- `EVOLUTION_API_KEY`

## 🚀 Despliegue en Producción

### Usando un Servidor VPS

1. Clona el repositorio en tu servidor
2. Configura las variables de entorno
3. Instala dependencias
4. Configura un reverse proxy (Nginx)
5. Usa un gestor de procesos (PM2, systemd)
6. Configura SSL con Let's Encrypt

### Ejemplo con Nginx

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs del servidor
2. Verifica la configuración en `.env`
3. Ejecuta `python test_integration.py`
4. Consulta la documentación de Evolution API

## 🎉 ¡Listo!

Tu chatbot de barbería está configurado y listo para usar. Los clientes pueden:

1. ✅ Reservar citas por WhatsApp
2. ✅ Consultar sus citas
3. ✅ Cancelar citas
4. ✅ Ver servicios y precios
5. ✅ Consultar promociones
6. ✅ Ver información de contacto

¡Disfruta de tu chatbot automatizado! 💈✨
