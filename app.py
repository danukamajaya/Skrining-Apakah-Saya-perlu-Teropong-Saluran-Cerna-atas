# app.py — Skrining Endoskopi Saluran Cerna Atas (EGD) – Versi Edukasi Lengkap
# Berdasarkan UpToDate 2025, ACG GERD Guideline 2022, PNPK Dispepsia Kemenkes 2021
# © 2025 dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang

import streamlit as st
from datetime import datetime

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna Atas?",
    layout="wide",
)

# ------------------ HEADER ------------------
st.title("💡 Apakah Saya Perlu Teropong Saluran Cerna Atas?")
st.caption(
    "Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan "
    "teropong saluran cerna atas (endoskopi/EGD). Berdasarkan panduan klinis terbaru. "
    "Hasil bersifat edukasi, bukan diagnosis medis."
)

# ------------------ SIDEBAR IDENTITAS ------------------
st.sidebar.header("Identitas (opsional)")
name = st.sidebar.text_input("Nama")
age = st.sidebar.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
sex = st.sidebar.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")

st.markdown("---")

# ===================== DAFTAR CEKLIS =====================
ALARM_ITEMS = [
    "Saya **muntah darah** (hematemesis)",
    "BAB saya **hitam pekat seperti aspal** (melena)",
    "Saya makin **sulit menelan** (disfagia progresif)",
    "Saya **nyeri saat menelan** (odynofagia)",
    "Berat badan saya **turun banyak tanpa sebab jelas**",
    "Saya diberi tahu darah saya **kurang (anemia)** atau saya tampak pucat/lemas",
    "Saya **sering muntah berulang atau tidak bisa makan/minum**",
    "Perut bagian atas terasa **penuh / cepat kenyang / tersumbat** (curiga sumbatan lambung)",
]

RISK_ITEMS = [
    "Saya **baru mengalami keluhan lambung/dispepsia setelah usia 50 tahun**",
    "Ada **keluarga dekat** yang pernah terkena **kanker lambung**",
]

OTHER_INDICATIONS = [
    "Keluhan perut atas/nyeri ulu hati/panas di dada **>4–6 minggu** dan belum membaik dengan obat",
    "**Nyeri ulu hati** tetap ada meskipun sudah minum obat lambung (PPI 4–8 minggu)",
    "Sering **asam/panas naik ke tenggorokan (refluks/GERD)** dan **tidak membaik** dengan obat",
    "Riwayat **tukak/ulkus lambung atau duodenum**, keluhan masih berlanjut",
    "Riwayat **infeksi H. pylori** dan masih ada keluhan setelah pengobatan",
    "Saya sering memakai **obat nyeri (NSAID)/pengencer darah** dan ada keluhan perut",
    "Dugaan **perdarahan samar** (feses tes darah positif) tanpa penyebab jelas",
    "Saya punya **penyakit hati kronis/sirosis** (skrining varises esofagus sesuai penilaian dokter)",
    "**Kontrol endoskopi** pasca pengobatan ulkus/varises/polipektomi (sesuai anjuran dokter)",
]

# ------------------ TOMBOL RESET ------------------
def reset_all():
    for key in list(st.session_state.keys()):
        if key.startswith(("alarm_", "risk_", "other_")):
            st.session_state[key] = False
    st.rerun()

col_reset = st.columns([1,1,1,1,1,1,1,1,1,1,1])[10]
with col_reset:
    st.button("↺ Reset semua jawaban", on_click=reset_all)

# ------------------ LAYOUT CEKLIS ------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🚨 Tanda Bahaya (Alarm)")
    st.markdown("Jika salah satu di bawah ini ada, endoskopi biasanya **dianjurkan segera**.")
    alarm_selected_labels = []
    for i, label in enumerate(ALARM_ITEMS):
        if st.checkbox(label, key=f"alarm_{i}"):
            alarm_selected_labels.append(label)

with c2:
    st.subheader("⚠️ Faktor Risiko Tambahan")
    st.markdown("Bukan darurat, namun **perlu dipertimbangkan** untuk evaluasi.")
    risk_selected_labels = []
    for i, label in enumerate(RISK_ITEMS):
        if st.checkbox(label, key=f"risk_{i}"):
            risk_selected_labels.append(label)

with c3:
    st.subheader("🩹 Indikasi Lain (Bukan Alarm)")
    st.markdown("Tidak darurat; pertimbangkan **endoskopi elektif** bila keluhan menetap.")
    other_selected_labels = []
    for i, label in enumerate(OTHER_INDICATIONS):
        if st.checkbox(label, key=f"other_{i}"):
            other_selected_labels.append(label)

st.markdown("---")

# ===================== PENILAIAN HASIL =====================
alarm_selected = len(alarm_selected_labels) > 0
risk_selected = len(risk_selected_labels) > 0
other_selected = len(other_selected_labels) > 0

if alarm_selected:
    verdict = "🔴 Anda **perlu endoskopi segera**"
    advice = "Segera periksa ke unit gawat darurat atau **konsultasikan ke dokter Anda.**"
    reasons = alarm_selected_labels
elif risk_selected or other_selected:
    verdict = "🟢 Anda **dapat menjadwalkan endoskopi (elektif)**"
    advice = "Buat janji melalui poliklinik atau **konsultasikan ke dokter Anda** untuk rencana pemeriksaan."
    reasons = risk_selected_labels + other_selected_labels
else:
    verdict = "⚪ Saat ini **belum tampak kebutuhan mendesak untuk endoskopi**"
    advice = """
🌿 **Langkah-langkah yang dapat Anda lakukan untuk menjaga kesehatan lambung dan mencegah kekambuhan:**

### 🥗 1️⃣ Atur Pola Makan
- Makan dalam porsi kecil tetapi sering (4–5 kali per hari)
- Hindari makan terburu-buru, kunyah makanan dengan baik
- Jangan langsung berbaring minimal **2–3 jam setelah makan**
- Kurangi makanan berlemak, pedas, asam, cokelat, kopi, teh kental, minuman bersoda, dan alkohol
- Pilih buah dan sayur rendah asam seperti pisang, pepaya, semangka, melon, labu, dan brokoli
- Minum air putih cukup setiap hari

### 💊 2️⃣ Hati-hati terhadap Penggunaan Obat
- Hindari minum **obat nyeri (NSAID seperti ibuprofen, asam mefenamat, piroksikam)** tanpa petunjuk dokter
- Jika harus menggunakannya, konsultasikan agar dokter memberikan **pelindung lambung (misalnya PPI)**
- Hindari merokok dan minuman beralkohol

### ⚖️ 3️⃣ Perbaiki Gaya Hidup
- **Tidur dengan kepala sedikit lebih tinggi** (10–20 cm) untuk mencegah asam naik ke tenggorokan
- Hindari pakaian atau ikat pinggang yang terlalu ketat di perut
- Pertahankan **berat badan ideal**, karena berat badan berlebih meningkatkan tekanan di lambung
- Kelola stres, karena stres dapat memperburuk gejala lambung

### 🏃‍♂️ 4️⃣ Lakukan Olahraga yang Tepat
- Pilih olahraga **ringan hingga sedang**: jalan kaki cepat, bersepeda santai, yoga, peregangan, atau berenang ringan
- Lakukan **30–45 menit per hari, minimal 5 hari per minggu**
- Hindari olahraga berat (angkat beban, sit-up, plank) atau aktivitas menunduk lama **segera setelah makan**
- Tunggu minimal **2 jam setelah makan** sebelum berolahraga

### ⏱️ 5️⃣ Evaluasi dan Pemeriksaan Lanjutan
- Jika keluhan tidak membaik setelah **4–6 minggu** melakukan perubahan pola hidup dan pengobatan lambung, konsultasikan kembali ke dokter Anda
- Dokter dapat menyarankan pemeriksaan **bakteri *H. pylori*** atau tindakan lain sebelum endoskopi
- Bila muncul **tanda bahaya baru** seperti muntah darah, BAB hitam, berat badan turun, atau anemia, segera periksa ke **dokter penyakit dalam**

💬 Dengan pola hidup sehat dan pengobatan terarah, sebagian besar keluhan lambung dapat membaik tanpa perlu tindakan endoskopi segera.
"""
    reasons = []

# ------------------ OUTPUT ------------------
st.subheader("📋 Hasil Skrining")
st.markdown(f"**{verdict}**")
st.write(advice)

with st.expander("Alasan yang terdeteksi"):
    if reasons:
        for i, r in enumerate(reasons, 1):
            st.write(f"{i}. {r}")
    else:
        st.write("Tidak ada pilihan yang tercentang.")

# ------------------ INFORMASI & FOOTER ------------------
st.markdown("---")
st.markdown("🔒 **Privasi:** Aplikasi ini tidak menyimpan data pribadi Anda. Semua isian hanya tampil di perangkat Anda.")
st.markdown(
    "> **Catatan:** Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
    "Jika Anda memiliki keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam."
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
