from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = Groq(api_key=API_KEY)


def generate_answer(question, chunks):
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
    return answer


if __name__ == "__main__":
    from retriever.retriever import retriever  # only needed for standalone testing
    test_chunks = retriever("What is perceptron?", top_k=3, chunk_size=300)
    answer = generate_answer("What is perceptron?", test_chunks)
    print(answer)