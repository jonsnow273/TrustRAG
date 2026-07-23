from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from chunker import process_documents, chunker_text
import pickle
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

CONFIGS = [
    (150, 30),
    (300, 50),
    (500, 80),
]


def build_and_save_index(chunk_size, overlap, folder_path="data/raw_docs"):
    all_chunks = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunker_text(text, chunk_size, overlap)
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source": file_name,
                    "chunk_id": i,
                })

    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    index_path = f"data/faiss_index_{chunk_size}.index"
    metadata_path = f"data/chunks_metadata_{chunk_size}.pkl"

    faiss.write_index(index, index_path)
    with open(metadata_path, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"Saved chunk_size={chunk_size}: {index.ntotal} chunks -> {index_path}")


if __name__ == "__main__":
    for chunk_size, overlap in CONFIGS:
        build_and_save_index(chunk_size, overlap)

    print("All indices built and saved.")