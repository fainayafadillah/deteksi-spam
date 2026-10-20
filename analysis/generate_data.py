"""Membuat dataset SINTETIS pesan Spam/Ham berbahasa Indonesia -> data/spam.csv
Untuk hasil yang lebih realistis, ganti file data/spam.csv dengan dataset asli
(kolom: label,text; label = spam atau ham), lalu jalankan ulang train_analyze.py."""
import csv, random
from pathlib import Path

random.seed(7)
V = {
    "hadiah": ["mobil", "motor", "uang tunai 50 juta", "iPhone 15", "paket umroh"],
    "brand": ["Shopee", "Telkomsel", "Tokopedia", "Bank Dunia", "Lazada"],
    "nominal": ["Rp5 juta", "Rp10 juta", "Rp500 ribu", "Rp100 ribu", "Rp25 juta"],
    "link": ["bit.ly/klaim99", "tinyurl.com/hadiahku", "s.id/promo88", "bit.ly/cair123"],
    "bank": ["BRI", "BCA", "Mandiri", "BNI"],
    "pct": ["50", "70", "90"],
    "jam": ["09.00", "13.00", "16.30", "19.00"],
    "tempat": ["kantin", "perpustakaan", "kafe depan kampus", "rumah Rina", "lab komputer"],
    "matkul": ["basis data", "sistem operasi", "pemrograman web", "jaringan komputer"],
    "hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
    "mnt": ["5", "10", "15", "20"],
    "barang": ["telur", "gula", "sabun", "minyak goreng"],
}
SPAM = [
    "SELAMAT! Anda memenangkan {hadiah} dari {brand}. Klik {link} untuk klaim sekarang!",
    "Pinjaman online cair {nominal} tanpa jaminan, bunga rendah. Daftar di {link} sekarang juga",
    "Dapatkan bonus {nominal} gratis, deposit pertama di {link}. Promo terbatas!",
    "Nomor Anda terpilih mendapat pulsa gratis {nominal}. Hubungi {link} segera",
    "Akun {bank} Anda diblokir. Verifikasi data sekarang di {link} atau akun ditutup",
    "Diskon {pct}% hari ini saja! Belanja sekarang di {link}, stok terbatas",
    "Hadiah undian {hadiah} menanti Anda, kirim data diri ke {link} untuk klaim",
    "Kerja online dari rumah, gaji {nominal} per hari, daftar gratis di {link}",
    "Anda terpilih jadi pemenang {brand}! Segera klaim hadiah {hadiah} sebelum hangus",
    "Transfer {nominal} langsung cair ke rekening {bank} Anda, daftar gratis sekarang",
]
HAM = [
    "Besok jadi kumpul jam {jam} di {tempat} ya",
    "Tugas {matkul} dikumpulkan hari {hari}, jangan lupa ya",
    "Nanti malam mau makan di {tempat}? aku yang traktir",
    "Maaf ya aku telat, masih di jalan, sekitar {mnt} menit lagi sampai",
    "Rapat panitia dipindah ke {hari} jam {jam}, tolong konfirmasi kehadiran",
    "Makasih ya udah bantuin tugas {matkul} kemarin",
    "Ada yang punya catatan {matkul} minggu lalu? aku kemarin nggak masuk",
    "Ibu titip beli {barang} sebelum pulang ya",
    "Kantin lagi ada promo, ayo makan bareng setelah kelas {matkul}",
    "Link zoom kelas {matkul} sudah dibagikan di grup, klik aja ya",
    "Pulsa aku habis, bisa tolong isiin {nominal} nanti aku ganti?",
    "Jangan lupa transfer uang kas {nominal} ke bendahara sebelum {hari}",
]
PRE_S = ["", "INFO: ", "PROMO: ", "Halo kak, "]
PRE_H = ["", "Hai, ", "Eh, ", "Guys, "]

def bikin(templates, prefixes, n):
    hasil = set()
    while len(hasil) < n:
        isi = {k: random.choice(v) for k, v in V.items()}
        hasil.add(random.choice(prefixes) + random.choice(templates).format(**isi))
    return sorted(hasil)

rows = [("spam", t) for t in bikin(SPAM, PRE_S, 300)] + [("ham", t) for t in bikin(HAM, PRE_H, 300)]
random.shuffle(rows)
out = Path(__file__).resolve().parent.parent / "data" / "spam.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["label", "text"]); w.writerows(rows)
print(f"{len(rows)} pesan ditulis ke {out}")
