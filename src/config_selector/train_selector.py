import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from feature import featurize_dataset

features_df = featurize_dataset("data/questions.csv")
labels_df = pd.read_csv("data/labeled_questions.csv")

dataset = features_df.merge(
    labels_df[["question", "best_chunk_size", "best_top_k"]],
    on="question",
    how="inner"
)

print("Features:", len(features_df))
print("Labels:", len(labels_df))
print("Merged dataset:", len(dataset))

dataset["label"] = (
    dataset["best_chunk_size"].astype(str)
    + "_"
    + dataset["best_top_k"].astype(str)
)

dataset = pd.get_dummies(dataset, columns=["question_word"])

drop_cols = ["question", "question_type", "source_doc", "best_chunk_size", "best_top_k", "label"]
x = dataset.drop(columns=drop_cols)
y = dataset["label"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

predictions = model.predict(x_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Test accuracy: {accuracy:.2f}")

with open("data/config_selector_model.pkl", "wb") as f:
    pickle.dump({"model": model, "columns": list(x.columns)}, f)

print("Model saved.")