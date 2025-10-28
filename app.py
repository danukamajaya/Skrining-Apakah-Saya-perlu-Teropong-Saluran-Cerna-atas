# app.py — Skrining Endoskopi Saluran Cerna Atas (EGD)
# Tema RS Kariadi • Header: kiri (logo+ilustrasi), kanan (judul) • Tanpa sidebar
# © 2025 dr. Danu Kamajaya, Sp.PD – RS Kariadi Semarang

import streamlit as st
from datetime import datetime
from pathlib import Path
from io import BytesIO

# PDF (reportlab)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna Atas?",
    page_icon="🩺",
    layout="wide",
)

# ------------------ THEME & CSS ------------------
CUSTOM_CSS = """
<style>
/* Sembunyikan sidebar & tombol collapse */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Background gradasi lembut */
.stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 55%, #e6fffb 100%);
  color: #1c1c1c;
}

/* Ruang kontainer utama */
.block-container { padding-top: 12px; padding-bottom: 2rem; }

/* Judul / heading warna RS Kariadi */
h1, h2, h3 { color:#007C80; }
h1 { font-weight:800; }
h2, h3 { font-weight:700; }

/* Kolom kiri (logo + ilustrasi) */
.left-stack {
  display: flex;
  flex-direction: column;
  align-items: center;  /* agar logo & gambar center rapi */
}

/* Turunkan logo RS Kariadi */
.left-stack .logo-wrap {
  margin-top: 80px !important;    /* 👉 turun seluruh container logo */
}

.left-stack .logo-wrap img,
.left-stack [data-testid="stImage"] img {
  margin-top: 0 !important;       /* pastikan tidak bentrok dengan default */
}
.left-stack .logo-wrap img{
  margin-top: 80px;           /* 👉 menurunkan posisi logo */
}
.left-stack .illu-wrap{
  margin-top: 10px;           /* jarak antara logo & ilustrasi */
  margin-left: 30px;          /* 👉 geser ilustrasi sedikit ke kanan */
  border:1px solid #d6eceb;
  border-radius:12px;
  padding:8px;
  background:#ffffffcc;
  box-shadow:0 6px 18px rgba(0,0,0,.05);
}

/* Kolom kanan (judul & deskripsi) */
.right-title h1{
  margin-top: 40px;           /* 👉 menurunkan posisi judul */
  line-height: 1.15;
  font-size: 2.8rem;
  text-align: left;
}
.right-title p{
  font-size: 1.05rem;
  color:#333;
  margin-top: 0.8rem;
  text-align: left;
}

/* Expander */
.streamlit-expanderHeader{
  background:#f0fdfa;
  color:#007C80;
  font-weight:700;
  border:1px solid #b2dfdb;
  border-radius:10px;
}

/* Kartu hasil */
.result-card{
  border:2px solid #00B3AD22;
  border-radius:14px;
  padding:1rem 1.2rem;
  background:#ffffffcc;
  box-shadow:0 6px 18px rgba(0,0,0,.06);
}

/* Badge hasil */
.badge{ display:inline-block; padding:.35rem .65rem; border-radius:999px; font-weight:700; }
.badge-red{ background:#ffebee; color:#c62828; border:1px solid #ffcdd2; }
.badge-green{ background:#e8f5e9; color:#1b5e20; border:1px solid #c8e6c9; }
.badge-gray{ background:#eceff1; color:#37474f; border:1px solid #cfd8dc; }

/* Tombol reset */
button[kind="secondary"]{
  background:#00B3AD !important;
  color:#fff !important;
  border:none !important;
}
button[kind="secondary"]:hover{ background:#009b96 !important; }

/* Footer */
.footer-note{ color:#004d40; font-size:.9rem; }

/* Responsif HP */
@media (max-width: 640px){
  .right-title h1{ font-size:2.05rem !important; margin-top:24px; }
  .left-stack .logo-wrap img{ margin-top:20px; }
  .left-stack .illu-wrap{ margin-left:0; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ KONFIGURASI ELEMEN ------------------
# Lebar ilustrasi (atur sesuai selera: 340–520)
ILU_WIDTH = 420

# ------------------ LOAD ASSET (logo & ilustrasi) ------------------
def find_first(path_list):
    for p in path_list:
        if Path(p).exists():
            return p
    return None

logo_path = find_first(["logo_kariadi.png", "./logo_kariadi.png", "/app/logo_kariadi.png"])
egd_img_path = find_first([
    "ilustrasi_egd.png",
    "egd_illustration.png",
    "egd_image.png",
    "ChatGPT Image 28 Okt 2025, 19.10.02.png"  # jika nama file seperti contoh
])

# ------------------ HEADER ------------------
col_left, col_right = st.columns([0.36, 0.64])

with col_left:
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)  # Spacer tambahan

    # LOGO
    if logo_path:
        st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
        st.image(logo_path, width=260)  # sesuaikan lebar logo
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='font-weight:800; color:#007C80; font-size:1.4rem'>Kemenkes<br/>RS Kariadi</div>",
            unsafe_allow_html=True,
        )

    # Ilustrasi
    if egd_img_path:
        st.markdown('<div class="illu-wrap" style="margin-top:10px;">', unsafe_allow_html=True)
        st.image(egd_img_path, width=180, caption="Skema endoskopi saluran cerna atas")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(
        """
        <div class="right-title">
          <h1>Apakah Saya Perlu Teropong<br/>Saluran Cerna Atas?</h1>
          <p style="font-size:1.05rem; color:#333; margin-top:.4rem;">
            Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan
            teropong saluran cerna atas (<i>endoskopi/EGD</i>). Berdasarkan panduan klinis terbaru.
            Hasil bersifat edukasi, bukan diagnosis medis.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# (Tidak ada <hr> di sini — agar tidak muncul garis putih di bawah logo)

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

# ------------------ PDF EXPORT (sederhana) ------------------
def build_pdf(name: str, age: int, sex: str, today: str,
              verdict_text: str, advice_md: str, reasons_list: list) -> bytes:
    """Bangun PDF hasil skrining dengan KOP RSUP Dr. Kariadi (return bytes)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from pathlib import Path
    from io import BytesIO
    import re

    # helper: konversi **bold** markdown → <b>bold</b>
    def md_to_html_bold(s: str) -> str:
        # ganti **teks** menjadi <b>teks</b>
        return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

    # helper: buang emoji di awal (🔴/🟢/⚪) agar tidak jadi kotak
    def strip_leading_emoji(s: str) -> str:
        return s.lstrip("🔴🟢⚪ ").strip()

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.6*cm, bottomMargin=1.6*cm
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    title  = styles["Title"]
    italic = ParagraphStyle("i", parent=normal, italic=True)

    # cari logo RS
    logo_rs = None
    for p in ["logo_kariadi.png", "./logo_kariadi.png", "/app/logo_kariadi.png"]:
        if Path(p).exists():
            logo_rs = p
            break

    elements = []

    # KOP SURAT: logo kiri + teks tengah
    if logo_rs:
        img_rs = Image(logo_rs, width=3.2*cm, height=2*cm, hAlign='LEFT')
    else:
        img_rs = Paragraph("<b>RSUP Dr. Kariadi</b>", normal)

    kop_html = (
        "<para align='center'>"
        "<b><font size='14'>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</font></b><br/>"
        "<font size='10'>Jalan Dr. Sutomo No 16 Semarang PO BOX 1104</font><br/>"
        "<font size='10'>Telepon : (024) 8413993, 8413476, 8413764 &nbsp;&nbsp; "
        "<font color='#2e7d32'><b>Fax</b> : (024) 8318617</font></font><br/>"
        "<font size='10'>Website : http://www.rskariadi.co.id</font>"
        "</para>"
    )
    kop_text = Paragraph(kop_html, normal)

    kop_tbl = Table([[img_rs, kop_text]], colWidths=[3.8*cm, None])
    kop_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",  (0,0), (0,0), "LEFT"),
        ("ALIGN",  (1,0), (1,0), "CENTER"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    elements.append(kop_tbl)
    elements.append(Spacer(1, 4))
    elements.append(Table([[""]], colWidths=[doc.width], style=TableStyle([
        ("LINEBELOW", (0,0), (-1,-1), 1.2, colors.HexColor("#9EC9C7"))
    ])))
    elements.append(Spacer(1, 10))

    # Judul
    elements.append(Paragraph("<b>HASIL SKRINING ENDOSKOPI SALURAN CERNA ATAS (EGD)</b>", title))
    elements.append(Spacer(1, 8))

    # Identitas
    def P(txt): return Paragraph(txt, normal)
    elements += [
        P(f"<b>Tanggal:</b> {today}"),
        P(f"<b>Nama:</b> {name}") if name else None,
        P(f"<b>Usia:</b> {age} tahun"),
        P(f"<b>Jenis kelamin:</b> {sex}"),
        Spacer(1, 8),
    ]
    elements = [e for e in elements if e is not None]

    # Hasil utama
    vt = strip_leading_emoji(verdict_text)               # hilangkan emoji
    vt = md_to_html_bold(vt)                             # konversi **bold**
    adv = md_to_html_bold(advice_md).replace("\n", "<br/>")

    elements.append(P(f"<b>Kesimpulan:</b> {vt}"))
    elements.append(Spacer(1, 6))
    elements.append(P(adv))
    elements.append(Spacer(1, 8))

    # Alasan (juga konversi **bold**)
    if reasons_list:
        elements.append(P("<b>Faktor yang terdeteksi:</b>"))
        for r in reasons_list:
            elements.append(P("- " + md_to_html_bold(r)))
        elements.append(Spacer(1, 8))

    # Catatan
    elements.append(Paragraph(
        "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
        "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
        italic
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
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
