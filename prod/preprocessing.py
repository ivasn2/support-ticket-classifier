import re
import time
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

SOURCE = "old_dataset.csv"
TARGET = "prepared_dataset.csv"
MODEL_NAME = "cointegrated/rubert-tiny-sentiment-balanced"

# ОЧИСТКА
FENCE = "`" * 3
RE_COMMENT      = re.compile(r"<!-{1,2}.*?-{1,2}!?>", re.S)
RE_COMMENT_OLD  = re.compile(r"<![^>]{0,3000}>")
RE_CODE_FENCE   = re.compile(FENCE + r".*?" + FENCE, re.S)
RE_CODE_INLINE  = re.compile(r"`[^`\n]{1,300}`")
RE_MD_IMAGE     = re.compile(r"!\[[^\]]*\]\([^)]*\)")
RE_MD_IMAGE_BAD = re.compile(r"!\[[^\]]*\]\(")
RE_MD_LINK      = re.compile(r"\[([^\]\n]{0,120})\]\([^)]*\)")
RE_MD_LINK_BAD  = re.compile(r"\[([^\]\n]{0,120})\]\(")
RE_HTML_TAG     = re.compile(r"</?[a-zA-Z][^>]{0,200}>")
RE_URL          = re.compile(r"https?://\S+|www\.\S+")
RE_PLACEHOLDER  = re.compile(r"_No response_|_Нет ответа_|\bN/A\b|Н/Д")
RE_CHECKLIST    = re.compile(r"-\s*\[[ Xx]\][^\n]{0,200}")
RE_TEMPLATE     = re.compile(r"ТЕМА:|\|\s*ОПИСАНИЕ:")
RE_DECOR        = re.compile(r"[-#*]{2,}")
RE_WS           = re.compile(r"\s+")


def clean_text(text, strip_code=True):
    """strip_code=True  -> для тональности (код = шум)
       strip_code=False -> для категории (в коде имена API = сигнал)"""
    if not isinstance(text, str):
        return ""

    # комментарии вырезаем ДО удаления дефисов, иначе '--' съедается
    text = RE_COMMENT.sub(" ", text)
    text = RE_COMMENT_OLD.sub(" ", text)

    if strip_code:
        text = RE_CODE_FENCE.sub(" ", text)
        text = RE_CODE_INLINE.sub(" ", text)

    text = RE_MD_IMAGE.sub(" ", text)
    text = RE_MD_IMAGE_BAD.sub(" ", text)
    text = RE_MD_LINK.sub(r"\1", text)
    text = RE_MD_LINK_BAD.sub(r"\1", text)

    text = RE_HTML_TAG.sub(" ", text)
    text = RE_URL.sub(" ", text)

    text = RE_PLACEHOLDER.sub(" ", text)
    text = RE_CHECKLIST.sub(" ", text)
    text = RE_TEMPLATE.sub(" ", text)

    text = RE_DECOR.sub(" ", text)
    text = text.replace("|", " ")
    text = RE_WS.sub(" ", text)
    return text.strip()


# ТОНАЛЬНОСТЬ: ruBERT
EN2RU = {"negative": "Негативная", "neutral": "Нейтральная", "positive": "Позитивная"}

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
model.eval()

# порядок меток берём из конфига, а не из карточки модели
ID2LABEL = {int(k): str(v).lower() for k, v in model.config.id2label.items()}
print("id2label:", ID2LABEL, "| device:", device)


@torch.no_grad()
def predict_sentiment(texts, batch_size=32, max_length=512):
    out = []
    t0 = time.time()
    for start in range(0, len(texts), batch_size):
        batch = [t if t else "пусто" for t in texts[start:start + batch_size]]
        enc = tokenizer(batch, padding=True, truncation=True,
                        max_length=max_length, return_tensors="pt").to(device)
        idx = model(**enc).logits.argmax(dim=-1).tolist()
        out.extend(EN2RU[ID2LABEL[i]] for i in idx)
        if (start // batch_size) % 20 == 0:
            print(f"  {start + len(batch)}/{len(texts)}  {time.time() - t0:.1f}s")
    print(f"  готово за {time.time() - t0:.1f}s")
    return out


# ТОНАЛЬНОСТЬ: VADER (для сравнения)
vader = SentimentIntensityAnalyzer()


def vader_sentiment(text):
    if not isinstance(text, str) or not text:
        return "Нейтральная"
    c = vader.polarity_scores(text)["compound"]
    if c >= 0.05:
        return "Позитивная"
    if c <= -0.05:
        return "Негативная"
    return "Нейтральная"


# ПРИОРИТЕТ
priority_rules = {
    "Баг":           {"Негативная": "Критический", "default": "Высокий"},
    "Документация":  {"Негативная": "Высокий",     "default": "Средний"},
    "Новая функция": {"default": "Низкий"},
}


def calculate_priority(category, sentiment):
    rules = priority_rules.get(category)
    if rules is None:
        raise ValueError(f"нет правила для категории: {category!r}")
    return rules.get(sentiment, rules["default"])


# ПАЙПЛАЙН
df = pd.read_csv(SOURCE)
print("загружено:", len(df), "строк из", SOURCE)

df["text_sentiment"] = df["translated_text"].apply(lambda t: clean_text(t, strip_code=True))
df["translated_text"] = df["translated_text"].apply(lambda t: clean_text(t, strip_code=False))
df["original_text"] = df["original_text"].apply(lambda t: clean_text(t, strip_code=False))

print("\nruBERT по русскому тексту:")
df["sentiment"] = predict_sentiment(df["text_sentiment"].tolist())

print("\nVADER по английскому оригиналу:")
df["sentiment_vader"] = df["original_text"].apply(vader_sentiment)

df["true_priority"] = [
    calculate_priority(c, s) for c, s in zip(df["true_category"], df["sentiment"])
]

# ПРОВЕРКИ
print("\n=== тональность ruBERT, % ===")
print((df["sentiment"].value_counts(normalize=True) * 100).round(1))
print("\n=== тональность VADER, % ===")
print((df["sentiment_vader"].value_counts(normalize=True) * 100).round(1))
print("\n=== согласны между собой, % ===")
print(round((df["sentiment"] == df["sentiment_vader"]).mean() * 100, 1))
print("\n=== категория x тональность (ruBERT) ===")
print(pd.crosstab(df["true_category"], df["sentiment"]))
print("\n=== приоритеты, % ===")
print((df["true_priority"].value_counts(normalize=True) * 100).round(1))
print("\n=== длины текста ===")
print(df[["translated_text", "text_sentiment"]].apply(lambda s: s.str.len().mean()).round(0))

df.to_csv(TARGET, index=False, encoding="utf-8")
print("\nсохранено:", TARGET, "| колонки:", df.columns.tolist())