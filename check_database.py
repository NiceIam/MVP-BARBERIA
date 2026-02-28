"""
Script para verificar el estado de la base de datos
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_database():
    """Verifica el estado de la base de datos"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL no está configurada")
        return
    
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("\n✅ Conexión exitosa a PostgreSQL")
        
        # Verificar tablas existentes
        print("\n📊 Tablas existentes:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tablas = cursor.fetchall()
        if tablas:
            for tabla in tablas:
                print(f"  ✓ {tabla[0]}")
        else:
            print("  ⚠️  No hay tablas creadas")
        
        # Verificar columnas de cada tabla
        tablas_esperadas = ['clientes', 'citas', 'sesiones_chat']
        
        for tabla in tablas_esperadas:
            print(f"\n📋 Estructura de '{tabla}':")
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{tabla}'
                ORDER BY ordinal_position
            """)
            
            columnas = cursor.fetchall()
            if columnas:
                for col in columnas:
                    nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                    print(f"  - {col[0]}: {col[1]} ({nullable})")
            else:
                print(f"  ⚠️  Tabla '{tabla}' no existe")
        
        # Verificar índices
        print("\n📑 Índices:")
        cursor.execute("""
            SELECT indexname, tablename
            FROM pg_indexes
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname
        """)
        
        indices = cursor.fetchall()
        if indices:
            for idx in indices:
                print(f"  - {idx[0]} en {idx[1]}")
        else:
            print("  ⚠️  No hay índices creados")
        
        # Contar registros
        print("\n📈 Registros:")
        for tabla in tablas_esperadas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"  - {tabla}: {count} registros")
            except:
                print(f"  - {tabla}: tabla no existe")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Soluciones posibles:")
        print("  1. Verifica que PostgreSQL esté corriendo")
        print("  2. Verifica las credenciales en .env")
        print("  3. Ejecuta: python reset_database.py")


if __name__ == "__main__":
    check_database()
