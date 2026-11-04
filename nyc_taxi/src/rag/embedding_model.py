
from sentence_transformers import SentenceTransformer


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def create_embedding_model():
    """Charge le modèle chargé de transformer les textes en vecteurs."""
    return SentenceTransformer(MODEL_NAME)
