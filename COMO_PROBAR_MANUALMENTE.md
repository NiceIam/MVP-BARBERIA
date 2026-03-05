# 🧪 Cómo Probar Manualmente la Funcionalidad del Menú

## 📋 Guía de Pruebas Manuales

### Prerequisitos
- Sistema de chatbot en ejecución
- Acceso a WhatsApp para enviar mensajes
- Número de teléfono configurado

---

## 🎯 Escenarios de Prueba

### Escenario 1: Inicio de Conversación
**Objetivo:** Verificar que el menú se muestre al inicio

**Pasos:**
1. Envía el mensaje: `hola`
2. **Verifica que recibes:**
   - Mensaje de bienvenida
   - Lista de opciones (1-6)
   - Texto al final: "_Escribe *hola* para volver al menú principal._"

**Resultado Esperado:** ✅ Menú completo con opción de volver

---

### Escenario 2: Opción Inválida
**Objetivo:** Verificar mensaje de error incluye opción de menú

**Pasos:**
1. Envía: `hola`
2. Envía: `99` (opción inválida)
3. **Verifica que recibes:**
   - Mensaje de error
   - Texto al final: "_Escribe *hola* para volver al menú principal._"

**Resultado Esperado:** ✅ Error con opción de volver al menú

---

### Escenario 3: Flujo de Agendamiento
**Objetivo:** Verificar que todos los pasos incluyen opción de menú

**Pasos:**
1. Envía: `hola`
2. Envía: `1` (Agendar cita)
3. **Verifica cada respuesta incluye:** "_Escribe *hola* para volver al menú principal._"
   - Solicitud de nombre (si eres nuevo)
   - Lista de servicios
   - Lista de fechas
   - Lista de horas
   - Confirmación de cita

**Resultado Esperado:** ✅ Cada paso incluye opción de menú

---

### Escenario 4: Comando 'hola' en Medio del Flujo
**Objetivo:** Verificar que 'hola' resetea en cualquier momento

**Pasos:**
1. Envía: `hola`
2. Envía: `1` (Agendar cita)
3. Envía: `1` (Seleccionar servicio)
4. **En medio del flujo, envía:** `hola`
5. **Verifica que recibes:**
   - Menú principal completo
   - Sesión reseteada (puedes empezar de nuevo)

**Resultado Esperado:** ✅ Vuelve al menú, sesión reseteada

---

### Escenario 5: Consultar Cita
**Objetivo:** Verificar mensajes de consulta incluyen opción de menú

**Pasos:**
1. Envía: `hola`
2. Envía: `2` (Consultar cita)
3. **Verifica que recibes:**
   - Si tienes citas: resumen con opción de menú
   - Si no tienes citas: "No tienes citas agendadas" + opción de menú

**Resultado Esperado:** ✅ Respuesta incluye opción de menú

---

### Escenario 6: Cancelar Cita
**Objetivo:** Verificar flujo de cancelación incluye opción de menú

**Pasos:**
1. Envía: `hola`
2. Envía: `3` (Cancelar cita)
3. **Verifica cada mensaje incluye:** "_Escribe *hola* para volver al menú principal._"
   - Lista de citas (si tienes múltiples)
   - Confirmación de cancelación
   - Mensaje de éxito

**Resultado Esperado:** ✅ Todo el flujo incluye opción de menú

---

### Escenario 7: Información de la Barbería
**Objetivo:** Verificar información incluye opción de menú

**Pasos:**
1. Envía: `hola`
2. Envía: `5` (Información)
3. **Verifica que recibes:**
   - Información completa de la barbería
   - Texto al final: "_Escribe *hola* para volver al menú principal._"

**Resultado Esperado:** ✅ Información con opción de menú

---

### Escenario 8: Cita Confirmada
**Objetivo:** Verificar confirmación incluye opción de menú

**Pasos:**
1. Completa el flujo de agendamiento hasta el final
2. Envía: `SI` para confirmar
3. **Verifica que recibes:**
   - Mensaje de confirmación "✅ ¡Cita confirmada!"
   - Detalles de la cita
   - Texto al final: "_Escribe *hola* para volver al menú principal._"

**Resultado Esperado:** ✅ Confirmación con opción de menú

---

## 📊 Checklist de Verificación

Marca cada item después de probarlo:

- [ ] Menú principal muestra opción de volver
- [ ] Mensajes de error incluyen opción de menú
- [ ] Selección de servicios incluye opción de menú
- [ ] Selección de fechas incluye opción de menú
- [ ] Selección de horas incluye opción de menú
- [ ] Confirmación de cita incluye opción de menú
- [ ] Cita confirmada incluye opción de menú
- [ ] Consulta de citas incluye opción de menú
- [ ] Cancelación incluye opción de menú
- [ ] Información de barbería incluye opción de menú
- [ ] Comando 'hola' funciona en cualquier momento
- [ ] Comando 'hola' resetea la sesión correctamente

---

## 🐛 Qué Buscar (Posibles Problemas)

### ❌ Problemas a Reportar:

1. **Mensaje sin opción de menú**
   - Si encuentras algún mensaje que NO incluya el texto de volver al menú
   - Anota el flujo exacto para reproducirlo

2. **Comando 'hola' no funciona**
   - Si escribes 'hola' y no vuelves al menú
   - Si la sesión no se resetea correctamente

3. **Texto duplicado**
   - Si ves el texto de volver al menú dos veces en el mismo mensaje

4. **Formato incorrecto**
   - Si el texto no aparece en cursiva (_texto_)
   - Si falta el asterisco en *hola*

---

## ✅ Criterios de Éxito

La funcionalidad está correcta si:

1. ✅ **TODOS** los mensajes incluyen la opción de volver al menú
2. ✅ El comando 'hola' funciona en **cualquier momento**
3. ✅ El comando 'hola' **siempre** muestra el menú principal
4. ✅ La sesión se resetea correctamente al usar 'hola'
5. ✅ El texto está formateado correctamente (cursiva y negrita)

---

## 📝 Reporte de Resultados

Después de probar, completa:

**Fecha de prueba:** _______________

**Escenarios probados:** _____ / 8

**Problemas encontrados:** 
- [ ] Ninguno
- [ ] Ver detalles abajo

**Detalles de problemas:**
```
[Describe aquí cualquier problema encontrado]
```

**Estado final:**
- [ ] ✅ Todas las pruebas pasaron
- [ ] ⚠️ Algunos problemas menores
- [ ] ❌ Problemas críticos encontrados

---

## 💡 Consejos para Probar

1. **Prueba en diferentes momentos del flujo**
   - Al inicio
   - En medio de agendar
   - Después de un error
   - Después de completar una acción

2. **Prueba con diferentes tipos de usuario**
   - Usuario nuevo (sin nombre registrado)
   - Usuario existente
   - Usuario con citas
   - Usuario sin citas

3. **Prueba casos extremos**
   - Enviar 'hola' múltiples veces seguidas
   - Enviar 'hola' en diferentes formatos (HOLA, Hola, hola)
   - Enviar opciones inválidas

4. **Verifica el formato**
   - El texto debe estar en cursiva
   - 'hola' debe estar en negrita
   - Debe haber espacio antes del texto

---

## 🎉 Conclusión

Si todos los escenarios pasan, la funcionalidad está lista para producción y mejorará significativamente la experiencia del usuario.
