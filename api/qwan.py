from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache


# ==============================
# Load único do modelo
# ==============================

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


# ==============================
# Embedding
# ==============================

def embed_texts(texts):
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


# ==============================
# Núcleo QWAN
# ==============================

def qwan_score(texts):
    """
    Mede coerência estrutural entre textos.
    """

    if len(texts) < 2:
        return 1.0

    embeddings = embed_texts(texts)

    # Similaridade média par-a-par
    sim_matrix = cosine_similarity(embeddings)

    # Remover diagonal
    mask = ~np.eye(sim_matrix.shape[0], dtype=bool)
    mean_similarity = sim_matrix[mask].mean()

    # Centroide
    centroid = embeddings.mean(axis=0)

    # Distância média ao centro
    distances = np.linalg.norm(embeddings - centroid, axis=1)
    structural_variance = distances.mean()

    # QWAN score híbrido
    score = (mean_similarity * 0.7) + ((1 - structural_variance) * 0.3)

    return float(score)


# ==============================
# Similaridade contextual
# ==============================

def semantic_search(query, corpus):
    model = get_model()

    query_emb = model.encode([query], convert_to_numpy=True)
    corpus_emb = model.encode(corpus, convert_to_numpy=True)

    sims = cosine_similarity(query_emb, corpus_emb)[0]

    ranked = sorted(
        zip(corpus, sims),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked
