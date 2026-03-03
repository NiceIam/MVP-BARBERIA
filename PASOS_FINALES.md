# 🚀 Pasos Finales para Activar el Chatbot

## ✅ Configuración

- **URL del Bot**: Configurada en tu archivo `.env`
- **Webhook**: `https://tu-dominio.com/webhook` (o localhost en desarrollo)
- **Base de Datos**: PostgreSQL configurada en `.env`
- **Evolution API**: Instancia configurada en `.env`

## 🎯 Pasos para Activar (5 minutos)

### 1️⃣ Resetear Base de Datos (si hay errores)

```bash
python reset_database.py
```

Escribe `SI` cuando te lo pida. Esto solucionará el error de "column does not exist".

### 2️⃣ Verificar que el Servidor Esté Corriendo

```bash
python test_webhook.py
```

Esto probará todos los endpoints de tu servidor desplegado.

### 3️⃣ Configurar Webhook en Evolution API

```bash
python configurar_webhook.py
```

Selecciona la opción **5** (Todo). Esto:
- ✅ Verificará el estado de la instancia
- ✅ Configurará el webhook automáticamente
- ✅ Generará el código QR

### 4️⃣ Conectar WhatsApp

Después del paso anterior, verás un código QR. Escanéalo:

1. Abre **WhatsApp** en tu teléfono
2. Ve a **Configuración** ⚙️
3. Toca **Dispositivos vinculados**
4. Toca **Vincular un dispositivo**
5. **Escanea el código QR**

### 5️⃣ Probar el Bot

Envía un mensaje al número de WhatsApp conectado:

```
Hola
```

El bot debería responder con el menú principal.

## 🔍 Verificaciones Rápidas

### ¿El servidor está corriendo?

```bash
curl http://localhost:8001/health
```

Debe responder con `"status": "healthy"`

### ¿El webhook está configurado?

```bash
python configurar_webhook.py
# Opción 2: Verificar webhook actual
```

Debe mostrar: `URL: https://tu-dominio.com/webhook`

### ¿WhatsApp está conectado?

```bash
python configurar_webhook.py
# Opción 3: Verificar estado de instancia
```

Debe mostrar: `"state": "open"` o `"status": "connected"`

## 📋 Checklist Final

- [ ] Base de datos reseteada (sin errores)
- [ ] Servidor responde en `/health`
- [ ] Webhook configurado en Evolution API
- [ ] Código QR escaneado con WhatsApp
- [ ] WhatsApp conectado (estado "open")
- [ ] Mensaje de prueba enviado
- [ ] Bot responde correctamente

## 🎉 ¡Listo!

Una vez completados estos pasos, tu chatbot estará:

✅ **Activo 24/7** en WhatsApp
✅ **Recibiendo mensajes** automáticamente
✅ **Guardando citas** en PostgreSQL
✅ **Respondiendo a clientes** instantáneamente

## 💡 Próximos Pasos (Opcional)

### Personalizar el Chatbot

Edita `chatbot_barberia.py` para cambiar:

```python
# Servicios y precios
self.servicios = {
    "1": {"nombre": "Corte de Cabello", "precio": 15000, "duracion": 30},
    # ... agregar más servicios
}

# Barberos
self.barberos = {
    "1": {"nombre": "Carlos", "especialidad": "Cortes modernos"},
    # ... agregar más barberos
}

# Promociones
self.promociones = [
    "🎉 Lunes y Martes: 15% descuento",
    # ... agregar más promociones
]

# Información de contacto
self.info_contacto = {
    "direccion": "Tu dirección",
    "telefono": "Tu teléfono",
    # ...
}
```

### Monitorear el Bot

```bash
# Ver estadísticas
curl http://localhost:8001/stats

# Ver citas en la base de datos
python -c "from database import get_database; db = get_database(); print(db.obtener_citas_por_telefono('TU_NUMERO'))"
```

### Agregar Más Funcionalidades

- Recordatorios automáticos 24h antes de la cita
- Sistema de calificaciones post-servicio
- Programa de puntos/fidelidad
- Integración con calendario
- Reportes y analytics

## 🆘 Si Algo No Funciona

### Error en Base de Datos

```bash
python check_database.py
python reset_database.py
```

### Webhook No Recibe Mensajes

```bash
python test_webhook.py
python configurar_webhook.py  # Opción 5
```

### WhatsApp No Se Conecta

```bash
python configurar_webhook.py  # Opción 4 (nuevo QR)
```

## 📚 Documentación Completa

- **CONFIGURAR_WHATSAPP.md** - Guía detallada de WhatsApp
- **SOLUCION_RAPIDA.md** - Solución a errores comunes
- **GUIA_INSTALACION.md** - Instalación completa
- **README.md** - Documentación general

## 🎊 ¡Felicidades!

Tu chatbot de barbería está listo para revolucionar la forma en que gestionas las citas. Los clientes ahora pueden:

- 📅 Reservar citas 24/7
- 📋 Consultar sus citas
- ❌ Cancelar cuando necesiten
- 💰 Ver precios y promociones
- 📍 Obtener información de contacto

Todo de forma **automática** y **sin intervención manual**.

---

**¿Necesitas ayuda?** Revisa los archivos de documentación o ejecuta los scripts de verificación.
