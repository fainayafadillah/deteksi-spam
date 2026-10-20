"""Melatih Multinomial Naive Bayes, menghitung metrik, dan mengekspor model + analisis
ke web/data/*.json agar bisa dipakai dashboard (JavaScript) dan Streamlit."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web" / "data"
TOKEN = r"[a-z0-9]{2,}"  # harus sama dengan tokenizer di app.js dan streamlit_app.py

df = pd.read_csv(ROOT / "data" / "spam.csv").dropna()
df["label"] = df["label"].str.lower().str.strip()
y = (df["label"] == "spam").astype(int)

X_tr, X_te, y_tr, y_te = train_test_split(df["text"], y, test_size=0.2, stratify=y, random_state=42)
vec = CountVectorizer(lowercase=True, token_pattern=TOKEN)
Xtr = vec.fit_transform(X_tr)
nb = MultinomialNB(alpha=1.0).fit(Xtr, y_tr)

pred = nb.predict(vec.transform(X_te))
acc = accuracy_score(y_te, pred)
pr, rc, f1, _ = precision_recall_fscore_support(y_te, pred, average="binary", zero_division=0)
tn, fp, fn, tp = confusion_matrix(y_te, pred, labels=[0, 1]).ravel()

vocab = vec.get_feature_names_out()
lp = nb.feature_log_prob_  # baris 0 = ham, baris 1 = spam
total = np.asarray(Xtr.sum(axis=0)).ravel()
rasio = lp[1] - lp[0]
idx = [i for i in np.argsort(-rasio) if total[i] >= 3]
top_spam = [[vocab[i], round(float(rasio[i]), 2)] for i in idx[:12]]
top_ham = [[vocab[i], round(float(-rasio[i]), 2)] for i in idx[::-1][:12]]

model = {"prior": {"ham": float(nb.class_log_prior_[0]), "spam": float(nb.class_log_prior_[1])},
         "words": {w: [round(float(lp[0][i]), 4), round(float(lp[1][i]), 4)] for i, w in enumerate(vocab)}}
panjang = df.assign(n=df["text"].str.split().str.len()).groupby("label")["n"].mean()
analysis = {
    "metrik": {"akurasi": round(acc, 4), "presisi": round(pr, 4), "recall": round(rc, 4), "f1": round(f1, 4)},
    "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    "distribusi": {"spam": int((y == 1).sum()), "ham": int((y == 0).sum())},
    "rata_kata": {k: round(float(v), 1) for k, v in panjang.items()},
    "top_spam": top_spam, "top_ham": top_ham,
    "n_train": int(len(X_tr)), "n_test": int(len(X_te)), "vocab": int(len(vocab)),
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "model.json").write_text(json.dumps(model, ensure_ascii=False))
(OUT / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False))
print("Metrik:", analysis["metrik"], "| Confusion:", analysis["confusion"])
print("Kata paling spam:", [w for w, _ in top_spam[:6]])
