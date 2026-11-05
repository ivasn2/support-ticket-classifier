import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Очистка текста
def clean_text(text):
    if not isinstance(text, str):
        return text

    url = r"https?://\S+|www\.\S+"

    text = re.sub(url, "", text)

    text = re.sub(r"[\r\n]+", " ", text)

    text = re.sub(r"[-#]{2,}", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def compound_sentiment(text):
    compound = analyzer.polarity_scores(text)['compound']
    if compound >= 0.05:
        return "Позитивная"
    elif compound <= -0.05:
        return "Негативная"
    else:
        return "Нейтральная"

df = pd.read_json("../Old/dataset_for_classification.json")
df['translated_text'] = df['translated_text'].str.replace("ТЕМА: ", "")
df['translated_text'] = df['translated_text'].str.replace(r"| ОПИСАНИЕ: ", "", regex=False)
df['translated_text'] = df['translated_text'].str.replace("|", " ")
df['translated_text'] = df['translated_text'].apply(clean_text)

df['original_text'] = df['original_text'].str.replace("ТЕМА: ", "")
df['original_text'] = df['original_text'].str.replace(r"| ОПИСАНИЕ: ", "", regex=False)
df['original_text'] = df['original_text'].str.replace("|", " ")
df['original_text'] = df['original_text'].apply(clean_text)

analyzer = SentimentIntensityAnalyzer()
df['true_sentiment'] = df['original_text'].apply(compound_sentiment)

df = df.drop(columns=['original_text'])

df.to_csv("prepared_dataset.csv", index=False, encoding="utf-8")

