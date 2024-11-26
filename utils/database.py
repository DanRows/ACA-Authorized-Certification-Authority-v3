import psycopg2
from psycopg2.extras import RealDictCursor
from config.configuration import Configuration
from config.secrets_manager import SecretsManager

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.config = Configuration()
        self.conn = None
        self._connect()
        
    def _connect(self):
        try:
            db_url = SecretsManager.get_secret("DATABASE_URL") or \
                     self.config.get_setting("database_url")
            
            self.conn = psycopg2.connect(
                db_url,
                cursor_factory=RealDictCursor
            )
            self._create_tables()
        except Exception as e:
            print(f"Error de conexión: {e}")
    
    def _create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
                user_data JSONB NOT NULL,
                type VARCHAR(50) NOT NULL,
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS certificates (
                id SERIAL PRIMARY KEY,
                request_id INTEGER REFERENCES requests(id),
                file_path VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        with self.conn.cursor() as cur:
            for query in queries:
                cur.execute(query)
        self.conn.commit()
    
    def execute(self, query, params=None):
        if not self.conn:
            self._connect()
            
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    
    def execute_one(self, query, params=None):
        if not self.conn:
            self._connect()
            
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone() 