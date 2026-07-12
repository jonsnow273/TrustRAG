import wikipediaapi
import os

wiki = wikipediaapi.Wikipedia(user_agent="TrustRAG-project", language="en")

topics = [
    "History of artificial intelligence",
    "Timeline of artificial intelligence",
    "AI winter",
    "Turing test",
    "Perceptron",
    "Deep Blue (chess computer)",
    "AlexNet",
    "Transformer (deep learning architecture)",
    "ImageNet",
    "Expert system",
    "Machine learning"
]

os.makedirs("data/raw_docs", exist_ok=True)

for topic in topics:
    page = wiki.page(topic)
    if page.exists():
        filename = f"data/raw_docs/{topic.replace(' ', '_').replace('/', '-')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page.text)
        print(f"Saved: {filename}")
    else:
        print(f"Not found: {topic}")