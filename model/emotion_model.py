import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load the training data
def load_data(filepath):
    data = pd.read_csv(filepath, sep=';', names=["text", "emotion"])
    return data

# Train the model
def train_model():
    data = load_data("model/train.txt")
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data["text"])
    y = data["emotion"]

    model = MultinomialNB()
    model.fit(X, y)

    # Save model and vectorizer
    joblib.dump(model, "model/emotion_model.pkl")
    joblib.dump(vectorizer, "model/vectorizer.pkl")
    print("Model trained and saved!")

# Run this script directly to train
if __name__ == "__main__":
    train_model()
