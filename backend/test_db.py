import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    for fila in conn.execute(text("SELECT id, nombre FROM local")):
        print(fila)
