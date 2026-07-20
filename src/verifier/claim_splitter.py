import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = Groq(api_key=API_KEY)

def split_claims(answer_text: str) -> list[str]:

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role" : "system",
                "content" : (
                    "Break the answer into separate, atomic factual claims. "
                    "One claim per line, no numbering, no bullets, no extra commentary."
                )
            },

            {
                "role" : "user",
                "content" : answer_text,
            },
        ],

    )

    response_text = response.choices[0].message.content

    lines = response_text.split("\n")
    claims = []

    for line in lines:
        cleaned = line.strip()
        cleaned = cleaned.lstrip("-•0123456789. ").strip()

        if cleaned:
            claims.append(cleaned)

    return claims


if __name__ == "__main__":
    example_answer = (
        "A perceptron is a simple neural network invented by Frank Rosenblatt in 1958. "
        "It can only solve linearly separable problems."
    )

    claims = split_claims(example_answer)
    for c in claims:
        print(c)
        