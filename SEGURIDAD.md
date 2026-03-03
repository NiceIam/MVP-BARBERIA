# 🔐 Guía de Seguridad

## ⚠️ Información Sensible

Este proyecto maneja información sensible que NO debe ser compartida públicamente:

### Archivos que NUNCA deben subirse a Git:

- `.env` - Contiene credenciales de base de datos y API keys
- `.env.local`
- `.env.production`
- Cualquier archivo con credenciales

### ✅ Verificar que .env esté ignorado

```bash
# Verificar que .env esté en .gitignore
cat .gitignore | grep .env

# Verificar que .env NO esté en el repositorio
git ls-files .env
# (No debería mostrar nada)
```

## 🚨 Si ya subiste credenciales a Git

Si accidentalmente subiste el archivo `.env` con credenciales:

### 1. Remover del índice de Git

```bash
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

### 2. Cambiar TODAS las credenciales

Es CRÍTICO que cambies:

- ✅ Contraseña de la base de datos
- ✅ API Key de Evolution API
- ✅ Cualquier otra credencial que estuviera en el archivo

### 3. Limpiar el historial (opcional pero recomendado)

Si el archivo ya fue pusheado, las credenciales quedan en el historial de Git:

```bash
# Usar git filter-branch o BFG Repo-Cleaner
# Ver: https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

## 📋 Checklist de Seguridad

Antes de hacer el repositorio público:

- [ ] `.env` está en `.gitignore`
- [ ] `.env` NO está en el repositorio (`git ls-files .env` no muestra nada)
- [ ] Existe `.env.example` con valores de ejemplo
- [ ] Toda la documentación usa valores genéricos (no credenciales reales)
- [ ] Se cambió la contraseña de la base de datos
- [ ] Se cambió la API Key de Evolution API
- [ ] Se revisó el historial de commits en busca de credenciales

## 🔒 Mejores Prácticas

### Para Desarrollo

1. Usa `.env` para desarrollo local
2. NUNCA hagas commit de `.env`
3. Comparte `.env.example` con el equipo
4. Documenta qué variables se necesitan

### Para Producción

1. Usa variables de entorno del sistema
2. Usa servicios de gestión de secretos (AWS Secrets Manager, HashiCorp Vault, etc.)
3. Rota las credenciales regularmente
4. Usa diferentes credenciales para cada ambiente

### Para Colaboradores

1. Cada desarrollador debe crear su propio `.env`
2. Usa `.env.example` como plantilla
3. NUNCA compartas tu `.env` por email, chat, etc.

## 📚 Recursos

- [GitHub: Removing sensitive data](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Git: gitignore](https://git-scm.com/docs/gitignore)
- [12 Factor App: Config](https://12factor.net/config)

## 🆘 En Caso de Exposición

Si descubres que las credenciales fueron expuestas:

1. **INMEDIATAMENTE** cambia todas las credenciales
2. Revoca las API keys comprometidas
3. Revisa los logs en busca de accesos no autorizados
4. Notifica a tu equipo
5. Considera usar un servicio de rotación automática de credenciales
