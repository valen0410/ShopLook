import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
app = FastAPI()

@app.get("/locales")
def locales_cercanos(lat: float, lng: float, radio: int = 2000):
    sql = text("""
        SELECT l.id, l.nombre, l.direccion,
               ST_Y(l.ubicacion::geometry) AS lat,
               ST_X(l.ubicacion::geometry) AS lng,
               ST_Distance(l.ubicacion, ST_MakePoint(:lng, :lat)::geography) AS metros
        FROM local l
        WHERE ST_DWithin(l.ubicacion, ST_MakePoint(:lng, :lat)::geography, :radio)
        ORDER BY metros
    """)
    with engine.connect() as conn:
        filas = conn.execute(sql, {"lat": lat, "lng": lng, "radio": radio})
        return [dict(f._mapping) for f in filas]