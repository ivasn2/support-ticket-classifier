import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

df = pd.read_csv("prepared_dataset.csv")

pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 1000)
pd.set_option("display.colheader_justify", "left")

# Начало модели
X = df['translated_text']
y = df['true_category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectors = TfidfVectorizer(max_features=5000, lowercase=True)

X_train_tfidf = vectors.fit_transform(X_train)

X_test_tfidf = vectors.transform(X_test)

model = LogisticRegression()

param_grid = {
    'C':[0.01, 0.1, 1, 10, 100],
    'class_weight': ['balanced']
}

grid_search = GridSearchCV (
    estimator=model,
    param_grid=param_grid,
    cv=5,
    scoring='f1_macro',
    n_jobs=-1
)

grid_search.fit(X_train_tfidf, y_train)

prediction = grid_search.predict(X_test_tfidf)

print(accuracy_score(y_test, prediction) * 100)
print(grid_search.best_params_)
print(classification_report(y_test, prediction))