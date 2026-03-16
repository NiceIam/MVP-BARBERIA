#!/bin/bash

# Script para obtener chats usando curl
# Evolution API v2

BASE_URL="https://n8n-evolution-api-barberia.dtbfmw.easypanel.host"
API_KEY="429683C4C977415CAAFCCE10F7D57E11"
INSTANCE="barberiaChurco"

echo "======================================================================="
echo "📱 OBTENIENDO CHATS CON CURL"
echo "======================================================================="

# Opción 1: Fetch all contacts
echo ""
echo "1️⃣ Intentando: /chat/fetchAllContacts"
curl -X GET "${BASE_URL}/chat/fetchAllContacts/${INSTANCE}" \
  -H "apikey: ${API_KEY}" \
  -H "Content-Type: application/json" \
  2>/dev/null | python -m json.tool 2>/dev/null || echo "❌ No funciona"

# Opción 2: Find messages (puede incluir info de chats)
echo ""
echo "2️⃣ Intentando: /chat/findMessages"
curl -X POST "${BASE_URL}/chat/findMessages/${INSTANCE}" \
  -H "apikey: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50}' \
  2>/dev/null | python -m json.tool 2>/dev/null || echo "❌ No funciona"

# Opción 3: Instance info
echo ""
echo "3️⃣ Intentando: /instance/fetchInstances"
curl -X GET "${BASE_URL}/instance/fetchInstances" \
  -H "apikey: ${API_KEY}" \
  -H "Content-Type: application/json" \
  2>/dev/null | python -m json.tool 2>/dev/null || echo "❌ No funciona"

echo ""
echo "======================================================================="
