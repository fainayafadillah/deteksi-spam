"""Versi Streamlit: memakai model & hasil analisis yang sama dengan dashboard web."""
import json, math, re
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
st.set_page_config(page_title="Deteksi Pesan Spam", page_icon="📨", layout="wide")

@st.cache_data
def muat():
    d = ROOT / "web" / "data"
    return (json.loads((d / "model.json").read_text()),
            json.loads((d / "analysis.json").read_text()),
            pd.read_csv(ROOT / "data" / "spam.csv"))

def prediksi(teks, m):
    d, pakai = m["prior"]["spam"] - m["prior"]["ham"], []
    for w in re.findall(r"[a-z0-9]{2,}", teks.lower()):
        if w in m["words"]:
            h, s = m["words"][w]; d += s - h; pakai.append((w, round(s - h, 2)))
    return 1 / (1 + math.exp(-max(-30, min(30, d)))), pakai

model, ana, data = muat()
st.title("📨 Deteksi Pesan Spam")
st.caption("Multinomial Naive Bayes · data sintetis")
tab1, tab2 = st.tabs(["Deteksi", "Analisis Model"])

with tab1:
    teks = st.text_area("Tulis pesan", "SELAMAT! Anda memenangkan hadiah, klik bit.ly/klaim99 sekarang!")
    if teks.strip():
        p, pakai = prediksi(teks, model)
        (st.error if p >= .5 else st.success)("SPAM" if p >= .5 else "Normal (Ham)")
        st.progress(p, text=f"Peluang spam {p*100:.1f}%")
        if pakai:
            st.dataframe(pd.DataFrame(pakai, columns=["kata", "skor (+ spam, - ham)"])
                         .sort_values("skor (+ spam, - ham)", key=abs, ascending=False), hide_index=True)

with tab2:
    k, c = ana["metrik"], ana["confusion"]
    cols = st.columns(4)
    for col, (n, v) in zip(cols, [("Akurasi", k["akurasi"]), ("Presisi", k["presisi"]), ("Recall", k["recall"]), ("F1", k["f1"])]):
        col.metric(n, f"{v*100:.1f}%")
    st.subheader("Confusion Matrix")
    st.dataframe(pd.DataFrame([[c["tn"], c["fp"]], [c["fn"], c["tp"]]],
                 index=["Aktual Ham", "Aktual Spam"], columns=["Prediksi Ham", "Prediksi Spam"]))
    a, b = st.columns(2)
    a.subheader("Kata penciri spam"); a.bar_chart(pd.DataFrame(ana["top_spam"], columns=["kata", "skor"]).set_index("kata"))
    b.subheader("Kata penciri ham"); b.bar_chart(pd.DataFrame(ana["top_ham"], columns=["kata", "skor"]).set_index("kata"))
    st.subheader("Contoh data"); st.dataframe(data.sample(10, random_state=1), hide_index=True)
