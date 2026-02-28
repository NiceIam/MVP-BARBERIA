"""
Módulo de integración con Evolution API para WhatsApp
"""
import os
import requests
from typing import Dict, Optional, List
import json


class EvolutionAPI:
    """Cliente para interactuar con Evolution API"""
    
    def __init__(self, api_url: str, api_key: str, instance_name: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.instance_name = instance_name
        self.headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Realiza una petición HTTP a la API"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en petición a Evolution API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta: {e.response.text}")
            return {"error": str(e)}
    
    # GESTIÓN DE INSTANCIA
    
    def verificar_instancia(self) -> Dict:
        """Verifica el estado de la instancia"""
        endpoint = f"/instance/connectionState/{self.instance_name}"
        return self._make_request('GET', endpoint)
    
    def crear_instancia(self) -> Dict:
        """Crea una nueva instancia"""
        endpoint = "/instance/create"
        data = {
            "instanceName": self.instance_name,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }
        return self._make_request('POST', endpoint, data)
    
    def conectar_instancia(self) -> Dict:
        """Conecta la instancia (obtiene QR)"""
        endpoint = f"/instance/connect/{self.instance_name}"
        return self._make_request('GET', endpoint)
    
    def obtener_qr(self) -> Dict:
        """Obtiene el código QR para conectar WhatsApp"""
        endpoint = f"/instance/qrcode/{self.instance_name}"
        return self._make_request('GET', endpoint)
    
    def desconectar_instancia(self) -> Dict:
        """Desconecta la instancia"""
        endpoint = f"/instance/logout/{self.instance_name}"
        return self._make_request('DELETE', endpoint)
    
    # ENVÍO DE MENSAJES
    
    def enviar_mensaje_texto(self, numero: str, mensaje: str) -> Dict:
        """Envía un mensaje de texto a un número de WhatsApp"""
        endpoint = f"/message/sendText/{self.instance_name}"
        
        # Limpiar número (remover caracteres especiales)
        numero_limpio = ''.join(filter(str.isdigit, numero))
        
        # Agregar código de país si no lo tiene (Colombia por defecto)
        if not numero_limpio.startswith('57'):
            numero_limpio = '57' + numero_limpio
        
        data = {
            "number": numero_limpio,
            "text": mensaje
        }
        
        return self._make_request('POST', endpoint, data)
    
    def enviar_mensaje_con_botones(self, numero: str, mensaje: str, botones: List[str]) -> Dict:
        """Envía un mensaje con botones interactivos"""
        endpoint = f"/message/sendButtons/{self.instance_name}"
        
        numero_limpio = ''.join(filter(str.isdigit, numero))
        if not numero_limpio.startswith('57'):
            numero_limpio = '57' + numero_limpio
        
        buttons_data = [{"buttonText": btn} for btn in botones[:3]]  # Máximo 3 botones
        
        data = {
            "number": numero_limpio,
            "title": "Opciones",
            "description": mensaje,
            "buttons": buttons_data
        }
        
        return self._make_request('POST', endpoint, data)
    
    def enviar_mensaje_con_lista(self, numero: str, titulo: str, mensaje: str, 
                                  opciones: List[Dict]) -> Dict:
        """Envía un mensaje con lista de opciones"""
        endpoint = f"/message/sendList/{self.instance_name}"
        
        numero_limpio = ''.join(filter(str.isdigit, numero))
        if not numero_limpio.startswith('57'):
            numero_limpio = '57' + numero_limpio
        
        data = {
            "number": numero_limpio,
            "title": titulo,
            "description": mensaje,
            "buttonText": "Ver opciones",
            "sections": [
                {
                    "title": "Selecciona una opción",
                    "rows": opciones
                }
            ]
        }
        
        return self._make_request('POST', endpoint, data)
    
    def enviar_imagen(self, numero: str, url_imagen: str, caption: str = "") -> Dict:
        """Envía una imagen"""
        endpoint = f"/message/sendMedia/{self.instance_name}"
        
        numero_limpio = ''.join(filter(str.isdigit, numero))
        if not numero_limpio.startswith('57'):
            numero_limpio = '57' + numero_limpio
        
        data = {
            "number": numero_limpio,
            "mediatype": "image",
            "media": url_imagen,
            "caption": caption
        }
        
        return self._make_request('POST', endpoint, data)
    
    # GESTIÓN DE MENSAJES
    
    def marcar_como_leido(self, numero: str, message_id: str) -> Dict:
        """Marca un mensaje como leído"""
        endpoint = f"/chat/markMessageAsRead/{self.instance_name}"
        
        numero_limpio = ''.join(filter(str.isdigit, numero))
        if not numero_limpio.startswith('57'):
            numero_limpio = '57' + numero_limpio
        
        data = {
            "remoteJid": f"{numero_limpio}@s.whatsapp.net",
            "id": message_id
        }
        
        return self._make_request('POST', endpoint, data)
    
    # WEBHOOKS
    
    def configurar_webhook(self, webhook_url: str) -> Dict:
        """Configura el webhook para recibir mensajes"""
        endpoint = f"/webhook/set/{self.instance_name}"
        
        data = {
            "url": webhook_url,
            "webhook_by_events": False,
            "events": [
                "MESSAGES_UPSERT",
                "MESSAGES_UPDATE",
                "CONNECTION_UPDATE"
            ]
        }
        
        return self._make_request('POST', endpoint, data)
    
    def obtener_webhook(self) -> Dict:
        """Obtiene la configuración actual del webhook"""
        endpoint = f"/webhook/find/{self.instance_name}"
        return self._make_request('GET', endpoint)
    
    # INFORMACIÓN
    
    def obtener_perfil(self, numero: str) -> Dict:
        """Obtiene información del perfil de un contacto"""
        endpoint = f"/chat/fetchProfile/{self.instance_name}"
        
        numero_limpio = ''.join(filter(str.isdigit, numero))
        if not numero_limpio.startswith('57'):
            numero_limpio = '57' + numero_limpio
        
        data = {
            "number": numero_limpio
        }
        
        return self._make_request('POST', endpoint, data)


# Singleton de Evolution API
_evolution_instance = None

def get_evolution_api() -> EvolutionAPI:
    """Obtiene la instancia singleton de Evolution API"""
    global _evolution_instance
    if _evolution_instance is None:
        api_url = os.getenv("EVOLUTION_API_URL")
        api_key = os.getenv("EVOLUTION_API_KEY")
        instance_name = os.getenv("EVOLUTION_INSTANCE_NAME")
        
        if not all([api_url, api_key, instance_name]):
            raise ValueError("Faltan variables de entorno de Evolution API")
        
        _evolution_instance = EvolutionAPI(api_url, api_key, instance_name)
    
    return _evolution_instance
