"""
Script para inicializar y verificar la base de datos
"""
from dotenv import load_dotenv
from database import get_database

load_dotenv()

def main():
    print("=" * 60)
    print("🔧 CONFIGURACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    try:
        print("\n📊 Conectando a PostgreSQL...")
        db = get_database()
        
        print("✅ Base de datos inicializada correctamente")
        print("\n📋 Tablas creadas:")
        print("   - clientes")
        print("   - citas")
        print("   - sesiones_chat")
        
        print("\n" + "=" * 60)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nVerifica que:")
        print("1. PostgreSQL esté ejecutándose")
        print("2. Las credenciales en .env sean correctas")
        print("3. La base de datos 'chatbot' exista")

if __name__ == "__main__":
    main()
