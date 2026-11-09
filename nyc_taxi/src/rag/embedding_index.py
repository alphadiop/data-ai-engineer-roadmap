
import numpy as np
import faiss

from nyc_taxi.src.rag.document_loader import load_markdown_documents
from nyc_taxi.src.rag.embedding_model import create_embedding_model
from nyc_taxi.src.rag.text_splitter import split_text


def build_embeddings(docs_dir: str, model=None):
    documents = load_markdown_documents(docs_dir)

    chunks = [
        {
            "source": document["source"],
            "content": chunk,
        }
        for document in documents
        for chunk in split_text(document["content"])
    ]


    # Réutiliser le modèle reçu, ou en créer un si nécessaire.
    if model is None:
        model = create_embedding_model()

    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return chunks, np.asarray(embeddings, dtype=np.float32)



def build_faiss_index(embeddings: np.ndarray):
    """Construit un index FAISS pour rechercher les vecteurs similaires."""
    if embeddings.ndim != 2 or embeddings.shape[0] == 0:
        raise ValueError("Les embeddings doivent contenir des vecteurs.")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


def search_documents(question: str, docs_dir: str, top_k: int = 3):
    """Retourne les chunks les plus pertinents pour une question."""
    if top_k <= 0:
        raise ValueError("top_k doit être positif.")

    # Charger le modèle une seule fois.
    model = create_embedding_model()

    # Réutiliser cette instance pour vectoriser les documents.
    chunks, embeddings = build_embeddings(docs_dir, model=model)
    index = build_faiss_index(embeddings)

    question_vector = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype(np.float32)

    scores, positions = index.search(
        question_vector,
        min(top_k, len(chunks)),
    )

    results = []
    for score, position in zip(scores[0], positions[0]):
        results.append(
            {
                "source": chunks[position]["source"],
                "content": chunks[position]["content"],
                "score": float(score),
            }
        )

    return results
