import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
app = FastAPI(title="ShopLook API")

# --- 1. CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def consultar(sql: str, params: dict | None = None):
    with engine.connect() as conn:
        filas = conn.execute(text(sql), params or {})
        return [dict(f._mapping) for f in filas]


# --- 2. Endpoints ---
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


@app.get("/locales/{local_id}")
def get_local(local_id: int):
    filas = consultar("""
        SELECT id, nombre, descripcion, direccion, telefono,
               es_mayorista, tiene_stock,
               ST_Y(ubicacion::geometry) AS lat,
               ST_X(ubicacion::geometry) AS lng
        FROM local
        WHERE id = :id
    """, {"id": local_id})
    if not filas:
        raise HTTPException(status_code=404, detail="Local no encontrado")

    local = filas[0]
    local["horarios"] = consultar(
        "SELECT dia_semana, abre, cierra FROM horario "
        "WHERE id_local = :id ORDER BY dia_semana, abre",
        {"id": local_id},
    )
    local["redes"] = consultar(
        "SELECT tipo, url FROM red_social WHERE id_local = :id",
        {"id": local_id},
    )
    return local


@app.get("/descuentos/hoy")
def descuentos_hoy():
    ahora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    hoy = ahora.date()
    dia = hoy.weekday()  # 0 = lunes ... 6 = domingo (ajustar si tu tabla usa otra convención)

    return consultar("""
        SELECT d.id, d.id_local, l.nombre AS local,
               b.nombre AS banco, d.porcentaje, d.condiciones
        FROM descuento d
        JOIN local l ON l.id = d.id_local
        LEFT JOIN banco b ON b.id = d.id_banco
        WHERE (d.dia_semana IS NULL OR d.dia_semana = :dia)
          AND (d.vigente_desde IS NULL OR d.vigente_desde <= :hoy)
          AND (d.vigente_hasta IS NULL OR d.vigente_hasta >= :hoy)
        ORDER BY d.porcentaje DESC
    """, {"dia": dia, "hoy": hoy})


@app.get("/locales/{local_id}/bancos")
def bancos_del_local(local_id: int):
    return consultar("""
        SELECT DISTINCT b.id, b.nombre
        FROM descuento d
        JOIN banco b ON b.id = d.id_banco
        WHERE d.id_local = :id
        ORDER BY b.nombre
    """, {"id": local_id})


class ReseniaIn(BaseModel):
    id_usuaria: int  # temporal: cuando haya login, sale del token
    puntaje: int = Field(ge=1, le=5)
    comentario: str = ""


@app.get("/locales/{local_id}/resenias")
def get_resenias(local_id: int):
    return consultar("""
        SELECT r.id, u.nombre AS usuaria, r.puntaje, r.comentario, r.creada_en
        FROM resenia r
        JOIN usuaria u ON u.id = r.id_usuaria
        WHERE r.id_local = :id
        ORDER BY r.creada_en DESC
    """, {"id": local_id})


@app.post("/locales/{local_id}/resenias", status_code=201)
def crear_resenia(local_id: int, resenia: ReseniaIn):
    sql = text("""
        INSERT INTO resenia (id_local, id_usuaria, puntaje, comentario)
        VALUES (:id_local, :id_usuaria, :puntaje, :comentario)
        RETURNING id, id_local, id_usuaria, puntaje, comentario, creada_en
    """)
    try:
        with engine.begin() as conn:
            fila = conn.execute(sql, {**resenia.model_dump(), "id_local": local_id}).first()
            return dict(fila._mapping)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Local o usuaria inexistente")
    

@app.get("/categorias")
def get_categorias():
    return consultar("SELECT id, nombre, id_padre FROM categoria ORDER BY nombre")