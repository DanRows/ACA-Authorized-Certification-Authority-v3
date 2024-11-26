from datetime import datetime
from typing import Dict, List, Optional
import uuid
from utils.helpers import get_database_connection

class Solicitudes:
    def __init__(self):
        self.conn = get_database_connection()
        self._init_db()
        
    def _init_db(self):
        if not self.conn:
            self.requests = []
            return
            
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id UUID PRIMARY KEY,
                    user_data JSONB,
                    type VARCHAR(50),
                    status VARCHAR(20),
                    created_at TIMESTAMP
                )
            """)
        self.conn.commit()
        
    def add_request(self, user_data: Dict, request_type: str) -> Dict:
        request_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO requests (id, user_data, type, status, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (request_id, user_data, request_type, "pending", timestamp))
            self.conn.commit()
        else:
            self.requests.append({
                "id": request_id,
                "user_data": user_data,
                "type": request_type,
                "status": "pending",
                "created_at": timestamp
            })
            
        return {"message": "Solicitud creada", "request_id": request_id}
        
    def get_requests(self) -> List[Dict]:
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM requests ORDER BY created_at DESC")
                return cur.fetchall()
        return self.requests
