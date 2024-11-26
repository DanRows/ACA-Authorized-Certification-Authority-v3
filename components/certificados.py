from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
from utils.helpers import validate_input

class Certificados:
    def __init__(self):
        self.template_path = "frontend/assets/certificate_template.png"
        self.output_path = "frontend/assets/generated"
        self._ensure_directories()
        
    def _ensure_directories(self):
        os.makedirs(self.output_path, exist_ok=True)
        
    def generate_certificate(self, user_data):
        """
        Genera un certificado basado en los datos del usuario.
        """
        if not validate_input(user_data, {
            "name": {"type": str},
            "type": {"type": str, "optional": True}
        }):
            raise ValueError("Datos de usuario inválidos")
            
        certificate_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_data['name']}"
        output_file = f"{self.output_path}/{certificate_id}.png"
        
        try:
            # Aquí iría la lógica real de generación del certificado
            # Por ahora retornamos un mensaje simulado
            return {
                "message": f"Certificado generado para {user_data['name']}",
                "path": output_file,
                "id": certificate_id
            }
        except Exception as e:
            raise Exception(f"Error generando certificado: {str(e)}")
