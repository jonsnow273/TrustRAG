from groq import Groq
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retriever"))
from retriever import retriever

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)


def generate_answer(question, top_k=3):
    chunks = retriever(question, top_k=top_k)
    context = " ".join([c["text"] for c in chunks])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Use only the provided context to answer the user's question. "
                    "If the answer is not in the context, say you don't know. "
                    "Explain in simple, plain language, avoiding technical jargon and formulas where possible. "
                    "Give real life examples and explain everything if possible."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )

    answer = response.choices[0].message.content
    return answer, chunks


if __name__ == "__main__":
    answer, chunks = generate_answer("What is perceptron?", top_k=3)
    print(answer)