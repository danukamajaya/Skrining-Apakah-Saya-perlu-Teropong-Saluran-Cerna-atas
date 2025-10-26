# app.py — Skrining EGD (versi awam, 2 kategori)
# Disederhanakan sesuai masukan: tanpa unduhan ringkasan & tanpa bagian sumber ilmiah.
# "Kuning (ikterus)" TIDAK lagi termasuk Tanda Bahaya.

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
    "teropong saluran cerna atas (endoskopi/EGD). Hasil ini bersifat edukasi."
)

# ------------------ SIDEBAR IDENTITAS ------------------
st.sidebar.header("Identitas (opsional)")
name = st.sidebar.text_input("Nama")
age = st.sidebar.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
sex = st.sidebar.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")

st.markdown("---")

# ===================== CHECKLIST (versi awam, disederhanakan) =====================
ALARM_ITEMS = [
    "Saya muntah darah",
    "BAB saya hitam pekat seperti aspal (melena)",
    "Saya makin **sulit menelan** (disfagia progresif) atau **nyeri saat menelan** (odynofagia)",
    "Berat badan saya **turun banyak** tanpa sebab jelas",
    "Saya diberi tahu darah saya **kurang (anemia)** atau tampak sangat pucat/lemas",
    "Perut bagian atas terasa **penuh/tersumbat** (dicurigai sumbatan lambung)",
    # Catatan: "kuning/ikterus" dihapus dari alarm items sesuai permintaan
]

NON_URGENT_ITEMS = [
    "Keluhan perut atas/nyeri ulu hati/panas di dada **>6 minggu** dan belum membaik dengan obat",
    "Saya sering **mual** atau **muntah berulang**",
    "Sering terasa **asam/panas naik ke tenggorokan** (refluks/GERD) **dan tidak membaik** dengan obat",
    "**Nyeri ulu hati** tetap ada meskipun sudah minum obat lambung",
    "Saya pernah diberi tahu ada **tukak/ulkus lambung/duodenum** dan keluhan masih berlanjut",
    "Ada **keluarga dekat** pernah kena **kanker lambung**",
    "Saya **baru muncul keluhan** ini setelah usia **50 tahun**",
]

SPECIAL_CASE_ITEMS = [
    "Saya/anak **menelan baterai kecil** atau **benda tajam**",
    "Saya **menelan cairan pembersih/kimia (zat korosif)**",
    "Saya merasa makanan/tulang **tersangkut di tenggorokan** (sulit menelan total/impaksi makanan)",
    "Saya punya **penyakit hati kronis/sirosis** (perlu skrining varises esofagus—sesuai penilaian dokter)",
]

# ------------------ LAYOUT 3 KOLOM ------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🚨 Tanda Bahaya")
    alarm_selected_labels = []
    for i, label in enumerate(ALARM_ITEMS):
        if st.checkbox(label, key=f"alarm_{i}"):
            alarm_selected_labels.append(label)

with c2:
    st.subheader("🩹 Keluhan Umum (Tidak Darurat)")
    nonurgent_selected_labels = []
    for i, label in enumerate(NON_URGENT_ITEMS):
        if st.checkbox(label, key=f"nonurgent_{i}"):
            nonurgent_selected_labels.append(label)

with c3:
    st.subheader("⚠️ Kondisi Khusus")
    special_selected_labels = []
    for i, label in enumerate(SPECIAL_CASE_ITEMS):
        if st.checkbox(label, key=f"special_{i}"):
            special_selected_labels.append(label)

st.markdown("---")

# ===================== PENILAIAN HASIL (2 kategori) =====================
alarm_selected = len(alarm_selected_labels) > 0
special_selected = len(special_selected_labels) > 0
nonurgent_selected = len(nonurgent_selected_labels) > 0

if alarm_selected or special_selected:
    verdict = "🔴 Anda **perlu endoskopi segera**"
    advice = "Segera ke unit gawat darurat atau layanan endoskopi terdekat."
    reasons = alarm_selected_labels + special_selected_labels
elif nonurgent_selected:
    verdict = "🟢 Anda dapat **menjadwalkan endoskopi (elektif)**"
    advice = "Buat janji melalui poliklinik/rujukan sesuai ketersediaan."
    reasons = nonurgent_selected_labels
else:
    verdict = "⚪ Saat ini **belum tampak kebutuhan endoskopi**"
    advice = "Pertimbangkan terapi empiris & edukasi; konsultasikan bila keluhan berlanjut."
    reasons = []

st.subheader("📋 Hasil Skrining")
st.markdown(f"**{verdict}**")
st.write(advice)

with st.expander("Alasan yang terdeteksi"):
    if reasons:
        for i, r in enumerate(reasons, 1):
            st.write(f"{i}. {r}")
    else:
        st.write("Tidak ada pilihan yang tercentang.")

st.markdown("---")

# ------------------ FOOTER ------------------
st.markdown(
    "> **Catatan:** Hasil ini bersifat umum dan tidak menggantikan penilaian dokter. Bila keluhan berat atau mendadak, segera ke IGD."
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
