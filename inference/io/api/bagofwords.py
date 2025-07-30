from . import api_router
from fastapi import Request,Query
from inference.io.schemas import BoWMethod
from tools.starch_approach import get_vector_for_sentence_scratch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


@api_router.get("/v1/bow/similarity")
def similarity(
    method: BoWMethod,
    request: Request,
    query: str = Query(..., example="Artificial intelligence is good for your productivity"),
):
    corpus = request.app.state.corpus

    if method == BoWMethod.vectorizer:
        vectorizer = request.app.state.vectorizer
        corpus_vectors = request.app.state.vectorizer_vectors
        input_vector = vectorizer.transform([query]).toarray()

    elif method == BoWMethod.scratch:
        vocab = request.app.state.vocab
        corpus_vectors = request.app.state.corpus_vectors
        input_vector = [get_vector_for_sentence_scratch(query, vocab)]
    else:
        raise HTTPException(status_code=400, detail="Invalid method")

    similarities = cosine_similarity(input_vector, corpus_vectors)[0]
    most_similar_idx = int(np.argmax(similarities))

    return {
        "input": query,
        "method": method.value,
        "most_similar": corpus[most_similar_idx],
        "similarity_score": float(similarities[most_similar_idx])
    }
