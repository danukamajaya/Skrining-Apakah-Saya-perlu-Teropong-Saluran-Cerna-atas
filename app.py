# app.py — Skrining Endoskopi Saluran Cerna Atas (EGD)
# Tema RS Kariadi • Tanpa Sidebar • Ilustrasi kanan-atas • Export PDF
# © 2025 dr. Danu Kamajaya, Sp.PD – RS Kariadi Semarang

import streamlit as st
from datetime import datetime
from pathlib import Path
from io import BytesIO

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna Atas?",
    page_icon="🩺",
    layout="wide",
)

# ------------------ THEME (RS Kariadi) ------------------
CUSTOM_CSS = """
<style>
/* Sembunyikan sidebar & tombol collapse (walau layout=wide) */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Background gradasi lembut */
.stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 55%, #e6fffb 100%);
  color: #1c1c1c;
}

/* Kontainer utama turun sedikit agar header tidak nempel tepi */
.block-container { padding-top: 14px; padding-bottom: 2rem; }

h1, h2, h3 { color:#007C80; }
h1 { font-weight:800; }
h2, h3 { font-weight:700; }

.header-wrap { padding: 6px 0 4px 0; }

/* Expander header (data dasar + alasan) */
.streamlit-expanderHeader {
  background:#f0fdfa; color:#007C80; font-weight:700; border:1px solid #b2dfdb;
  border-radius:10px;
}

/* Kartu hasil */
.result-card {
  border:2px solid #00B3AD22; border-radius:14px; padding:1rem 1.2rem;
  background:#ffffffcc; box-shadow:0 6px 18px rgba(0,0,0,.06);
}

/* Badge hasil */
.badge { display:inline-block; padding:.35rem .65rem; border-radius:999px; font-weight:700; }
.badge-red  { background:#ffebee; color:#c62828; border:1px solid #ffcdd2; }
.badge-green{ background:#e8f5e9; color:#1b5e20; border:1px solid #c8e6c9; }
.badge-gray { background:#eceff1; color:#37474f; border:1px solid #cfd8dc; }

/* Tombol reset */
button[kind="secondary"] { background:#00B3AD !important; color:#fff !important; border:none !important; }
button[kind="secondary"]:hover { background:#009b96 !important; }

/* Footer */
.footer-note { color:#004d40; font-size:.9rem; }

/* Ilustrasi kanan: bingkai lembut */
.illustration-wrap {
  border:1px solid #d6eceb; border-radius:12px; padding:6px; background:#ffffffcc;
  box-shadow:0 6px 18px rgba(0,0,0,.05);
}

/* Responsif HP */
@media (max-width: 640px){
  .title-text h1 { font-size:2.05rem !important; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ HEADER: logo + judul + ilustrasi ------------------
# Robus load logo
logo = None
for p in ["logo_kariadi.png", "./logo_kariadi.png", "/app/logo_kariadi.png"]:
    if Path(p).exists():
        logo = p
        break

# Robus load ilustrasi EGD
egd_img = None
for p in ["ilustrasi_egd.png", "egd_illustration.png", "egd_image.png"]:
    if Path(p).exists():
        egd_img = p
        break

# 3 kolom: logo | judul | ilustrasi
col_logo, col_title, col_pic = st.columns([0.20, 0.55, 0.25])

with col_logo:
    # turunkan logo sedikit via spacer agar tidak nempel
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    if logo:
        st.image(logo, use_container_width=True)
    else:
        st.markdown(
            "<div style='font-weight:800; color:#007C80; font-size:1.4rem;'>Kemenkes<br/>RS Kariadi</div>",
            unsafe_allow_html=True
        )

with col_title:
    st.markdown(
        """
        <div class="title-text">
          <h1 style='font-size:2.6rem; font-weight:800; color:#007C80; margin-top:25px; margin-bottom:0.25rem;'>
            Apakah Saya Perlu Teropong Saluran Cerna Atas?
          </h1>
          <p style='font-size:1.05rem; color:#333; margin-top:0.4rem;'>
            Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan
            teropong saluran cerna atas (<i>endoskopi/EGD</i>). Berdasarkan panduan klinis terbaru.
            Hasil bersifat edukasi, bukan diagnosis medis.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_pic:
    if egd_img:
        st.markdown("<div class='illustration-wrap'>", unsafe_allow_html=True)
        st.image(egd_img, use_container_width=True, caption="Skema endoskopi saluran cerna atas")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top:0.2rem;margin-bottom:0.8rem;border:1px solid #cfd8dc;'/>",
            unsafe_allow_html=True)

# ------------------ DATA DASAR (opsional) ------------------
with st.expander("🧑‍⚕️ Data dasar (opsional)", expanded=False):
    name = st.text_input("Nama")
    age  = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
    sex  = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)

today = datetime.today().strftime("%d %b %Y")

st.markdown("---")

# ------------------ DAFTAR CEKLIS ------------------
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

st.button("↺ Reset semua jawaban", on_click=reset_all, type="secondary")

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

# ------------------ PENILAIAN HASIL ------------------
alarm_selected = len(alarm_selected_labels) > 0
risk_selected  = len(risk_selected_labels)  > 0
other_selected = len(other_selected_labels) > 0

if alarm_selected:
    verdict_text = "🔴 Anda **perlu endoskopi segera**"
    badge_class  = "badge badge-red"
    advice = "Segera periksa ke unit gawat darurat atau **konsultasikan ke dokter Anda.**"
    reasons = alarm_selected_labels
elif risk_selected or other_selected:
    verdict_text = "🟢 Anda **dapat menjadwalkan endoskopi (elektif)**"
    badge_class  = "badge badge-green"
    advice = "Buat janji melalui poliklinik atau **konsultasikan ke dokter Anda** untuk rencana pemeriksaan."
    reasons = risk_selected_labels + other_selected_labels
else:
    verdict_text = "⚪ Saat ini **belum tampak kebutuhan mendesak untuk endoskopi**"
    badge_class  = "badge badge-gray"
    advice = """
🌿 **Langkah-langkah yang dapat Anda lakukan untuk menjaga kesehatan lambung dan mencegah kekambuhan:**

### 🥗 1️⃣ Atur Pola Makan
- Makan dalam porsi kecil tetapi sering (4–5 kali per hari)
- Hindari makan terburu-buru, kunyah makanan dengan baik
- Jangan langsung berbaring minimal **2–3 jam setelah makan**
- Kurangi makanan berlemak, pedas, asam, cokelat, kopi, teh kental, minuman bersoda, dan alkohol
- Pilih buah & sayur rendah asam (pisang, pepaya, melon/semangka, labu, brokoli)
- Minum air putih cukup setiap hari

### 💊 2️⃣ Hati-hati terhadap Penggunaan Obat
- Hindari **NSAID** (ibuprofen, asam mefenamat, piroksikam) tanpa petunjuk dokter
- Jika harus, minta dokter mempertimbangkan **pelindung lambung (mis. PPI)**
- Hindari merokok dan alkohol

### ⚖️ 3️⃣ Perbaiki Gaya Hidup
- **Tidur dengan kepala sedikit lebih tinggi** (10–20 cm)
- Hindari pakaian/ikat pinggang terlalu ketat
- Pertahankan **berat badan ideal**
- Kelola stres, istirahat cukup

### 🏃‍♂️ 4️⃣ Olahraga yang Tepat
- Pilih olahraga **ringan–sedang**: jalan kaki cepat, bersepeda santai, yoga/peregangan, atau berenang ringan
- Durasi **30–45 menit**, **≥5 hari/minggu**
- Hindari olahraga berat/menunduk lama **segera setelah makan**; tunggu **≥2 jam** setelah makan

### ⏱️ 5️⃣ Evaluasi Lanjutan
- Bila tidak membaik setelah **4–6 minggu**, konsultasikan kembali ke dokter Anda
- Dokter mungkin menyarankan pemeriksaan **H. pylori** atau lainnya sebelum endoskopi
- Jika muncul **tanda bahaya** (muntah darah, BAB hitam, berat turun, anemia), segera periksa ke **dokter penyakit dalam**
"""
    reasons = []

# ------------------ OUTPUT ------------------
st.subheader("📋 Hasil Skrining")
st.markdown(
    f'<div class="result-card"><span class="{badge_class}">{verdict_text}</span><br/>{advice}</div>',
    unsafe_allow_html=True
)

with st.expander("Alasan yang terdeteksi"):
    if reasons:
        for i, r in enumerate(reasons, 1):
            st.write(f"{i}. {r}")
    else:
        st.write("Tidak ada pilihan yang tercentang.")

# ------------------ PDF EXPORT ------------------
def build_pdf(name: str, age: int, sex: str, today: str,
              verdict_text: str, advice_md: str, reasons_list: list) -> bytes:
    """Membangun PDF hasil skrining (return bytes)."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Judul
    elements.append(Paragraph("<b>Hasil Skrining Endoskopi Saluran Cerna Atas (EGD)</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Identitas
    elements.append(Paragraph(f"<b>Tanggal:</b> {today}", styles["Normal"]))
    if name:
        elements.append(Paragraph(f"<b>Nama:</b> {name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Usia:</b> {age} tahun", styles["Normal"]))
    elements.append(Paragraph(f"<b>Jenis kelamin:</b> {sex}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Hasil utama
    elements.append(Paragraph(f"<b>Kesimpulan:</b> {verdict_text}", styles["Normal"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(advice_md.replace("\n", "<br/>"), styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Alasan
    if reasons_list:
        elements.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Normal"]))
        for r in reasons_list:
            elements.append(Paragraph(f"- {r}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Catatan
    elements.append(Paragraph(
        "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
        "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
        styles["Italic"]
    ))

    doc.build(elements)
    return buffer.getvalue()

pdf_bytes = build_pdf(name or "", int(age), sex, today, verdict_text, advice, reasons)

st.download_button(
    label="⬇️ Unduh Hasil Skrining (PDF)",
    data=pdf_bytes,
    file_name=f"Hasil_Skrining_EGD_{today.replace(' ', '_')}.pdf",
    mime="application/pdf",
)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    "🔒 **Privasi:** Aplikasi ini tidak menyimpan data pribadi Anda. Semua isian hanya tampil di perangkat Anda.",
    help="Tidak ada penyimpanan server."
)
st.markdown(
    '<p class="footer-note"><b>Catatan:</b> Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. '
    'Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.</p>',
    unsafe_allow_html=True
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RS Kariadi Semarang – Versi Awam")
