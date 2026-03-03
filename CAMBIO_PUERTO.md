# ✅ Cambio de Puerto

## Cambio Realizado

Se actualizó el puerto del servidor de **8001** a **8000** en todos los archivos del proyecto.

### Puerto Anterior
```
8001
```

### Puerto Nuevo
```
8000
```

## Archivos Actualizados

1. ✅ `config/settings.py` - Valor por defecto
2. ✅ `.env` - Configuración activa
3. ✅ `.env.example` - Template
4. ✅ `docker-compose.yml` - Configuración Docker
5. ✅ `Dockerfile` - Puerto expuesto
6. ✅ `start.py` - Script de inicio
7. ✅ `test_webhook.py` - Tests
8. ✅ `configurar_webhook.py` - Configuración webhook
9. ✅ `README_V2.md` - Documentación principal
10. ✅ `CONFIGURAR_WHATSAPP.md` - Guía de configuración
11. ✅ `GUIA_INSTALACION.md` - Guía de instalación
12. ✅ `CONFIGURACION_INICIAL.md` - Configuración inicial
13. ✅ `README.md` - README original

## Verificación

Para verificar que el cambio funcionó correctamente:

```bash
# 1. Verificar que el .env tiene el puerto correcto
cat .env | grep PORT

# 2. Iniciar el servidor
python server.py

# 3. Verificar que está corriendo en el puerto 8000
curl http://localhost:8000/health
```

## URLs Actualizadas

Todas las URLs ahora usan el puerto **8000**:

- Servidor: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- Webhook: `http://localhost:8000/webhook`
- Stats: `http://localhost:8000/stats`

## Docker

Si usas Docker, el puerto también fue actualizado:

```bash
# Construir
docker build -t barberia-churco .

# Ejecutar (puerto 8000)
docker run -p 8000:8000 --env-file .env barberia-churco
```

## Webhook de Evolution API

Si ya configuraste el webhook en Evolution API, actualízalo a:

```
http://localhost:8000/webhook
```

O en producción:

```
https://tu-dominio.com/webhook
```

## Notas

- El puerto 8001 estaba ocupado, por eso se cambió a 8000
- Si necesitas cambiar a otro puerto en el futuro, solo actualiza la variable `PORT` en el archivo `.env`
- El sistema usa el valor de `.env` primero, y si no existe, usa el valor por defecto en `config/settings.py`
