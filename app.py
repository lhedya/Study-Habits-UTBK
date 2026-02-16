"""
UTBK Study Recommendation System
Main Streamlit Application - FIXED VERSION
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Import custom modules
from utils.preprocessing import (
    load_mappings, encode_survey_responses, 
    calculate_dimension_scores, calculate_gap_analysis
)
from utils.model_utils import (
    load_models, load_learner_type_descriptions,
    predict_learner_type
)
from utils.recommendations import (
    generate_study_plan, generate_milestones
)

# Page configuration
st.set_page_config(
    page_title="UTBK Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .learner-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #E63946;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'profile'
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}
if 'survey_responses' not in st.session_state:
    st.session_state.survey_responses = {}

# Load models and mappings (cached)
@st.cache_resource
def load_app_models():
    return load_models()

@st.cache_resource
def load_app_mappings():
    return load_mappings()

@st.cache_resource
def load_learner_descriptions():
    return load_learner_type_descriptions()

# ================================================================
# SURVEY QUESTIONS - ALL 52 QUESTIONS COMPLETE
# ================================================================

def get_survey_questions():
    """Return all 52 survey questions with options"""
    
    questions = {}
    
    # Q1-Q12: Gaya Belajar & Preferensi Kognitif
    questions['Q1'] = {
        'question': 'Saya lebih mudah memahami materi UTBK dengan cara:',
        'options': [
            'Membaca dan melihat diagram/grafik',
            'Mendengarkan penjelasan guru/video',
            'Praktik langsung mengerjakan soal',
            'Diskusi dengan teman'
        ]
    }
    
    questions['Q2'] = {
        'question': 'Metode mencatat yang paling saya sukai adalah:',
        'options': [
            'Mind mapping dengan warna-warna',
            'Catatan linear terstruktur dengan numbering',
            'Digital notes (Google Docs, Notion, dll)',
            'Tulis tangan dengan stabilo highlight'
        ]
    }
    
    questions['Q3'] = {
        'question': 'Waktu paling produktif saya untuk belajar adalah:',
        'options': [
            'Pagi (05.00-09.00)',
            'Siang (09.00-15.00)',
            'Sore (15.00-19.00)',
            'Malam (19.00-23.00)',
            'Tengah malam (23.00-05.00)'
        ]
    }
    
    questions['Q4'] = {
        'question': 'Saya lebih mudah memahami konsep jika diberikan:',
        'options': [
            'Contoh soal konkret dan aplikasi nyata',
            'Teori dan penjelasan konsep mendalam',
            'Formula dan rumus praktis',
            'Analogi dan perumpamaan'
        ]
    }
    
    questions['Q5'] = {
        'question': 'Dalam belajar, saya lebih suka:',
        'options': [
            'Belajar sendiri di ruangan tenang',
            'Belajar kelompok dengan teman',
            'Belajar sendiri tapi kadang diskusi',
            'Belajar di tempat ramai (cafe, perpustakaan)'
        ]
    }
    
    questions['Q6'] = {
        'question': 'Media belajar yang paling efektif untuk saya:',
        'options': [
            'Video pembelajaran YouTube/platform online',
            'Buku dan modul cetak',
            'Aplikasi mobile dan e-learning',
            'Les privat/kelompok tatap muka'
        ]
    }
    
    questions['Q7'] = {
        'question': 'Durasi maksimal saya dapat fokus belajar tanpa break:',
        'options': [
            'Kurang dari 30 menit',
            '30-45 menit',
            '45-60 menit',
            '60-90 menit',
            'Lebih dari 90 menit'
        ]
    }
    
    questions['Q8'] = {
        'question': 'Saya lebih fokus belajar dengan suasana:',
        'options': [
            'Hening total, tanpa suara apapun',
            'Musik instrumental/lo-fi',
            'Suara alam (hujan, ombak)',
            'Tidak masalah ada kebisingan'
        ]
    }
    
    questions['Q9'] = {
        'question': 'Materi UTBK yang paling saya sukai:',
        'options': [
            'Yang ada hitungan (Matematika, Fisika)',
            'Yang ada teori dan hafalan (Biologi, Sejarah)',
            'Yang ada analisis teks (Bahasa, TPS)',
            'Semuanya sama saja'
        ]
    }
    
    questions['Q10'] = {
        'question': 'Saat mengerjakan soal UTBK, strategi saya:',
        'options': [
            'Kerjakan yang mudah dulu, lalu yang sulit',
            'Urut dari nomor 1 sampai selesai',
            'Lihat semua soal dulu, prioritaskan yang pasti bisa',
            'Kerjakan yang saya suka dulu'
        ]
    }
    
    questions['Q11'] = {
        'question': 'Saat mempelajari topik baru, saya lebih suka:',
        'options': [
            'Cari overview dulu, baru detail',
            'Langsung masuk ke detail dan contoh soal',
            'Cari video penjelasan terlebih dahulu',
            'Diskusi dengan orang yang sudah paham'
        ]
    }
    
    questions['Q12'] = {
        'question': 'Untuk mengingat materi, saya perlu:',
        'options': [
            'Baca berulang kali',
            'Buat rangkuman sendiri',
            'Mengajar/jelaskan ke orang lain',
            'Kerjakan banyak soal latihan'
        ]
    }
    
    # Q13-Q22: Konsistensi & Disiplin
    questions['Q13'] = {
        'question': 'Dalam seminggu, saya belajar untuk UTBK secara rutin:',
        'options': ['1-2 hari', '3-4 hari', '5-6 hari', 'Setiap hari (7 hari)']
    }
    
    questions['Q14'] = {
        'question': 'Rata-rata durasi belajar saya per hari:',
        'options': [
            'Kurang dari 1 jam',
            '1-2 jam',
            '2-3 jam',
            '3-4 jam',
            'Lebih dari 4 jam'
        ]
    }
    
    questions['Q15'] = {
        'question': 'Kemampuan saya mengikuti jadwal belajar yang sudah dibuat:',
        'options': [
            'Sangat sulit, jarang sesuai jadwal',
            'Kadang-kadang sesuai jadwal',
            'Sering sesuai jadwal',
            'Hampir selalu sesuai jadwal',
            'Selalu disiplin sesuai jadwal'
        ]
    }
    
    questions['Q16'] = {
        'question': 'Seberapa sering saya menunda belajar:',
        'options': [
            'Sangat sering menunda',
            'Sering menunda',
            'Kadang-kadang menunda',
            'Jarang menunda',
            'Hampir tidak pernah menunda'
        ]
    }
    
    questions['Q17'] = {
        'question': 'Motivasi utama saya belajar UTBK:',
        'options': [
            'Keinginan sendiri masuk kampus/jurusan impian',
            'Tuntutan orang tua',
            'Ikut-ikutan teman',
            'Target nilai/skor tertentu',
            'Gabungan dari beberapa faktor'
        ]
    }
    
    questions['Q18'] = {
        'question': 'Seberapa konsisten saya mengerjakan latihan soal:',
        'options': [
            'Jarang, hanya kalau ada PR',
            'Sesekali kalau ingat',
            'Seminggu sekali',
            'Beberapa kali seminggu',
            'Hampir setiap hari'
        ]
    }
    
    questions['Q19'] = {
        'question': 'Saya membuat target belajar harian:',
        'options': [
            'Tidak pernah membuat target',
            'Jarang membuat target',
            'Kadang-kadang membuat target',
            'Sering membuat target',
            'Selalu membuat dan evaluasi target'
        ]
    }
    
    questions['Q20'] = {
        'question': 'Jika teman mengajak main saat jadwal belajar:',
        'options': [
            'Langsung ikut main',
            'Tergantung mood',
            'Kadang ikut kadang tidak',
            'Lebih sering menolak demi belajar',
            'Tetap belajar sesuai jadwal'
        ]
    }
    
    questions['Q21'] = {
        'question': 'Seberapa sering saya mengevaluasi progress belajar:',
        'options': [
            'Tidak pernah evaluasi',
            'Sesekali saja',
            'Sebulan sekali',
            'Setiap minggu',
            'Setiap hari'
        ]
    }
    
    questions['Q22'] = {
        'question': 'Saat mendapat nilai tryout rendah, saya:',
        'options': [
            'Merasa down dan malas belajar',
            'Sedih tapi lanjut belajar biasa saja',
            'Termotivasi untuk belajar lebih giat',
            'Analisis kesalahan dan perbaiki',
            'Konsultasi dengan guru/mentor'
        ]
    }
    
    # Q23-Q32: Manajemen Waktu
    questions['Q23'] = {
        'question': 'Saya memiliki jadwal belajar tertulis/terencana:',
        'options': [
            'Tidak punya jadwal, spontan saja',
            'Ada di kepala tapi tidak tertulis',
            'Ada jadwal kasar/mingguan',
            'Ada jadwal detail per hari',
            'Ada jadwal detail + alarm reminder'
        ]
    }
    
    questions['Q24'] = {
        'question': 'Estimasi waktu luang saya untuk belajar UTBK per hari:',
        'options': [
            'Kurang dari 1 jam',
            '1-2 jam',
            '2-3 jam',
            '3-4 jam',
            'Lebih dari 4 jam'
        ]
    }
    
    questions['Q25'] = {
        'question': 'Selain sekolah, aktivitas rutin saya:',
        'options': [
            'Banyak (les 3+ mapel, ekskul, part-time)',
            'Cukup banyak (les 1-2 mapel, ekskul)',
            'Sedang (les 1 mapel atau ekskul saja)',
            'Minimal (fokus belajar mandiri)',
            'Tidak ada aktivitas lain'
        ]
    }
    
    questions['Q26'] = {
        'question': 'Cara saya prioritaskan materi belajar:',
        'options': [
            'Tidak ada prioritas, random saja',
            'Yang saya suka dulu',
            'Yang paling lemah dulu',
            'Yang bobotnya besar di UTBK',
            'Kombinasi antara lemah dan bobot besar'
        ]
    }
    
    questions['Q27'] = {
        'question': 'Gangguan terbesar saat saya belajar:',
        'options': [
            'Media sosial (Instagram, TikTok, Twitter)',
            'Notifikasi chat (WhatsApp, Line, dll)',
            'Keluarga/teman mengganggu',
            'Rasa ngantuk/lelah',
            'Tidak ada gangguan berarti'
        ]
    }
    
    questions['Q28'] = {
        'question': 'Cara saya mengelola gangguan:',
        'options': [
            'Tidak bisa menolak, sering terganggu',
            'Coba ignore tapi sering gagal',
            'Matikan notif saat belajar serius',
            'Gunakan teknik Pomodoro/app blocker',
            'Sangat disiplin, hampir tidak terganggu'
        ]
    }
    
    questions['Q29'] = {
        'question': 'Rata-rata waktu saya main media sosial per hari:',
        'options': [
            'Lebih dari 4 jam',
            '2-4 jam',
            '1-2 jam',
            'Kurang dari 1 jam',
            'Hampir tidak main medsos'
        ]
    }
    
    questions['Q30'] = {
        'question': 'Jika jadwal belajar bentrok dengan acara penting:',
        'options': [
            'Skip belajar, ganti hari lain',
            'Belajar tapi kurang fokus',
            'Reschedule dan pastikan tetap belajar',
            'Belajar di waktu lain di hari yang sama',
            'Hampir tidak pernah bentrok'
        ]
    }
    
    questions['Q31'] = {
        'question': 'Intensitas belajar saya saat akhir pekan:',
        'options': [
            'Libur total dari belajar',
            'Belajar sangat minimal',
            'Sama seperti hari biasa',
            'Lebih intensif dari hari biasa',
            'Weekend khusus untuk tryout/drilling'
        ]
    }
    
    questions['Q32'] = {
        'question': 'Rata-rata jam tidur saya per malam:',
        'options': [
            'Kurang dari 5 jam',
            '5-6 jam',
            '6-7 jam',
            '7-8 jam',
            'Lebih dari 8 jam'
        ]
    }
    
    # Q33-Q44: Kesiapan UTBK
    questions['Q33'] = {
        'question': 'Pemahaman saya tentang format soal UTBK 2026:',
        'options': [
            'Tidak tahu sama sekali',
            'Tahu sedikit',
            'Cukup tahu',
            'Sangat paham',
            'Sangat paham dan sudah sering tryout'
        ]
    }
    
    mastery_opts = ['Sangat lemah', 'Lemah', 'Sedang', 'Baik', 'Sangat baik']
    
    questions['Q34'] = {
        'question': 'Penguasaan saya terhadap Tes Potensi Skolastik (TPS):',
        'options': mastery_opts
    }
    
    questions['Q35'] = {
        'question': 'Penguasaan saya terhadap Literasi Bahasa Indonesia:',
        'options': mastery_opts
    }
    
    questions['Q36'] = {
        'question': 'Penguasaan saya terhadap Literasi Bahasa Inggris:',
        'options': mastery_opts
    }
    
    questions['Q37'] = {
        'question': 'Penguasaan saya terhadap Penalaran Matematika:',
        'options': mastery_opts
    }
    
    questions['Q38'] = {
        'question': 'Pengalaman tryout UTBK saya sejauh ini:',
        'options': [
            'Belum pernah tryout sama sekali',
            '1-2 kali tryout',
            '3-5 kali tryout',
            '6-10 kali tryout',
            'Lebih dari 10 kali tryout'
        ]
    }
    
    questions['Q39'] = {
        'question': 'Strategi saya saat menghadapi ujian/tryout:',
        'options': [
            'Belum punya strategi khusus',
            'Ada strategi tapi belum konsisten',
            'Punya strategi dasar (kerjakan yang mudah dulu)',
            'Punya strategi matang per subtes',
            'Punya strategi detail + time management'
        ]
    }
    
    questions['Q40'] = {
        'question': 'Kemampuan time management saat tryout/ujian:',
        'options': [
            'Sering tidak selesai mengerjakan',
            'Kadang selesai kadang tidak',
            'Biasanya selesai tapi buru-buru',
            'Selesai tepat waktu',
            'Selesai lebih cepat dan sempat cek jawaban'
        ]
    }
    
    questions['Q41'] = {
        'question': 'Tingkat kepercayaan diri saya untuk mencapai target UTBK:',
        'options': [
            'Sangat tidak percaya diri',
            'Kurang percaya diri',
            'Cukup percaya diri',
            'Percaya diri',
            'Sangat percaya diri'
        ]
    }
    
    questions['Q42'] = {
        'question': 'Gap antara skor tryout terakhir dengan target saya:',
        'options': [
            'Belum pernah tryout/belum tahu',
            'Sangat jauh (>150 poin)',
            'Jauh (100-150 poin)',
            'Sedang (50-100 poin)',
            'Dekat (<50 poin) atau sudah tercapai'
        ]
    }
    
    questions['Q43'] = {
        'question': 'Persiapan mental saya menghadapi UTBK:',
        'options': [
            'Sangat cemas dan tertekan',
            'Cukup cemas',
            'Biasa saja, santai',
            'Tenang dan siap',
            'Sangat siap dan excited'
        ]
    }
    
    questions['Q44'] = {
        'question': 'Saya tahu materi mana yang harus diprioritaskan:',
        'options': [
            'Tidak tahu sama sekali',
            'Masih bingung',
            'Punya gambaran kasar',
            'Cukup jelas',
            'Sangat jelas dan terukur'
        ]
    }
    
    # Q45-Q52: Kondisi Psikologis
    questions['Q45'] = {
        'question': 'Tingkat stress saya saat ini terkait UTBK:',
        'options': [
            'Sangat tinggi, mengganggu aktivitas',
            'Tinggi',
            'Sedang',
            'Rendah',
            'Sangat rendah, tidak stress'
        ]
    }
    
    questions['Q46'] = {
        'question': 'Kualitas tidur saya saat ini:',
        'options': [
            'Sangat buruk (susah tidur, sering terbangun)',
            'Buruk (kurang nyenyak)',
            'Cukup baik',
            'Baik',
            'Sangat baik (tidur nyenyak dan cukup)'
        ]
    }
    
    questions['Q47'] = {
        'question': 'Dukungan keluarga untuk persiapan UTBK saya:',
        'options': [
            'Tidak mendukung/tekanan berlebihan',
            'Kurang mendukung',
            'Cukup mendukung',
            'Sangat mendukung',
            'Luar biasa mendukung'
        ]
    }
    
    questions['Q48'] = {
        'question': 'Pandangan saya terhadap kemampuan belajar:',
        'options': [
            'Kemampuan sudah bawaan, susah berubah (fixed)',
            'Lebih banyak bawaan tapi bisa sedikit ditingkatkan',
            'Seimbang antara bawaan dan usaha',
            'Bisa ditingkatkan dengan usaha keras',
            'Bisa terus berkembang dengan metode tepat (growth)'
        ]
    }
    
    questions['Q49'] = {
        'question': 'Cara saya menghadapi kegagalan/nilai buruk:',
        'options': [
            'Menyalahkan diri sendiri dan menyerah',
            'Merasa down cukup lama',
            'Sedih sebentar lalu lanjut lagi',
            'Jadikan motivasi untuk lebih baik',
            'Analisis kesalahan dan buat perbaikan konkret'
        ]
    }
    
    questions['Q50'] = {
        'question': 'Keseimbangan belajar dan kegiatan refreshing saya:',
        'options': [
            'Tidak ada waktu refreshing, fokus belajar terus',
            'Jarang refreshing',
            'Cukup seimbang',
            'Baik, ada waktu teratur untuk refreshing',
            'Sangat baik, terjaga dengan sistem'
        ]
    }
    
    questions['Q51'] = {
        'question': 'Kemampuan saya mengelola kecemasan:',
        'options': [
            'Sangat sulit, sering overwhelmed',
            'Sulit',
            'Cukup baik',
            'Baik, punya teknik tertentu',
            'Sangat baik, tetap tenang dalam tekanan'
        ]
    }
    
    questions['Q52'] = {
        'question': 'Support system (teman/mentor/guru) yang saya miliki:',
        'options': [
            'Tidak ada yang bisa dimintai bantuan',
            'Ada tapi jarang bisa diandalkan',
            'Cukup ada',
            'Baik, ada beberapa orang yang bisa dimintai bantuan',
            'Sangat baik, ada circle yang solid'
        ]
    }
    
    return questions

# ================================================================
# MAIN APPLICATION PAGES
# ================================================================

def main():
    """Main application flow"""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Sistem Rekomendasi Belajar UTBK</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dapatkan rekomendasi belajar yang dipersonalisasi berdasarkan profilmu!</p>', 
                unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📍 Navigasi")
        st.markdown("---")
        
        # Progress tracker
        steps = {
            'profile': '1️⃣ Profil Siswa',
            'survey': '2️⃣ Survey Study Habits',
            'results': '3️⃣ Hasil & Rekomendasi'
        }
        
        current_step_num = list(steps.keys()).index(st.session_state.step) + 1
        st.progress(current_step_num / len(steps))
        st.markdown(f"**Step {current_step_num}/{len(steps)}**")
        st.markdown(f"*{steps[st.session_state.step]}*")
        st.markdown("---")
        
        # Additional info
        st.info("💡 **Tips:**\n\n"
                "• Jawab dengan jujur\n"
                "• Tidak ada jawaban benar/salah\n"
                "• Estimasi waktu: 15-20 menit")
    
    # Route to appropriate page
    if st.session_state.step == 'profile':
        profile_page()
    elif st.session_state.step == 'survey':
        survey_page()
    elif st.session_state.step == 'results':
        results_page()

def profile_page():
    """Halaman input profil siswa"""
    st.header("📝 Profil Siswa")
    st.markdown("Isi data diri dan skor UTBK terakhirmu dengan lengkap")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input(
                "Nama Lengkap*", 
                value=st.session_state.profile_data.get('nama', ''),
                placeholder="Masukkan nama lengkap"
            )
            
            kelas_options = [10, 11, 12]
            kelas_default = st.session_state.profile_data.get('kelas', 12)
            kelas = st.selectbox(
                "Kelas*", 
                kelas_options,
                index=kelas_options.index(kelas_default) if kelas_default in kelas_options else 2
            )
            
            jurusan_options = [
                'Kedokteran', 'Teknik Informatika', 'Hukum', 'Psikologi',
                'Akuntansi', 'Manajemen', 'Teknik Elektro', 'Arsitektur',
                'Farmasi', 'Desain Komunikasi Visual', 'Ilmu Komunikasi',
                'Teknik Sipil', 'Ekonomi', 'Hubungan Internasional', 'Lainnya'
            ]
            jurusan_default = st.session_state.profile_data.get('jurusan', 'Kedokteran')
            jurusan = st.selectbox(
                "Jurusan Impian*", 
                jurusan_options,
                index=jurusan_options.index(jurusan_default) if jurusan_default in jurusan_options else 0
            )
            
        with col2:
            kampus_options = [
                'Universitas Indonesia', 'ITB', 'UGM', 'IPB', 'ITS',
                'Universitas Airlangga', 'Universitas Brawijaya',
                'Universitas Diponegoro', 'Universitas Padjadjaran',
                'Universitas Hasanuddin', 'Universitas Sebelas Maret', 'Lainnya'
            ]
            kampus_default = st.session_state.profile_data.get('kampus', 'Universitas Indonesia')
            kampus = st.selectbox(
                "Kampus Impian*", 
                kampus_options,
                index=kampus_options.index(kampus_default) if kampus_default in kampus_options else 0
            )
            
            target_skor = st.number_input(
                "Target Skor Total UTBK*", 
                min_value=500, 
                max_value=4000, 
                value=st.session_state.profile_data.get('target_skor', 2800),
                step=50,
                help="Total skor target dari semua subtes (TPS + Literasi Indo + Literasi Inggris + Penalaran Mat)"
            )
            
            waktu_options = ['< 1 jam', '1-2 jam', '2-3 jam', '3-4 jam', '> 4 jam']
            waktu_default = st.session_state.profile_data.get('waktu_belajar', '2-3 jam')
            waktu_belajar = st.select_slider(
                "Waktu Belajar Tersedia per Hari",
                options=waktu_options,
                value=waktu_default if waktu_default in waktu_options else '2-3 jam'
            )
        
        st.markdown("### 📊 Skor Tryout Terakhir")
        st.caption("*Isi dengan skor terakhir yang kamu dapat. Jika belum pernah tryout, isi dengan perkiraan kemampuanmu saat ini.*")
        
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            skor_tps = st.number_input(
                "TPS", 
                min_value=200, 
                max_value=1000, 
                value=st.session_state.profile_data.get('skor_tps', 600),
                step=10,
                help="Tes Potensi Skolastik"
            )
        
        with col4:
            skor_literasi_indo = st.number_input(
                "Literasi Indonesia", 
                min_value=200, 
                max_value=1000,
                value=st.session_state.profile_data.get('skor_literasi_indo', 600),
                step=10
            )
        
        with col5:
            skor_literasi_inggris = st.number_input(
                "Literasi Inggris", 
                min_value=200, 
                max_value=1000,
                value=st.session_state.profile_data.get('skor_literasi_inggris', 600),
                step=10
            )
        
        with col6:
            skor_penalaran_mat = st.number_input(
                "Penalaran Matematika", 
                min_value=200, 
                max_value=1000,
                value=st.session_state.profile_data.get('skor_penalaran_mat', 600),
                step=10
            )
        
        # Quick summary
        total_current = skor_tps + skor_literasi_indo + skor_literasi_inggris + skor_penalaran_mat
        gap_amount = target_skor - total_current
        st.info(f"📊 **Total Skor Saat Ini:** {total_current} | **Target:** {target_skor} | **Gap:** {gap_amount} poin")
        
        st.markdown("---")
        submit = st.form_submit_button("Lanjut ke Survey →", type="primary")
        
        if submit:
            if not nama:
                st.error("⚠️ Nama harus diisi!")
            elif total_current > target_skor:
                st.warning("⚠️ Total skor saat ini sudah melebihi target. Apakah kamu yakin dengan data yang diisi?")
            else:
                # Save profile data
                st.session_state.profile_data = {
                    'nama': nama,
                    'kelas': kelas,
                    'jurusan': jurusan,
                    'kampus': kampus,
                    'target_skor': target_skor,
                    'skor_tps': skor_tps,
                    'skor_literasi_indo': skor_literasi_indo,
                    'skor_literasi_inggris': skor_literasi_inggris,
                    'skor_penalaran_mat': skor_penalaran_mat,
                    'waktu_belajar': waktu_belajar
                }
                
                st.session_state.step = 'survey'
                st.success("✅ Profil berhasil disimpan!")
                st.rerun()

def survey_page():
    """Halaman survey 52 pertanyaan"""
    st.header("📋 Survey Study Habits")
    st.markdown(f"Halo **{st.session_state.profile_data['nama']}**! Jawab 52 pertanyaan berikut dengan jujur.")
    st.caption("💡 Survey ini akan membantu kami memahami gaya belajarmu untuk memberikan rekomendasi yang paling tepat.")
    
    # Load survey questions
    survey_questions = get_survey_questions()
    
    # Create tabs untuk setiap bagian
    tabs = st.tabs([
        "🎨 Gaya Belajar (Q1-12)",
        "💪 Konsistensi (Q13-22)", 
        "⏰ Manajemen Waktu (Q23-32)",
        "📚 Kesiapan UTBK (Q33-44)",
        "🧘 Kondisi Psikologis (Q45-52)"
    ])
    
    responses = {}
    
    # TAB 1: Gaya Belajar (Q1-12)
    with tabs[0]:
        st.markdown("### 🎨 Gaya Belajar & Preferensi Kognitif")
        for i in range(1, 13):
            q = survey_questions[f'Q{i}']
            default_val = st.session_state.survey_responses.get(f'Q{i}', q['options'][0])
            default_idx = q['options'].index(default_val) if default_val in q['options'] else 0
            
            responses[f'Q{i}'] = st.radio(
                f"**Q{i}. {q['question']}**",
                options=q['options'],
                key=f'Q{i}',
                index=default_idx
            )
            st.markdown("---")
    
    # TAB 2: Konsistensi (Q13-22)
    with tabs[1]:
        st.markdown("### 💪 Konsistensi & Disiplin Belajar")
        for i in range(13, 23):
            q = survey_questions[f'Q{i}']
            default_val = st.session_state.survey_responses.get(f'Q{i}', q['options'][0])
            default_idx = q['options'].index(default_val) if default_val in q['options'] else 0
            
            responses[f'Q{i}'] = st.radio(
                f"**Q{i}. {q['question']}**",
                options=q['options'],
                key=f'Q{i}',
                index=default_idx
            )
            st.markdown("---")
    
    # TAB 3: Manajemen Waktu (Q23-32)
    with tabs[2]:
        st.markdown("### ⏰ Manajemen Waktu & Prioritas")
        for i in range(23, 33):
            q = survey_questions[f'Q{i}']
            default_val = st.session_state.survey_responses.get(f'Q{i}', q['options'][0])
            default_idx = q['options'].index(default_val) if default_val in q['options'] else 0
            
            responses[f'Q{i}'] = st.radio(
                f"**Q{i}. {q['question']}**",
                options=q['options'],
                key=f'Q{i}',
                index=default_idx
            )
            st.markdown("---")
    
    # TAB 4: Kesiapan UTBK (Q33-44)
    with tabs[3]:
        st.markdown("### 📚 Kesiapan & Pemahaman UTBK")
        for i in range(33, 45):
            q = survey_questions[f'Q{i}']
            default_val = st.session_state.survey_responses.get(f'Q{i}', q['options'][0])
            default_idx = q['options'].index(default_val) if default_val in q['options'] else 0
            
            responses[f'Q{i}'] = st.radio(
                f"**Q{i}. {q['question']}**",
                options=q['options'],
                key=f'Q{i}',
                index=default_idx
            )
            st.markdown("---")
    
    # TAB 5: Kondisi Psikologis (Q45-52)
    with tabs[4]:
        st.markdown("### 🧘 Kondisi Psikologis & Kesejahteraan")
        for i in range(45, 53):
            q = survey_questions[f'Q{i}']
            default_val = st.session_state.survey_responses.get(f'Q{i}', q['options'][0])
            default_idx = q['options'].index(default_val) if default_val in q['options'] else 0
            
            responses[f'Q{i}'] = st.radio(
                f"**Q{i}. {q['question']}**",
                options=q['options'],
                key=f'Q{i}',
                index=default_idx
            )
            st.markdown("---")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Kembali ke Profil", use_container_width=True):
            st.session_state.step = 'profile'
            st.rerun()
    
    with col2:
        if st.button("Lihat Hasil →", type="primary", use_container_width=True):
            st.session_state.survey_responses = responses
            st.session_state.step = 'results'
            st.rerun()

def results_page():
    """Halaman hasil dan rekomendasi"""
    st.header("🎯 Hasil Analisis & Rekomendasi Belajar")
    
    # Process survey responses
    with st.spinner("🔄 Menganalisis profil belajarmu..."):
        try:
            # Load resources
            models = load_app_models()
            mappings = load_app_mappings()
            learner_descriptions = load_learner_descriptions()
            
            # Check if models loaded successfully
            if models is None:
                st.error("❌ Error: Model files tidak ditemukan. Pastikan folder 'models/' berisi semua file yang diperlukan.")
                st.stop()
            
            # Encode responses
            encoded = encode_survey_responses(st.session_state.survey_responses, mappings)
            
            # Calculate dimension scores
            dimension_scores = calculate_dimension_scores(encoded)
            
            # Predict learner type
            learner_type = predict_learner_type(dimension_scores, models)
            
            # Gap analysis
            current_scores = {
                'TPS': st.session_state.profile_data['skor_tps'],
                'Literasi_Indo': st.session_state.profile_data['skor_literasi_indo'],
                'Literasi_Inggris': st.session_state.profile_data['skor_literasi_inggris'],
                'Penalaran_Mat': st.session_state.profile_data['skor_penalaran_mat']
            }
            gap_analysis = calculate_gap_analysis(current_scores, st.session_state.profile_data['target_skor'])
            
            # Generate recommendations
            recommendations = generate_study_plan(learner_type, dimension_scores, gap_analysis)
            
            # Generate milestones
            milestones = generate_milestones(gap_analysis, months_to_utbk=4)
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat memproses data: {str(e)}")
            st.info("💡 Pastikan semua file di folder 'models/' sudah lengkap dan benar.")
            st.stop()
    
    # Display results
    st.success("✅ Analisis selesai!")
    
    # Learner Type Card
    learner_info = learner_descriptions.get(learner_type, {})
    st.markdown(f"""
    <div class="learner-card">
        <h1 style="text-align: center; font-size: 4rem;">{learner_info.get('emoji', '🎓')}</h1>
        <h2 style="text-align: center; margin: 10px 0;">{learner_type}</h2>
        <p style="text-align: center; font-size: 1.2rem; margin: 15px 0;">{learner_info.get('description', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs untuk hasil
    result_tabs = st.tabs([
        "📊 Profil Dimensi",
        "📈 Gap Analysis",
        "📚 Rekomendasi Belajar",
        "📅 Study Plan",
        "🎯 Milestone Timeline"
    ])
    
    # TAB 1: Profil Dimensi
    with result_tabs[0]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Radar chart
            fig = go.Figure()
            
            categories = [k.replace('_', ' ') for k in dimension_scores.keys()]
            values = list(dimension_scores.values())
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Skor Kamu',
                line=dict(color='#FF4B4B', width=2)
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True, 
                        range=[0, 100],
                        tickfont=dict(size=10)
                    )
                ),
                showlegend=False,
                title="Profil 5 Dimensi Belajar",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Skor per Dimensi")
            st.caption("Skala: 0-100 (semakin tinggi semakin baik)")
            
            for dim, score in dimension_scores.items():
                dim_name = dim.replace('_', ' ')
                
                # Color based on score
                if score >= 75:
                    color = "🟢"
                elif score >= 50:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.metric(f"{color} {dim_name}", f"{score:.1f}/100")
                st.progress(score / 100)
                st.markdown("")
        
        # Strengths & Focus Areas
        st.markdown("---")
        col_s, col_f = st.columns(2)
        
        with col_s:
            st.markdown("### 💪 Kekuatan Kamu")
            for strength in learner_info.get('strengths', []):
                st.success(f"✓ {strength}")
        
        with col_f:
            st.markdown("### 🎯 Area untuk Ditingkatkan")
            for area in learner_info.get('focus_areas', []):
                st.info(f"→ {area}")
    
    # TAB 2: Gap Analysis
    with result_tabs[1]:
        st.markdown("### 📈 Analisis Kesenjangan Skor")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Skor Saat Ini", gap_analysis['total_current'])
        col2.metric("Target Skor", gap_analysis['total_target'])
        col3.metric("Gap", gap_analysis['total_gap'], delta=f"-{gap_analysis['gap_percentage']:.1f}%")
        col4.metric("Status", gap_analysis['status'])
        
        st.markdown("---")
        
        # Bar chart gap per subtes
        fig = go.Figure()
        
        subjects = [s.replace('_', ' ') for s in current_scores.keys()]
        current = list(current_scores.values())
        target_per_subtes = [gap_analysis['total_target'] / 4] * 4
        
        fig.add_trace(go.Bar(
            name='Skor Saat Ini', 
            x=subjects, 
            y=current,
            marker_color='#667eea'
        ))
        fig.add_trace(go.Bar(
            name='Target Rata-rata', 
            x=subjects, 
            y=target_per_subtes,
            marker_color='#FF4B4B'
        ))
        
        fig.update_layout(
            barmode='group', 
            title='Perbandingan Skor Saat Ini vs Target',
            xaxis_title="Subtes",
            yaxis_title="Skor",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        st.markdown("---")
        col_weak, col_strong = st.columns(2)
        
        with col_weak:
            st.markdown(f"### 🔴 Area Terlemah")
            st.error(f"**{gap_analysis['weakest_area'].replace('_', ' ')}**")
            st.caption("Prioritaskan fokus di area ini untuk improvement maksimal")
        
        with col_strong:
            st.markdown(f"### 🟢 Area Terkuat")
            st.success(f"**{gap_analysis['strongest_area'].replace('_', ' ')}**")
            st.caption("Pertahankan performa bagus di area ini")
    
    # TAB 3: Rekomendasi
    with result_tabs[2]:
        st.markdown("### 🎯 Metode Belajar yang Disarankan")
        st.caption("Berdasarkan profil learner type kamu")
        
        for method in recommendations['study_methods']:
            st.markdown(f"{method}")
            st.markdown("")
        
        st.markdown("---")
        st.markdown("### ⏰ Alokasi Waktu Belajar")
        
        col_pie, col_table = st.columns([1, 1])
        
        with col_pie:
            fig = go.Figure(data=[go.Pie(
                labels=list(recommendations['time_allocation'].keys()),
                values=list(recommendations['time_allocation'].values()),
                hole=.4,
                marker=dict(colors=['#FF4B4B', '#667eea', '#764ba2', '#FFA500'])
            )])
            fig.update_layout(
                title='Distribusi Waktu Belajar (%)',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_table:
            st.markdown("#### 📊 Detail Alokasi")
            for subject, percentage in recommendations['time_allocation'].items():
                st.metric(subject, f"{percentage}%")
        
        st.markdown("---")
        st.markdown("### 💡 Tips & Strategi Khusus")
        
        for tip in recommendations['tips']:
            st.info(tip)
    
    # TAB 4: Study Plan
    with result_tabs[3]:
        st.markdown("### 📅 Rencana Belajar Mingguan")
        st.caption("Template jadwal yang bisa kamu sesuaikan dengan kondisimu")
        
        for day, plan in recommendations['weekly_plan'].items():
            with st.expander(f"**{day}** - {plan['focus']}", expanded=False):
                st.markdown(f"**🎯 Fokus:** {plan['focus']}")
                st.markdown("**📋 Aktivitas:**")
                for activity in plan['activities']:
                    st.markdown(f"- {activity}")
    
    # TAB 5: Milestones
    with result_tabs[4]:
        st.markdown("### 🎯 Timeline Milestone hingga UTBK")
        st.caption("Target bertahap untuk mencapai skor impianmu")
        
        for idx, milestone in enumerate(milestones):
            with st.expander(f"**Bulan {milestone['month']}: {milestone['title']}**", expanded=(idx==0)):
                col_m1, col_m2 = st.columns([2, 1])
                
                with col_m1:
                    st.markdown(f"**🎯 Target:** {milestone['target']}")
                    st.markdown(f"**📈 Score Target:** {milestone['score_target']}")
                    st.markdown(f"**📝 Action Plan:** {milestone['action']}")
                    st.markdown(f"**💡 Focus:** {milestone['focus']}")
                
                with col_m2:
                    progress = milestone.get('progress', 0)
                    st.metric("Progress Target", f"{progress}%")
                    st.progress(progress / 100)
    
    # Action buttons
    st.markdown("---")
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        if st.button("📥 Download Laporan (PDF)", use_container_width=True):
            st.info("📌 Fitur download PDF dalam pengembangan...")
    
    with col_b2:
        if st.button("📤 Share Hasil", use_container_width=True):
            st.info("📌 Fitur share dalam pengembangan...")
    
    with col_b3:
        if st.button("🔄 Mulai dari Awal", use_container_width=True):
            st.session_state.step = 'profile'
            st.session_state.profile_data = {}
            st.session_state.survey_responses = {}
            st.rerun()

if __name__ == "__main__":
    main()