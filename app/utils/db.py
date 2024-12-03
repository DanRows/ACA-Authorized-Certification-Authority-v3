import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.database import Base, Client, ClientStatus, Equipment


class DatabaseManager:
    def __init__(self):
        # Crear directorio data si no existe
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # URL para SQLite
        self.db_url = f"sqlite:///{data_dir}/acma.db"

        # Crear engine y sesión
        self.engine = create_engine(
            self.db_url,
            connect_args={"check_same_thread": False}  # Necesario para SQLite
        )

        # Crear tablas
        Base.metadata.create_all(self.engine)

        # Crear fábrica de sesiones
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @contextmanager
    def get_db(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def add_sample_data(self, db: Session) -> None:
        """Agrega datos de ejemplo a la base de datos"""
        try:
            # Verificar si ya hay datos
            if db.query(Client).count() > 0:
                return

            # Agregar clientes de ejemplo
            clients = [
                Client(
                    name="Cliente 1",
                    status=ClientStatus.ACTIVE,
                    satisfaction_score=4.5
                ),
                Client(
                    name="Cliente 2",
                    status=ClientStatus.ACTIVE,
                    satisfaction_score=4.0
                )
            ]
            db.add_all(clients)
            db.commit()

            # Agregar equipos de ejemplo
            equipment = [
                Equipment(
                    client_id=1,
                    type="Tipo A",
                    calibration_date=datetime.now() - timedelta(days=30),
                    next_calibration=datetime.now() + timedelta(days=335),
                    status="calibrated"
                ),
                Equipment(
                    client_id=2,
                    type="Tipo B",
                    calibration_date=datetime.now() - timedelta(days=60),
                    next_calibration=datetime.now() + timedelta(days=305),
                    status="calibrated"
                )
            ]
            db.add_all(equipment)
            db.commit()

        except Exception as e:
            db.rollback()
            raise e
