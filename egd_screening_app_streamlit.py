import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Apakah Saya Perlu Teropong Saluran Cerna Atas?", layout="wide")

# ---- Header ----
st.title("💡 Apakah Saya Perlu Teropong Saluran Cerna Atas?")
st.caption("Alat bantu sederhana untuk membantu Anda menilai apakah Anda mungkin memerlukan pemeriksaan teropong saluran cerna atas (endoskopi/Esofagogastroduodenoskopi - EGD). Hasil hanya bersifat informasi awal.")

# ---- Sidebar: Identitas ----
st.sidebar.header("Identitas (opsional)")
name = st.sidebar.text_input("Nama")
age = st.sidebar.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
sex = st.sidebar.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)

date_today = datetime.today().strftime("%d %b %Y")

st.markdown("---")

# ---- Layout columns ----
col1, col2, col3 = st.columns(3)

# ==============================
# 1) TANDA BAHAYA (BAHASA AWAM)
# ==============================
with col1:
    st.subheader("🚨 Tanda Bahaya")
    alarm = {
        "muntah_darah": st.checkbox("Saya pernah **muntah darah**"),
        "bab_hitam": st.checkbox("Tinja saya pernah **hitam pekat seperti aspal**"),
        "sulit_menelan": st.checkbox("Saya **semakin sulit menelan** makanan/minuman"),
        "nyeri_saat_menelan": st.checkbox("Saya **nyeri saat menelan**"),
        "bb_turun": st.checkbox("Berat badan saya **turun banyak** tanpa diet/sebab jelas"),
        "lemas_pucat_anemia": st.checkbox("Saya sering **lemas/pucat**, pernah diberi tahu darah saya **kurang (anemia)**"),
        "benjolan_perut_atas": st.checkbox("Dokter pernah bilang ada **benjolan di perut bagian atas**"),
        "kuning_nyeri": st.checkbox("Saya pernah **kulit/mata kuning** disertai **nyeri perut atas**"),
    }

# =====================================
# 2) GEJALA UMUM / TIDAK DARURAT (AWAM)
# =====================================
with col2:
    st.subheader("🩹 Keluhan Umum (Tidak Darurat)")
    non_alarm = {
        "keluhan_1_bulan": st.checkbox("Sudah **>1 bulan** sering **kembung/nyeri/begah**"),
        "panas_dada_asam": st.checkbox("Sering **panas di dada** atau **asam naik ke tenggorokan**"),
        "mual_muntah": st.checkbox("Sering **mual atau muntah berulang**"),
        "nyeri_ulu_tetap": st.checkbox("**Nyeri ulu hati** meski sudah minum obat lambung"),
        "riwayat_luka_lambung": st.checkbox("Pernah **luka di lambung**, sekarang keluhan muncul lagi"),
        "obat_nyeri_lama": st.checkbox("Sering minum **obat nyeri (NSAID)** dalam waktu lama"),
        "hpylori_positif": st.checkbox("Pernah diberi tahu ada **bakteri lambung (H. pylori)** dan masih ada keluhan"),
        "kontrol_luka": st.checkbox("Sedang **kontrol setelah pengobatan luka lambung**"),
        "keluarga_kanker_lambung": st.checkbox("Ada **keluarga dekat** pernah kena **kanker lambung**"),
    }

# ==================================
# 3) KONDISI KHUSUS / DARURAT (AWAM)
# ==================================
with col3:
    st.subheader("⚠️ Kondisi Khusus")
    khusus = {
        "perdarahan_tidak_stabil": st.checkbox("Saya **muntah darah/BAB hitam** dan **sempat sangat lemas/pingsan**"),
        "perdarahan_stabil": st.checkbox("Saya **muntah darah/BAB hitam**, tapi **tidak pingsan**"),
        "tenggorokan_tersangkut": st.checkbox("Saya merasa makanan/tulang **tersangkut di tenggorokan**"),
        "telan_benda_berbahaya": st.checkbox("Saya/anak **menelan baterai kecil** atau **benda tajam**"),
        "telan_bahan_kimia": st.checkbox("Saya **menelan cairan pembersih/kimia kuat**"),
        "riwayat_hati_kronis": st.checkbox("Saya punya **riwayat penyakit hati kronis/sirosis**"),
        "keluhan_baru_50": st.checkbox("Saya **baru mengalami keluhan lambung** setelah usia **50 tahun**"),
    }

st.markdown("---")

# ======================================
# 4) RISIKO SEDASI / KONTRAINDIKASI (AWAM)
# ======================================
st.subheader("🛑 Kondisi yang Perlu Perhatian Sebelum Tindakan")
kontra = {
    "sesak_berat": st.checkbox("Saya **sering sesak berat** atau butuh oksigen"),
    "tekanan_tidak_stabil": st.checkbox("Tekanan darah saya **sering turun/tidak stabil**"),
    "serangan_jantung_stroke_baru": st.checkbox("Saya **baru saja** kena **serangan jantung** atau **stroke**"),
    "nyeri_perut_sangat": st.checkbox("Saya **nyeri perut sangat hebat**, perut terasa **tegang/keras**"),
    "gangguan_pembekuan": st.checkbox("Saya **gangguan pembekuan darah** atau minum **pengencer darah dosis tinggi**"),
}

st.info("Catatan: Kondisi di atas perlu **penilaian dokter** dan seringkali **stabilisasi** dahulu sebelum pemeriksaan teropong.")

# ============================
# LOGIKA KEPUTUSAN (2 KATEGORI)
# ============================
trigger_segera = []

if khusus["perdarahan_tidak_stabil"]:
    trigger_segera.append("Perdarahan saluran cerna dengan kondisi sangat lemah/tidak stabil")
if khusus["perdarahan_stabil"]:
    trigger_segera.append("Perdarahan saluran cerna (stabil)")
if khusus["tenggorokan_tersangkut"]:
    trigger_segera.append("Rasa makanan/benda tersangkut di tenggorokan")
if khusus["telan_benda_berbahaya"]:
    trigger_segera.append("Menelan baterai kecil/benda tajam")
if khusus["telan_bahan_kimia"]:
    trigger_segera.append("Menelan cairan pembersih/kimia kuat")
if alarm["muntah_darah"]:
    trigger_segera.append("Muntah darah")
if alarm["bab_hitam"]:
    trigger_segera.append("BAB hitam pekat")
if alarm["sulit_menelan"]:
    trigger_segera.append("Semakin sulit menelan")
if alarm["nyeri_saat_menelan"]:
    trigger_segera.append("Nyeri saat menelan")
if alarm["bb_turun"]:
    trigger_segera.append("Penurunan berat badan banyak tanpa sebab jelas")
if alarm["lemas_pucat_anemia"]:
    trigger_segera.append("Lemas/pucat, dugaan anemia")
if alarm["benjolan_perut_atas"]:
    trigger_segera.append("Benjolan di perut atas")
if alarm["kuning_nyeri"]:
    trigger_segera.append("Kuning pada kulit/mata + nyeri perut atas")
if khusus["keluhan_baru_50"]:
    trigger_segera.append("Keluhan lambung baru pada usia ≥50 tahun")

if len(trigger_segera) > 0:
    kategori = "🔴 Anda Perlu **Segera Memeriksakan Diri** untuk Teropong Saluran Cerna Atas"
    alasan = trigger_segera
else:
    ada_keluhan = any(non_alarm.values()) or khusus["riwayat_hati_kronis"]
    if ada_keluhan:
        kategori = "🟢 Anda Dapat **Menjadwalkan Pemeriksaan Teropong Saluran Cerna Atas (Elektif)**"
        alasan = [label for key, label in {
            "keluhan_1_bulan": "Keluhan lambung/kembung/nyeri >1 bulan",
            "panas_dada_asam": "Panas di dada / asam naik",
            "mual_muntah": "Mual/muntah berulang",
            "nyeri_ulu_tetap": "Nyeri ulu hati meski minum obat",
            "riwayat_luka_lambung": "Riwayat luka lambung, keluhan muncul lagi",
            "obat_nyeri_lama": "Sering minum obat nyeri (NSAID) jangka panjang",
            "hpylori_positif": "Riwayat bakteri lambung (H. pylori) + keluhan",
            "kontrol_luka": "Kontrol setelah terapi luka lambung",
            "keluarga_kanker_lambung": "Keluarga dekat dengan kanker lambung",
            "riwayat_hati_kronis": "Riwayat penyakit hati kronis/sirosis (skrining varises)"
        }.items() if (non_alarm.get(key) if key in non_alarm else khusus.get(key))]
    else:
        kategori = "🟢 Saat ini belum tampak tanda bahaya. Anda dapat berkonsultasi dulu dengan dokter atau menjadwalkan pemeriksaan secara rutin."
        alasan = ["Tidak ditemukan tanda bahaya atau keluhan khas yang mendesak."]

st.subheader("📋 Hasil Skrining")
st.markdown(f"**{kategori}**")

with st.expander("Alasan yang terdeteksi"):
    for i, r in enumerate(alasan, 1):
        st.write(f"{i}. {r}")

with st.expander("Kondisi yang perlu perhatian sebelum tindakan"):
    risks = [label for key, label in {
        "sesak_berat": "Sering sesak berat / butuh oksigen",
        "tekanan_tidak_stabil": "Tekanan darah tidak stabil",
        "serangan_jantung_stroke_baru": "Baru kena serangan jantung / stroke",
        "nyeri_perut_sangat": "Nyeri perut sangat hebat (perut tegang/keras)",
        "gangguan_pembekuan": "Gangguan pembekuan darah / pengencer darah dosis tinggi",
    }.items() if kontra[key]]
    if risks:
        for i, r in enumerate(risks, 1):
            st.write(f"{i}. {r}")
    else:
        st.write("Tidak ada yang dipilih.")

st.markdown("---")
st.markdown("🩺 **Catatan:** Hasil ini bersifat umum dan tidak menggantikan penilaian dokter. Jika Anda memiliki keluhan berat atau mendadak, segera periksa ke unit gawat darurat atau dokter penyakit dalam.")

st.markdown("---")
st.caption("© 2025 | Aplikasi edukasi oleh dr. Danu Kamajaya – Versi Awam")
