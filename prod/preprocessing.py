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

priority_rules = {
    "Баг": {
        "Негативная": "Критический",
        "default": "Высокий"
    },
    "Документация": {
        "Негативная": "Высокий",
        "default": "Средний"
    },
    "Новая функция": {"default": "Низкий"}
}

def calculate_priority(row):
    category = row['true_category']
    sentiment = row['true_sentiment']

    category_dict = priority_rules.get(category)
    priority = category_dict.get(sentiment, category_dict.get("default"))
    return priority

df['true_priority'] = df.apply(calculate_priority, axis=1)

# 1. Фильтруем одной маской, 2. берём нужные колонки и 3. первые 10 строк
sample = df.loc[
    (df['true_category'] == 'Баг') & (df['true_sentiment'] == 'Позитивная'),
    ['translated_text', 'original_text']
].head(10)

# 4. Проходимся по строкам и печатаем читаемо
for idx, row in sample.iterrows():
    # 5. Считаем compound (обычно VADER натравливают на английский текст — поменяйте колонку, если нужно)
    compound = analyzer.polarity_scores(str(row['original_text']))['compound']

    print(f"ID: {idx} | Compound: {compound:.3f}")
    print(f"Перевод:  {row['translated_text']}")
    print(f"Оригинал: {row['original_text']}")
    print("-" * 60)

df.to_csv("prepared_dataset.csv", index=False, encoding="utf-8")

