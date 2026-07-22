from transformers import pipeline

nli_model = pipeline("text-classification", model="facebook/bart-large-mnli")

def check_claim(claim: str, chunks: list[dict]) -> str:
    results = []
    for chunk in chunks:
        premise = chunk["text"]
        output = nli_model(premise, text_pair=claim)
        label = output[0]["label"].upper()
        results.append(label)

    if any(label == "ENTAILMENT" for label in results):
        return "Supported"
    if any(label == "CONTRADICTION" for label in results):
        return "Contradicted"
    else:
        return "Unverified"

if __name__ == "__main__":
    test_chunks = [
        {"text": "The perceptron was invented by Frank Rosenblatt in 1958."},
        {"text": "AlexNet was introduced in 2012."},
    ]
    result = check_claim("Frank Rosenblatt invented the perceptron in 1958.", test_chunks)
    print(result)