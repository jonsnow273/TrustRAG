from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from chunker import process_documents
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = process_documents("data/raw_docs")
texts = [chunk["text"] for chunk in chunks]
embedding = model.encode(texts)

embedding = np.array(embedding).astype("float32")

dimention = embedding.shape[1]
index = faiss.IndexFlatL2(dimention)
index.add(embedding)
print(index.ntotal)

faiss.write_index(index, "data/faiss_index.index")
with open("data/chunks_metadata.pkl", "wb") as f:
    pickle.dump(chunks, f)
    
print("saved")