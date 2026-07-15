from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss_index.index")
with open ("data/chunks_metadata.pkl", "rb") as f:
    chunks = pickle.load(f)

def retriever(query, top_k):
    embedding = model.encode([query])
    embedding = np.array(embedding).astype("float32")
    
    distances, indices = index.search(embedding, top_k)
    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results

if __name__ == "__main__":
    results = retriever("What is a perceptron?", top_k=3)
    for r in results:
        print(r["source"], "-", r["text"][:100])