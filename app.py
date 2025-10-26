# app.py
# Aplikasi skrining sederhana (versi awam) apakah perlu teropong saluran cerna atas (EGD)
# Disusun berdasar ringkasan UpToDate: "Overview of upper gastrointestinal endoscopy (EGD)"
# Hasil hanya 2 kategori: PERLU SEGERA atau ELEKTIF

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

# ===================== CHECKLIST (UPTODATE, versi awam) =====================
ALARM_ITEMS = [
    "Saya muntah darah",
    "BAB saya hitam pekat seperti aspal (melena)",
    "Saya makin **sulit menelan** (disfagia progresif) atau **nyeri saat menelan** (odynofagia)",
    "Berat badan saya **turun banyak** tanpa sebab jelas",
    "Saya diberi tahu darah saya **kurang (anemia)** atau tampak sangat pucat/lemas",
    "Perut bagian atas terasa **penuh/tersumbat** (dicurigai sumbatan lambung)",
    "Kulit atau mata saya **kuning** (ikterus)",
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

# ===================== SUMMARIZE & DOWNLOAD =====================
def build_summary():
    lines = []
    lines.append(f"Ringkasan Skrining EGD – {today}")
    lines.append(f"Nama: {name or '-'} | Usia: {age} | JK: {sex}")
    lines.append("")
    lines.append(f"Hasil: {verdict}")
    lines.append("Alasan:")
    if reasons:
        for i, r in enumerate(reasons, 1):
            lines.append(f"  {i}. {r}")
    else:
        lines.append("  - (tidak ada)")
    lines.append("")
    lines.append("Catatan: Hasil ini bersifat edukasi dan tidak menggantikan penilaian dokter.")
    return "\n".join(lines)

summary_text = build_summary()
st.download_button(
    label="💾 Unduh Ringkasan (TXT)",
    data=summary_text,
    file_name=f"skrining_egd_{datetime.today().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
)

st.markdown("---")

# ===================== SUMBER ILMIAH (RINGKASAN UPTODATE) =====================
with st.expander("Sumber ilmiah (klik untuk lihat)"):
    st.markdown(
        """
**UpToDate** — *Overview of upper gastrointestinal endoscopy (esophagogastroduodenoscopy, EGD)*.  
Ringkasan yang diterapkan di aplikasi ini:
- **Alarm features / Indications for EGD**: hematemesis, melena, disfagia progresif/odynofagia, penurunan berat badan tanpa sebab, anemia defisiensi besi, massa/obstruksi, ikterus.
- **Urgent/emergent indications**: perdarahan aktif/instabilitas, menelan baterai/benda tajam/korosif, impaksi makanan.
- **Elective indications**: dispepsia/GERD menetap **>4–6 minggu** tidak membaik dengan terapi, gejala baru usia **>50 tahun**, faktor risiko seperti riwayat keluarga kanker lambung, evaluasi pasca ulkus sesuai indikasi.
*(Ringkasan ini ditulis untuk edukasi; silakan rujuk ke naskah UpToDate penuh untuk detail dan pembaruan.)*
"""
    )

# ------------------ FOOTER ------------------
st.markdown(
    "> **Catatan:** Hasil ini bersifat umum dan tidak menggantikan penilaian dokter. Bila keluhan berat atau mendadak, segera ke IGD."
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
