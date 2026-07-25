import os
import pickle
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "config_selector"))
sys.path.append(os.path.join(os.path.dirname(__file__), "retriever"))
sys.path.append(os.path.join(os.path.dirname(__file__), "generator"))
sys.path.append(os.path.join(os.path.dirname(__file__), "verifier"))

from feature import extract_features
from retriever import retriever
from generate_answers import generate_answer
from claim_splitter import split_claims
from nli_checker import check_claim

with open(os.path.join(os.path.dirname(__file__), "..", "data", "config_selector_model.pkl"), "rb") as f:
    saved = pickle.load(f)
    selector_model = saved["model"]
    expected_columns = saved["columns"]


def predict_config(question):
    features = extract_features(question)
    features_df = pd.DataFrame([features])
    features_df = pd.get_dummies(features_df, columns=["question_word"])

    features_df = features_df.reindex(columns=expected_columns, fill_value=0)

    prediction = selector_model.predict(features_df)[0]
    chunk_size, top_k = prediction.split("_")
    return int(chunk_size), int(top_k)


def run_pipeline(question):
    chunk_size, top_k = predict_config(question)

    chunks = retriever(question, top_k=top_k, chunk_size=chunk_size)

    answer = generate_answer(question, chunks)

    claims = split_claims(answer)

    claim_results = []
    for claim in claims:
        label = check_claim(claim, chunks)
        claim_results.append({"claim": claim, "status": label})

    return {
        "question": question,
        "chunk_size": chunk_size,
        "top_k": top_k,
        "answer": answer,
        "claims": claim_results,
    }


if __name__ == "__main__":
    result = run_pipeline("What is a perceptron?")
    print("Question:", result["question"])
    print("Config used:", result["chunk_size"], result["top_k"])
    print("\nAnswer:\n", result["answer"])
    print("\nClaims:")
    for c in result["claims"]:
        print(f"- [{c['status']}] {c['claim']}")