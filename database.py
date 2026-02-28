"""
Módulo de gestión de base de datos PostgreSQL
"""
import os
from datetime import datetime
from typing import List, Optional, Dict
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


class Database:
    """Clase para gestionar la conexión y operaciones con PostgreSQL"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones a la base de datos"""
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_database(self):
        """Inicializa las tablas de la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Tabla de clientes
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(255) NOT NULL,
                        telefono VARCHAR(50) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                
                # Tabla de citas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS citas (
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
                conn.commit()
                
                # Tabla de sesiones de chat
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sesiones_chat (
                        id SERIAL PRIMARY KEY,
                        telefono VARCHAR(50) UNIQUE NOT NULL,
                        estado VARCHAR(100) NOT NULL,
                        datos_temporales JSONB,
                        ultima_interaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                
                # Índices para mejorar rendimiento (solo si no existen)
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_citas_cliente_id ON citas(cliente_id)
                    """)
                    conn.commit()
                except Exception as e:
                    print(f"Índice idx_citas_cliente_id ya existe o error: {e}")
                    conn.rollback()
                
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(fecha)
                    """)
                    conn.commit()
                except Exception as e:
                    print(f"Índice idx_citas_fecha ya existe o error: {e}")
                    conn.rollback()
                
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_sesiones_telefono ON sesiones_chat(telefono)
                    """)
                    conn.commit()
                except Exception as e:
                    print(f"Índice idx_sesiones_telefono ya existe o error: {e}")
                    conn.rollback()
                
                print("✅ Base de datos inicializada correctamente")
                
            except Exception as e:
                print(f"❌ Error inicializando base de datos: {e}")
                conn.rollback()
                raise
    
    # OPERACIONES DE CLIENTES
    
    def crear_cliente(self, nombre: str, telefono: str) -> int:
        """Crea un nuevo cliente o retorna el ID si ya existe"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar si el cliente ya existe
            cursor.execute(
                "SELECT id FROM clientes WHERE telefono = %s",
                (telefono,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado[0]
            
            # Crear nuevo cliente
            cursor.execute(
                """
                INSERT INTO clientes (nombre, telefono)
                VALUES (%s, %s)
                RETURNING id
                """,
                (nombre, telefono)
            )
            return cursor.fetchone()[0]
    
    def obtener_cliente_por_telefono(self, telefono: str) -> Optional[Dict]:
        """Obtiene un cliente por su número de teléfono"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM clientes WHERE telefono = %s",
                (telefono,)
            )
            return cursor.fetchone()
    
    def buscar_clientes(self, busqueda: str) -> List[Dict]:
        """Busca clientes por nombre o teléfono"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT * FROM clientes 
                WHERE LOWER(nombre) LIKE LOWER(%s) OR telefono LIKE %s
                """,
                (f"%{busqueda}%", f"%{busqueda}%")
            )
            return cursor.fetchall()
    
    # OPERACIONES DE CITAS
    
    def crear_cita(self, cliente_id: int, servicio: str, precio: float, 
                   duracion: int, barbero: str, fecha: str, hora: str) -> int:
        """Crea una nueva cita"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO citas (cliente_id, servicio, precio, duracion, barbero, fecha, hora)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (cliente_id, servicio, precio, duracion, barbero, fecha, hora)
            )
            return cursor.fetchone()[0]
    
    def obtener_citas_cliente(self, cliente_id: int) -> List[Dict]:
        """Obtiene todas las citas de un cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT c.*, cl.nombre as cliente_nombre, cl.telefono as cliente_telefono
                FROM citas c
                JOIN clientes cl ON c.cliente_id = cl.id
                WHERE c.cliente_id = %s AND c.estado = 'confirmada'
                ORDER BY c.fecha, c.hora
                """,
                (cliente_id,)
            )
            return cursor.fetchall()
    
    def obtener_citas_por_telefono(self, telefono: str) -> List[Dict]:
        """Obtiene todas las citas de un cliente por su teléfono"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT c.*, cl.nombre as cliente_nombre, cl.telefono as cliente_telefono
                FROM citas c
                JOIN clientes cl ON c.cliente_id = cl.id
                WHERE cl.telefono = %s AND c.estado = 'confirmada'
                ORDER BY c.fecha, c.hora
                """,
                (telefono,)
            )
            return cursor.fetchall()
    
    def cancelar_citas_cliente(self, cliente_id: int) -> int:
        """Cancela todas las citas de un cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE citas 
                SET estado = 'cancelada', updated_at = CURRENT_TIMESTAMP
                WHERE cliente_id = %s AND estado = 'confirmada'
                """,
                (cliente_id,)
            )
            return cursor.rowcount
    
    def obtener_horarios_ocupados(self, fecha: str) -> List[str]:
        """Obtiene las horas ocupadas para una fecha específica"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT hora FROM citas 
                WHERE fecha = %s AND estado = 'confirmada'
                """,
                (fecha,)
            )
            return [str(row[0]) for row in cursor.fetchall()]
    
    # OPERACIONES DE SESIONES
    
    def guardar_sesion(self, telefono: str, estado: str, datos_temporales: Dict):
        """Guarda o actualiza una sesión de chat"""
        import json
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO sesiones_chat (telefono, estado, datos_temporales, ultima_interaccion)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (telefono) 
                DO UPDATE SET 
                    estado = EXCLUDED.estado,
                    datos_temporales = EXCLUDED.datos_temporales,
                    ultima_interaccion = CURRENT_TIMESTAMP
                """,
                (telefono, estado, json.dumps(datos_temporales))
            )
    
    def obtener_sesion(self, telefono: str) -> Optional[Dict]:
        """Obtiene una sesión de chat"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM sesiones_chat WHERE telefono = %s",
                (telefono,)
            )
            return cursor.fetchone()
    
    def eliminar_sesion(self, telefono: str):
        """Elimina una sesión de chat"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM sesiones_chat WHERE telefono = %s",
                (telefono,)
            )
    
    def limpiar_sesiones_antiguas(self, horas: int = 24):
        """Limpia sesiones inactivas por más de X horas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM sesiones_chat 
                WHERE ultima_interaccion < NOW() - INTERVAL '%s hours'
                """,
                (horas,)
            )
            return cursor.rowcount


# Singleton de la base de datos
_db_instance = None

def get_database() -> Database:
    """Obtiene la instancia singleton de la base de datos"""
    global _db_instance
    if _db_instance is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL no está configurada")
        _db_instance = Database(database_url)
    return _db_instance
