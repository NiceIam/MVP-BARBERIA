"""
Script para limpiar y recrear las tablas de la base de datos
ADVERTENCIA: Este script eliminará todos los datos existentes
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def reset_database():
    """Elimina y recrea todas las tablas"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL no está configurada")
        return
    
    print("=" * 60)
    print("⚠️  ADVERTENCIA: RESET DE BASE DE DATOS")
    print("=" * 60)
    print("\nEsto eliminará TODAS las tablas y datos existentes:")
    print("  - clientes")
    print("  - citas")
    print("  - sesiones_chat")
    print("\n¿Estás seguro? (escribe 'SI' para continuar)")
    
    confirmacion = input("> ").strip()
    
    if confirmacion != "SI":
        print("\n❌ Operación cancelada")
        return
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("\n🗑️  Eliminando tablas existentes...")
        
        # Eliminar tablas en orden inverso (por las foreign keys)
        cursor.execute("DROP TABLE IF EXISTS citas CASCADE")
        cursor.execute("DROP TABLE IF EXISTS sesiones_chat CASCADE")
        cursor.execute("DROP TABLE IF EXISTS clientes CASCADE")
        
        conn.commit()
        print("✅ Tablas eliminadas")
        
        print("\n📊 Creando tablas nuevas...")
        
        # Crear tabla de clientes
        cursor.execute("""
            CREATE TABLE clientes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                telefono VARCHAR(50) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'clientes' creada")
        
        # Crear tabla de citas
        cursor.execute("""
            CREATE TABLE citas (
                id SERIAL PRIMARY KEY,
                cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
                servicio VARCHAR(255) NOT NULL,
                precio DECIMAL(10, 2) NOT NULL,
                duracion INTEGER NOT NULL,
                barbero VARCHAR(255) NOT NULL,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estado VARCHAR(50) DEFAULT 'confirmada',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'citas' creada")
        
        # Crear tabla de sesiones
        cursor.execute("""
            CREATE TABLE sesiones_chat (
                id SERIAL PRIMARY KEY,
                telefono VARCHAR(50) UNIQUE NOT NULL,
                estado VARCHAR(100) NOT NULL,
                datos_temporales JSONB,
                ultima_interaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'sesiones_chat' creada")
        
        # Crear índices
        print("\n📑 Creando índices...")
        cursor.execute("CREATE INDEX idx_citas_cliente_id ON citas(cliente_id)")
        cursor.execute("CREATE INDEX idx_citas_fecha ON citas(fecha)")
        cursor.execute("CREATE INDEX idx_sesiones_telefono ON sesiones_chat(telefono)")
        print("✅ Índices creados")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ BASE DE DATOS RESETEADA EXITOSAMENTE")
        print("=" * 60)
        print("\nPuedes iniciar el servidor con:")
        print("  python server.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    reset_database()
