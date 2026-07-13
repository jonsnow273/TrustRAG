import os 

def chunker_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start += chunk_size - overlap 
    return chunks


def process_documents(folder_path):
    all_chunks = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            filepath =  os.path.join(folder_path, file_name)
            with open(filepath, "r", encoding='utf-8') as file:
                text = file.read()

            chunks = chunker_text(text, 300, 50)

            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source": file_name,
                    "chunk_id": i,
                })
    return all_chunks


if __name__ == "__main__":
    result = process_documents("data/raw_docs")
    print(f"Total chunks created: {len(result)}")
    print(result[0])