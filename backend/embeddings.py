from PIL import Image
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("clip-ViT-B-32")  # vectores de 512 dimensiones


def embedding_de_imagen(img: Image.Image) -> list[float]:
    return modelo.encode(img, normalize_embeddings=True).tolist()


def a_pgvector(v: list[float]) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"