# app.py — Skrining Endoskopi Saluran Cerna Atas (EGD) – Tema RS Kariadi + Mobile Friendly
# © 2025 dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang
# Berdasar ringkasan: UpToDate 2025, ACG GERD 2022, PNPK Dispepsia Kemenkes 2021

import streamlit as st
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna Atas?",
    page_icon="🩺",
    layout="wide",
)

# ------------------ THEME (RS Kariadi) ------------------
CUSTOM_CSS = """
<style>
/* Background gradasi lembut */
.stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 55%, #e6fffb 100%);
  color: #1c1c1c;
}
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
h1, h2, h3 {color:#007C80;}
h1 {font-weight:800;}
h2,h3 {font-weight:700;}
/* Banner hint mobile */
.notice {
  background:#e0f2f1; border:1px solid #b2dfdb; color:#004d40;
  padding:.6rem .8rem; border-radius:10px; margin-bottom: .75rem;
  box-shadow:0 4px 14px rgba(0,0,0,.05);
}
.notice b {color:#00695c;}
/* Kartu hasil */
.result-card {
  border: 2px solid #00B3AD22; border-radius:14px; padding:1rem 1.2rem;
  background:#ffffffcc; box-shadow:0 6px 18px rgba(0,0,0,.06);
}
/* Badge hasil */
.badge {display:inline-block; padding:.35rem .65rem; border-radius:999px; font-weight:700;}
.badge-red {background:#ffebee; color:#c62828; border:1px solid #ffcdd2;}
.badge-green {background:#e8f5e9; color:#1b5e20; border:1px solid #c8e6c9;}
.badge-gray {background:#eceff1; color:#37474f; border:1px solid #cfd8dc;}
/* Expander header */
.streamlit-expanderHeader {background:#f0fdfa; color:#007C80; font-weight:700; border:1px solid #b2dfdb;}
/* Tombol reset */
button[kind="secondary"] {background:#00B3AD !important; color:#fff !important; border:none !important;}
button[kind="secondary"]:hover {background:#009b96 !important;}
/* Footer */
.footer-note {color:#004d40; font-size:.9rem;}
/* Responsive tweak untuk HP */
@media (max-width: 640px){
  .mobile-hide {display:none;}
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ HEADER + LOGO (proporsional) ------------------
col_logo, col_title = st.columns([0.25, 0.75])
with col_logo:
    st.image("logo_kariadi.png", use_container_width=True)
with col_title:
    st.markdown(
        """
        <h1 style='font-size:2.6rem; font-weight:800; color:#007C80; margin-bottom:0.25rem;'>
        Apakah Saya Perlu Teropong Saluran Cerna Atas?
        </h1>
        <p style='font-size:1.05rem; color:#333; margin-top:0.4rem;'>
        Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan 
        teropong saluran cerna atas (<i>endoskopi/EGD</i>). Berdasarkan panduan klinis terbaru. 
        Hasil bersifat edukasi, bukan diagnosis medis.
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown("<hr style='margin-top:0.2rem;margin-bottom:0.8rem;border:1px solid #cfd8dc;'/>",
            unsafe_allow_html=True)

# ------------------ SIDEBAR: identitas ------------------
st.sidebar.header("Identitas (opsional)")
sb_name = st.sidebar.text_input("Nama (opsional)", key="sb_name")
sb_age = st.sidebar.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1, key="sb_age")
sb_sex = st.sidebar.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0, key="sb_sex")

# Hint untuk HP: arahkan buka sidebar + sediakan input alternatif
st.markdown(
    """
<div class="notice">
<b>Tip:</b> Jika Anda menggunakan HP dan **sidebar tidak terlihat**, 
klik ikon **☰** di kiri atas untuk membuka sidebar. 
Atau isi data diri melalui <b>form alternatif</b> di bawah ini.
</div>
""", unsafe_allow_html=True
)

with st.expander("📄 Form Alternatif Data Diri (gunakan jika sidebar tidak terlihat)"):
    alt_name = st.text_input("Nama", value=sb_name or "")
    alt_age = st.number_input("Usia (tahun)", min_value=0, max_value=120,
                              value=int(sb_age) if sb_age is not None else 45, step=1)
    alt_sex = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"],
                           index=(["Laki-laki","Perempuan","Lainnya"].index(sb_sex)
                                  if sb_sex in ["Laki-laki","Perempuan","Lainnya"] else 0))
# Sinkronisasi ringan: gunakan sidebar jika ada, jika kosong pakai form alternatif
name = sb_name or alt_name
age = int(sb_age) if sb_name or sb_age else int(alt_age)
sex = sb_sex or alt_sex
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
risk_selected = len(risk_selected_labels) > 0
other_selected = len(other_selected_labels) > 0

if alarm_selected:
    verdict_text = "🔴 Anda **perlu endoskopi segera**"
    badge_class = "badge badge-red"
    advice = "Segera periksa ke unit gawat darurat atau **konsultasikan ke dokter Anda.**"
    reasons = alarm_selected_labels
elif risk_selected or other_selected:
    verdict_text = "🟢 Anda **dapat menjadwalkan endoskopi (elektif)**"
    badge_class = "badge badge-green"
    advice = "Buat janji melalui poliklinik atau **konsultasikan ke dokter Anda** untuk rencana pemeriksaan."
    reasons = risk_selected_labels + other_selected_labels
else:
    verdict_text = "⚪ Saat ini **belum tampak kebutuhan mendesak untuk endoskopi**"
    badge_class = "badge badge-gray"
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

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("🔒 **Privasi:** Aplikasi ini tidak menyimpan data pribadi Anda. Semua isian hanya tampil di perangkat Anda.",
            help="Tidak ada penyimpanan server.")
st.markdown(
    '<p class="footer-note"><b>Catatan:</b> Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. '
    'Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.</p>',
    unsafe_allow_html=True
)
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
