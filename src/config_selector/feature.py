import pandas as pd 
import re

def extract_features(question:str) -> dict:
    question = question.strip()
    words = question.split()
    word_count = len(words)

    first_word = words[0].lower().strip("?,.") if words else ""

    question_word_map = {
        "when": "when", "who": "who", "what": "what",
        "why": "why", "how": "how", "which": "which",
        "where": "where", "define": "define", "explain": "explain",
    }

    question_word = question_word_map.get(first_word, "other")
    reasoning_keywords = ["why", "how", "compare", "difference", "explain", "cause", "reason"]
    has_reasoning_keyword = int(any(kw in question.lower() for kw in reasoning_keywords))

    capitalized_word_count = len(re.findall(r"\b[A-Z][a-zA-Z]*\b", question))

    return{
        "word_count": word_count,
        "question_word": question_word,
        "has_reasoning_keyword": has_reasoning_keyword,
        "capitalized_word_count": capitalized_word_count,
    }

def featurize_dataset(csv_path : str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    feature_rows = df["question"].apply(extract_features)
    features_df = pd.DataFrame(list(feature_rows))

    result = pd.concat([df.reset_index(drop=True), features_df], axis=1)
    return result

if __name__ == "__main__":
    result = featurize_dataset("data/questions.csv")
    print(result.head())
    print("\nShape", result.shape)
    print("\nColumns", list(result.columns))
    