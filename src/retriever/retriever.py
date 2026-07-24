from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

_loaded_indices = {}


def _load_index(chunk_size):
    if chunk_size not in _loaded_indices:
        index = faiss.read_index(f"data/faiss_index_{chunk_size}.index")
        with open(f"data/chunks_metadata_{chunk_size}.pkl", "rb") as f:
            chunks = pickle.load(f)
        _loaded_indices[chunk_size] = (index, chunks)

    return _loaded_indices[chunk_size]


def retriever(query, top_k, chunk_size=300):
    index, chunks = _load_index(chunk_size)

    embedding = model.encode([query])
    embedding = np.array(embedding).astype("float32")

    distances, indices = index.search(embedding, top_k)
    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


if __name__ == "__main__":
    results = retriever("What is a perceptron?", top_k=3, chunk_size=300)
    for r in results:
        print(r["source"], "-", r["text"][:100])