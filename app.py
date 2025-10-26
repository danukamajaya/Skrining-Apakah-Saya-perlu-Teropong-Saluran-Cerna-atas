# app.py — Skrining EGD berbasis Alarm Symptoms Valid (UpToDate & ACG 2022)
# Danu Kamajaya, Sp.PD (K)GEH – RSUP Dr. Kariadi Semarang – 2025

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna Atas?",
    layout="wide",
)

st.title("💡 Apakah Saya Perlu Teropong Saluran Cerna Atas?")
st.caption(
    "Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan "
    "teropong saluran cerna atas (endoskopi/EGD). Berdasarkan panduan UpToDate & ACG 2022. "
    "Hasil ini bersifat edukasi, bukan diagnosis medis."
)

st.sidebar.header("Identitas (opsional)")
name = st.sidebar.text_input("Nama")
age = st.sidebar.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
sex = st.sidebar.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")

st.markdown("---")

# ------------------ CHECKLIST ------------------
st.subheader("🚨 Tanda Bahaya (Alarm Symptoms)")

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

st.markdown(
    "Jika Anda mengalami salah satu dari tanda di bawah ini, pemeriksaan endoskopi biasanya "
    "dianjurkan **segera** untuk mencari penyebab yang lebih serius."
)

alarm_selected_labels = []
for i, label in enumerate(ALARM_ITEMS):
    if st.checkbox(label, key=f"alarm_{i}"):
        alarm_selected_labels.append(label)

st.markdown("---")

# ------------------ FAKTOR RISIKO TAMBAHAN ------------------
st.subheader("⚠️ Faktor Risiko Tambahan (Bukan Darurat, tapi Perlu Diperiksa)")
NON_URGENT_ITEMS = [
    "Saya **baru mengalami keluhan lambung/dispepsia setelah usia 50 tahun**",
    "Ada **keluarga dekat** yang pernah terkena **kanker lambung**",
]
nonurgent_selected_labels = []
for i, label in enumerate(NON_URGENT_ITEMS):
    if st.checkbox(label, key=f"risk_{i}"):
        nonurgent_selected_labels.append(label)

st.markdown("---")

# ------------------ PENILAIAN HASIL ------------------
alarm_selected = len(alarm_selected_labels) > 0
nonurgent_selected = len(nonurgent_selected_labels) > 0

if alarm_selected:
    verdict = "🔴 Anda **perlu endoskopi**"
    # ✅ Bahasa disesuaikan lebih aman dan empatik
    advice = "Segera periksa ke unit gawat darurat atau **konsultasikan ke dokter Anda**."
    reasons = alarm_selected_labels
elif nonurgent_selected:
    verdict = "🟢 Anda **dapat menjadwalkan endoskopi (elektif)**"
    advice = "Buat janji melalui poliklinik atau **konsultasikan ke dokter Anda** untuk rencana pemeriksaan."
    reasons = nonurgent_selected_labels
else:
    verdict = "⚪ Saat ini **belum tampak kebutuhan mendesak untuk endoskopi**"
    advice = "Pertimbangkan terapi empiris, ubah pola makan, dan konsultasikan bila keluhan berlanjut."
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
    "> **Catatan:** Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
    "Jika Anda memiliki keluhan berat, mendadak, atau terus-menerus, segera konsultasikan ke dokter penyakit dalam."
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
