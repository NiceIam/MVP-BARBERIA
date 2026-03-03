# 🔧 Solución Rápida al Error "column does not exist"

## ❌ El Problema

El error `psycopg2.errors.UndefinedColumn: column "cliente_id" does not exist` ocurre porque:
- Las tablas se crearon en un orden incorrecto
- Los índices intentaron crearse antes que las columnas
- Hay tablas parcialmente creadas en la base de datos

## ✅ Solución en 3 Pasos

### Paso 1: Verificar el Estado Actual

```bash
python check_database.py
```

Esto te mostrará:
- Qué tablas existen
- Qué columnas tienen
- Si hay problemas de estructura

### Paso 2: Resetear la Base de Datos

```bash
python reset_database.py
```

Cuando te pregunte, escribe `SI` para confirmar.

Esto:
- ✅ Eliminará todas las tablas existentes
- ✅ Recreará las tablas en el orden correcto
- ✅ Creará todos los índices necesarios

⚠️ **ADVERTENCIA**: Esto eliminará todos los datos existentes.

### Paso 3: Iniciar el Servidor

```bash
python start.py
```

O si prefieres:

```bash
python server.py
```

## 🚀 Inicio Automático (Recomendado)

Si quieres que todo se configure automáticamente:

```bash
python start.py
```

Este script:
1. Verifica la conexión a PostgreSQL
2. Verifica que las tablas existan
3. Las crea si no existen
4. Inicia el servidor

## 📋 Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `check_database.py` | Verifica el estado de la BD |
| `reset_database.py` | Elimina y recrea todas las tablas |
| `setup_database.py` | Inicializa la BD (sin eliminar) |
| `start.py` | Inicio automático con verificaciones |
| `server.py` | Inicia solo el servidor |
| `test_integration.py` | Prueba la integración completa |

## 🔍 Verificar que Todo Funciona

Después de resetear, verifica:

```bash
# 1. Verificar tablas
python check_database.py

# 2. Probar integración
python test_integration.py

# 3. Iniciar servidor
python start.py
```

## 💡 Si Aún Tienes Problemas

### Problema: No puedo conectar a PostgreSQL

```bash
# Verifica que el contenedor esté corriendo
docker ps | grep postgres

# Verifica las credenciales en .env
cat .env
```

### Problema: Las tablas no se crean

```bash
# Conéctate manualmente a PostgreSQL
psql postgresql://usuario:contraseña@host:5432/nombre_bd

# Dentro de psql, ejecuta:
\dt  # Ver tablas
\d clientes  # Ver estructura de tabla clientes
```

### Problema: Error de permisos

Asegúrate de que el usuario `postgres` tenga permisos para crear tablas:

```sql
GRANT ALL PRIVILEGES ON DATABASE chatbot TO postgres;
```

## 📞 Comandos Útiles

```bash
# Ver logs del servidor
python server.py

# Probar envío de mensaje
curl -X POST http://localhost:8001/send-message \
  -H "Content-Type: application/json" \
  -d '{"telefono": "1234567890", "mensaje": "Hola"}'

# Ver estado de salud
curl http://localhost:8001/health

# Ver estadísticas
curl http://localhost:8001/stats
```

## ✅ Checklist de Verificación

- [ ] PostgreSQL está corriendo
- [ ] Las credenciales en `.env` son correctas
- [ ] Ejecuté `python reset_database.py` y confirmé con "SI"
- [ ] `python check_database.py` muestra las 3 tablas
- [ ] `python start.py` inicia sin errores
- [ ] `curl http://localhost:8001/health` responde OK

## 🎉 ¡Listo!

Una vez completados estos pasos, tu chatbot estará funcionando correctamente y listo para recibir mensajes de WhatsApp.
