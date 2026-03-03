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

Copia el archivo de ejemplo y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_bd?sslmode=disable
EVOLUTION_API_URL=https://tu-evolution-api.com/
EVOLUTION_API_KEY=tu_api_key_aqui
EVOLUTION_INSTANCE_NAME=NombreDeTuInstancia
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Inicializar Base de Datos

#### Opción A: Inicialización Normal (recomendado)
```bash
python setup_database.py
```

#### Opción B: Verificar Estado de la BD
```bash
python check_database.py
```

#### Opción C: Reset Completo (elimina todos los datos)
```bash
python reset_database.py
```

Esto creará las tablas necesarias:
- `clientes` - Información de clientes
- `citas` - Citas agendadas
- `sesiones_chat` - Sesiones activas del chatbot

**Si encuentras errores de columnas no existentes:**
1. Ejecuta `python check_database.py` para ver el estado
2. Ejecuta `python reset_database.py` para recrear las tablas
3. Confirma escribiendo "SI" cuando se solicite

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

El servidor estará disponible en: `http://0.0.0.0:8000`

## 🌐 Configurar Webhook en Evolution API

### Opción 1: Usando el endpoint del servidor

```bash
curl -X POST http://localhost:8001/webhook/configure \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://tu-dominio.com/webhook"}'
```

### Opción 2: Manualmente en Evolution API

1. Accede a tu panel de Evolution API
2. Ve a la configuración de tu instancia
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
    "telefono": "1234567890",
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

# Verificar estado de la base de datos
python check_database.py

# Si hay problemas con las tablas, resetear
python reset_database.py

# Probar conexión manual
psql postgresql://usuario:contraseña@host:5432/nombre_bd
```

### Error: "column does not exist"

Este error ocurre cuando las tablas no están correctamente creadas:

```bash
# 1. Verificar estado
python check_database.py

# 2. Resetear base de datos
python reset_database.py

# 3. Iniciar servidor
python server.py
```

### Error de Conexión a Evolution API

```bash
# Verificar URL y API Key
curl -H "apikey: TU_API_KEY" \
  https://tu-evolution-api.com/instance/connectionState/TuInstancia
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
        proxy_pass http://localhost:8000;
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
