# 📱 Guía Completa: Configurar WhatsApp con Evolution API

## 🎯 Configuración

- **URL del Bot**: `https://tu-dominio.com` (o `http://localhost:8000` en desarrollo)
- **Webhook**: `https://tu-dominio.com/webhook`
- **Instancia**: Configurada en tu archivo `.env`

## ✅ Pasos para Configurar

### Paso 1: Verificar que el Servidor Esté Corriendo

```bash
# Probar que el servidor responde
curl http://localhost:8000/health
```

Deberías ver algo como:
```json
{
  "status": "healthy",
  "database": "connected",
  "evolution_api": {...}
}
```

### Paso 2: Ejecutar Tests del Webhook

```bash
python test_webhook.py
```

Este script probará:
- ✅ Health check
- ✅ Endpoint raíz
- ✅ Webhook (simulado)
- ✅ Envío de mensajes
- ✅ Estadísticas

### Paso 3: Configurar el Webhook en Evolution API

```bash
python configurar_webhook.py
```

Selecciona la opción **5** (Todo) para:
1. Verificar estado de la instancia
2. Configurar el webhook automáticamente
3. Obtener el código QR

### Paso 4: Conectar WhatsApp

Después de ejecutar el script anterior:

1. **Abre WhatsApp** en tu teléfono
2. Ve a **Configuración** (⚙️)
3. Toca **Dispositivos vinculados**
4. Toca **Vincular un dispositivo**
5. **Escanea el código QR** que aparece en la terminal

### Paso 5: Probar el Bot

Envía un mensaje al número de WhatsApp conectado:

```
Hola
```

El bot debería responder con el menú principal.

## 🔧 Comandos Útiles

### Verificar Estado del Servidor

```bash
curl https://n8n-barberia-mvp.dtbfmw.easypanel.host/health
```

### Verificar Webhook Configurado

```bash
python configurar_webhook.py
# Selecciona opción 2
```

### Obtener Código QR

```bash
python configurar_webhook.py
# Selecciona opción 4
```

### Enviar Mensaje de Prueba

```bash
curl -X POST http://localhost:8001/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "1234567890",
    "mensaje": "Hola, esto es una prueba"
  }'
```

## 📊 Verificar que Todo Funciona

### 1. Servidor Activo

```bash
curl http://localhost:8001/
```

Respuesta esperada:
```json
{
  "status": "online",
  "service": "Chatbot Barbería",
  "version": "1.0.0"
}
```

### 2. Base de Datos Conectada

```bash
curl http://localhost:8001/health
```

Debe mostrar `"database": "connected"`

### 3. Evolution API Conectada

El mismo endpoint `/health` debe mostrar el estado de Evolution API.

### 4. Webhook Configurado

```bash
python configurar_webhook.py
# Opción 2: Verificar webhook actual
```

Debe mostrar:
```
URL: https://tu-dominio.com/webhook
```

### 5. WhatsApp Conectado

```bash
python configurar_webhook.py
# Opción 3: Verificar estado de instancia
```

Debe mostrar algo como:
```json
{
  "state": "open",
  "status": "connected"
}
```

## 🧪 Flujo de Prueba Completo

### 1. Desde la Terminal

```bash
# 1. Verificar servidor
python test_webhook.py

# 2. Configurar webhook
python configurar_webhook.py
# Selecciona opción 5

# 3. Escanear QR con WhatsApp
```

### 2. Desde WhatsApp

Envía estos mensajes para probar cada flujo:

```
1. "Hola" → Debe mostrar el menú principal
2. "1" → Debe iniciar el flujo de reserva
3. "4" → Debe mostrar servicios y precios
4. "menu" → Debe volver al menú principal
```

## 🔍 Solución de Problemas

### Problema: El servidor no responde

```bash
# Verificar que esté corriendo
curl http://localhost:8001/health

# Si no responde, verifica los logs del servidor
```

### Problema: Webhook no recibe mensajes

1. Verifica que el webhook esté configurado:
```bash
python configurar_webhook.py
# Opción 2
```

2. Verifica que la URL sea correcta:
```
https://tu-dominio.com/webhook
```

3. Prueba el webhook manualmente:
```bash
python test_webhook.py
```

### Problema: WhatsApp no se conecta

1. Obtén un nuevo código QR:
```bash
python configurar_webhook.py
# Opción 4
```

2. Asegúrate de escanear el QR rápidamente (expira en ~60 segundos)

3. Verifica que no haya otra sesión activa

### Problema: El bot no responde

1. Verifica que el mensaje llegue al webhook:
   - Revisa los logs del servidor
   - Busca líneas como: `📨 Webhook recibido`

2. Verifica la base de datos:
```bash
python check_database.py
```

3. Prueba enviar un mensaje manualmente:
```bash
curl -X POST http://localhost:8001/send-message \
  -H "Content-Type: application/json" \
  -d '{"telefono": "TU_NUMERO", "mensaje": "Prueba"}'
```

## 📋 Checklist de Configuración

- [ ] Servidor corriendo en `http://localhost:8000` (o tu dominio en producción)
- [ ] `/health` responde correctamente
- [ ] Base de datos conectada
- [ ] Evolution API accesible
- [ ] Webhook configurado en Evolution API
- [ ] Código QR generado
- [ ] WhatsApp escaneado y conectado
- [ ] Mensaje de prueba enviado
- [ ] Bot responde correctamente

## 🎉 ¡Listo!

Una vez completados todos los pasos, tu chatbot estará:

✅ Conectado a WhatsApp
✅ Recibiendo mensajes automáticamente
✅ Guardando citas en PostgreSQL
✅ Respondiendo a los clientes 24/7

## 📞 URLs Importantes

| Endpoint | URL |
|----------|-----|
| Servidor | http://localhost:8000 |
| Health | http://localhost:8000/health |
| Webhook | http://localhost:8000/webhook |
| Stats | http://localhost:8000/stats |

## 💡 Próximos Pasos

1. Personaliza los servicios en `chatbot_barberia.py`
2. Ajusta los horarios según tu barbería
3. Actualiza la información de contacto
4. Agrega más promociones
5. Monitorea las estadísticas en `/stats`
