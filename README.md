# Deteksi Pesan Spam (Spam vs Ham)

Model klasifikasi teks sederhana (Multinomial Naive Bayes, bag-of-words) yang membedakan pesan
Spam dan Normal (Ham). Python melatih model dan mengekspornya ke JSON; dashboard JavaScript
menjalankan prediksi langsung di browser, jadi bisa di-hosting statis di GitHub Pages.

## Struktur
    analysis/generate_data.py   # data sintetis -> data/spam.csv
    analysis/train_analyze.py   # latih model, metrik, ekspor web/data/*.json
    web/                        # dashboard (index.html, style.css, app.js, data/)
    streamlit_app.py            # versi Streamlit
    .github/workflows/pages.yml # deploy otomatis web/ ke GitHub Pages

## Menjalankan
    pip install -r requirements.txt
    python analysis/generate_data.py
    python analysis/train_analyze.py
    cd web && python -m http.server 8000     # dashboard web
    streamlit run streamlit_app.py           # atau versi Streamlit

## Hosting
- GitHub Pages: Settings > Pages > Source = GitHub Actions, lalu push ke main.
- Streamlit Community Cloud: pilih repository ini, Main file path = streamlit_app.py.

## Desain
Aksen indigo #3730a3, merah = spam, hijau = ham, mode gelap otomatis, tanpa library eksternal.

## Catatan
Data sintetis sehingga akurasi mendekati sempurna. Ganti data/spam.csv dengan dataset asli
(mis. SMS Spam Collection) untuk hasil yang realistis.
