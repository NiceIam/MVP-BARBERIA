"""
Script de inicio rápido que verifica y configura todo automáticamente
"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def verificar_conexion_db():
    """Verifica la conexión a la base de datos"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL no está configurada en .env")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return False


def verificar_tablas():
    """Verifica que las tablas existan"""
    database_url = os.getenv("DATABASE_URL")
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Verificar tabla clientes
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'clientes'
            )
        """)
        
        existe = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return existe
    except:
        return False


def inicializar_db():
    """Inicializa la base de datos"""
    print("\n📊 Inicializando base de datos...")
    
    try:
        from database import get_database
        db = get_database()
        print("✅ Base de datos inicializada")
        return True
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False


def iniciar_servidor():
    """Inicia el servidor"""
    print("\n🚀 Iniciando servidor...")
    
    try:
        import uvicorn
        from server import app
        
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        
        print(f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          💈 CHATBOT BARBERÍA - WHATSAPP BOT 💈          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🌐 Servidor: http://{host}:{port}
📡 Webhook: http://{host}:{port}/webhook
🔧 Health: http://{host}:{port}/health
📊 Stats: http://{host}:{port}/stats

Presiona CTRL+C para detener el servidor
""")
        
        uvicorn.run(
            "server:app",
            host=host,
            port=port,
            reload=False
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 INICIO RÁPIDO - CHATBOT BARBERÍA")
    print("=" * 60)
    
    # 1. Verificar conexión a base de datos
    print("\n[1/3] Verificando conexión a PostgreSQL...")
    if not verificar_conexion_db():
        print("\n💡 Solución:")
        print("  1. Verifica que PostgreSQL esté corriendo")
        print("  2. Verifica las credenciales en .env")
        sys.exit(1)
    print("✅ Conexión a PostgreSQL exitosa")
    
    # 2. Verificar/Inicializar tablas
    print("\n[2/3] Verificando tablas de base de datos...")
    if not verificar_tablas():
        print("⚠️  Tablas no encontradas, inicializando...")
        if not inicializar_db():
            print("\n💡 Solución:")
            print("  Ejecuta: python reset_database.py")
            sys.exit(1)
    else:
        print("✅ Tablas verificadas")
    
    # 3. Iniciar servidor
    print("\n[3/3] Todo listo para iniciar")
    print("=" * 60)
    
    iniciar_servidor()


if __name__ == "__main__":
    main()
