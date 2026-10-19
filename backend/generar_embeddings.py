import os
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image
from sqlalchemy import create_engine, text

from embeddings import a_pgvector, embedding_de_imagen

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    prendas = conn.execute(text(
        "SELECT id, imagen_url FROM prenda "
        "WHERE embedding IS NULL AND imagen_url IS NOT NULL"
    )).all()

for id_prenda, url in prendas:
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        emb = a_pgvector(embedding_de_imagen(img))
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE prenda SET embedding = CAST(:e AS vector) WHERE id = :id"),
                {"e": emb, "id": id_prenda},
            )
        print("OK", id_prenda)
    except Exception as e:
        print("Falló", id_prenda, e)