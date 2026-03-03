# ✅ Cambio de Google Sheet ID

## Cambio Realizado

Se actualizó el ID del Google Sheet en todos los archivos del proyecto.

### ID Anterior
```
1VH-pQT7HF8iD1y5WLLltGJN9eossHbcG6z66Bq0OLrM
```

### ID Nuevo
```
1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT
```

## Archivos Actualizados

1. ✅ `config/settings.py` - Valor por defecto actualizado
2. ✅ `.env.example` - Template actualizado
3. ✅ `.env` - Archivo de configuración actualizado
4. ✅ `ARQUITECTURA_GOOGLE.md` - Documentación actualizada

## Verificación

Para verificar que el cambio funcionó correctamente:

```bash
# 1. Verificar que el .env tiene el ID correcto
cat .env | grep GOOGLE_SHEETS_ID

# 2. Probar conexión al nuevo Sheet
python -c "from services import SheetsClient; print('✅ Conectado' if SheetsClient().test_connection() else '❌ Error')"

# 3. Ejecutar test completo
python test_sistema.py
```

## Requisitos del Nuevo Sheet

Asegúrate de que el Google Sheet `1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT` tenga:

### 1. Estructura de Sheets (5 tabs)
- ✅ `clientes`
- ✅ `citas`
- ✅ `servicios`
- ✅ `disponibilidad`
- ✅ `sesiones_chat`

### 2. Headers en cada Sheet

#### Sheet: clientes
```
id | telefono | nombre | fecha_registro | total_citas | ultima_cita
```

#### Sheet: citas
```
id | cliente_id | cliente_telefono | cliente_nombre | servicio_id | servicio_nombre | precio | fecha | hora_inicio | hora_fin | estado | calendar_event_id | fecha_creacion | fecha_modificacion | notas
```

#### Sheet: servicios
```
id | nombre | precio | duracion_minutos | activo | orden
```

#### Sheet: disponibilidad
```
id | dia_semana | hora_inicio | hora_fin | activo
```

#### Sheet: sesiones_chat
```
telefono | estado | datos_temp | ultima_actividad | cita_en_proceso
```

### 3. Permisos

El Service Account debe tener permisos de **Editor** en el Sheet:

```
Email del Service Account: churcobarberstudio@gmail.com
Permisos: Editor
```

## Poblar Datos Iniciales

Una vez verificada la estructura, poblar los datos iniciales:

```bash
python scripts/seed_data.py
```

Esto creará:
- 2 servicios (Corte + Barba, Corte Normal)
- Horarios de disponibilidad para todos los días

## Próximos Pasos

1. ✅ Verificar que el Sheet tenga la estructura correcta
2. ✅ Verificar permisos del Service Account
3. ✅ Ejecutar `python scripts/seed_data.py`
4. ✅ Ejecutar `python test_sistema.py`
5. ✅ Iniciar servidor: `python server.py`

## Notas

- El ID del Sheet se obtiene de la URL:
  ```
  https://docs.google.com/spreadsheets/d/1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT/edit
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      Este es el ID
  ```

- Si cambias de Sheet en el futuro, solo necesitas actualizar la variable `GOOGLE_SHEETS_ID` en el archivo `.env`

- El sistema usa el valor de `.env` primero, y si no existe, usa el valor por defecto en `config/settings.py`
