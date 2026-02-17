"""
Generate personalized study recommendations
UTBK 2026 - 7 Subtes Lengkap:
- Penalaran Umum (PU)
- Pengetahuan & Pemahaman Umum (PPU)
- Pemahaman Bacaan & Menulis (PBM)
- Pengetahuan Kuantitatif (PK)
- Literasi Indonesia
- Literasi Inggris
- Penalaran Matematika
"""

# ================================================================
# ALOKASI WAKTU PER LEARNER TYPE (Total = 100%)
# 7 subtes: PU, PPU, PBM, PK, Literasi Indo, Literasi Inggris, Penalaran Mat
# ================================================================

TIME_ALLOCATION = {
    "Strategic Achiever": {
        'Penalaran Umum': 15,
        'Pengetahuan & Pemahaman Umum': 10,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 15,
        'Literasi Indonesia': 15,
        'Literasi Inggris': 15,
        'Penalaran Matematika': 15,
    },
    "Diligent Scholar": {
        'Penalaran Umum': 15,
        'Pengetahuan & Pemahaman Umum': 15,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 15,
        'Literasi Indonesia': 15,
        'Literasi Inggris': 10,
        'Penalaran Matematika': 15,
    },
    "Fast Learner": {
        'Penalaran Umum': 20,
        'Pengetahuan & Pemahaman Umum': 10,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 15,
        'Literasi Indonesia': 15,
        'Literasi Inggris': 10,
        'Penalaran Matematika': 15,
    },
    "Resilient Fighter": {
        'Penalaran Umum': 10,
        'Pengetahuan & Pemahaman Umum': 15,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 10,
        'Literasi Indonesia': 20,
        'Literasi Inggris': 20,
        'Penalaran Matematika': 10,
    },
    "Growing Learner": {
        'Penalaran Umum': 15,
        'Pengetahuan & Pemahaman Umum': 15,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 15,
        'Literasi Indonesia': 15,
        'Literasi Inggris': 10,
        'Penalaran Matematika': 15,
    },
    "Inconsistent Talent": {
        'Penalaran Umum': 20,
        'Pengetahuan & Pemahaman Umum': 10,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 15,
        'Literasi Indonesia': 15,
        'Literasi Inggris': 10,
        'Penalaran Matematika': 15,
    },
    "Methodical Planner": {
        'Penalaran Umum': 15,
        'Pengetahuan & Pemahaman Umum': 10,
        'Pemahaman Bacaan & Menulis': 15,
        'Pengetahuan Kuantitatif': 15,
        'Literasi Indonesia': 15,
        'Literasi Inggris': 15,
        'Penalaran Matematika': 15,
    },
    "Needs Support": {
        'Penalaran Umum': 10,
        'Pengetahuan & Pemahaman Umum': 15,
        'Pemahaman Bacaan & Menulis': 20,
        'Pengetahuan Kuantitatif': 10,
        'Literasi Indonesia': 20,
        'Literasi Inggris': 15,
        'Penalaran Matematika': 10,
    },
}

# ================================================================
# TIPS PER SUBTES - BAHASA GEN Z
# ================================================================

TIPS_PER_SUBTES = {
    'Penalaran Umum': [
        "🧠 **Penalaran Umum:** Latih pola-pola soal analogi, silogisme, dan deret angka secara rutin setiap hari minimal 15 soal",
        "⚡ Saat ngerjain soal PU, jangan terlalu lama di satu soal — skip dulu kalau stuck, balik lagi nanti",
        "🔍 Biasakan berpikir dari yang diketahui ke yang ditanya (top-down), bukan hafalan",
    ],
    'Pengetahuan & Pemahaman Umum': [
        "📰 **PPU:** Update wawasan umum tiap hari — baca berita, artikel sains, sejarah singkat minimal 15 menit",
        "🗂️ Buat catatan 'fakta keren' dari berbagai bidang: geografi, IPA, IPS, budaya — ini banget yang keluar di PPU",
        "🎯 Hafal konsep-konsep dasar lintas mata pelajaran, bukan detail — PPU lebih ke breadth bukan depth",
    ],
    'Pemahaman Bacaan & Menulis': [
        "📖 **PBM:** Biasakan baca teks panjang dengan cepat sambil ambil ide pokok setiap paragraf",
        "✍️ Latihan identifikasi: ide utama, gagasan pendukung, tujuan penulis, dan kesimpulan logis",
        "⏰ Speed reading adalah kunci PBM — target baca 1 teks dalam 3-4 menit sebelum jawab soal",
    ],
    'Pengetahuan Kuantitatif': [
        "🔢 **PK:** Kuasai operasi bilangan, rasio, persentase, dan interpretasi tabel/grafik dulu sebelum ke yang susah",
        "📊 Banyak soal PK adalah soal data — rajin latihan baca grafik batang, garis, dan diagram lingkaran",
        "🧮 Hafalin shortcut hitungan cepat: perkalian, pembagian, dan konversi satuan biar nggak buang waktu",
    ],
    'Literasi Indonesia': [
        "📚 **Literasi Indo:** Baca beragam jenis teks: narasi, deskripsi, argumentasi, prosedur — biasakan setiap hari",
        "🎯 Fokus latihan soal tipe: makna kata, koherensi paragraf, perbaikan kalimat, dan simpulan",
        "💡 Perhatikan EYD dan struktur kalimat efektif — sering keluar di soal perbaikan teks",
    ],
    'Literasi Inggris': [
        "🌏 **Literasi Inggris:** Mulai biasain konsumsi konten bahasa Inggris: YouTube, artikel, podcast",
        "📝 Kuasai vocabulary akademik (Academic Word List) — banyak muncul di teks UTBK Inggris",
        "🔑 Strategi: baca pertanyaan dulu sebelum baca teks — cari clue yang relevan, jangan baca semua",
    ],
    'Penalaran Matematika': [
        "➕ **Penalaran Mat:** Fokus ke konsep aljabar, geometri, statistika, dan logika matematika",
        "🧩 Soal Penalaran Matematika beda dari Mat SMA — lebih ke cara pikir, bukan rumus hafalan",
        "📐 Latihan soal cerita (word problem) tiap hari — ini yang paling sering bikin siswa kesulitan",
    ],
}

# ================================================================
# STUDY METHODS PER LEARNER TYPE
# ================================================================

STUDY_METHODS = {
    "Strategic Achiever": [
        "🔥 **Drilling HOTS:** Fokus ke soal-soal level tinggi yang punya banyak jebakan — ini buat maintain dan naik level",
        "📊 **Error Log Sistem:** Setiap soal yang salah, catat: topik, kenapa salah, cara benar. Review mingguan wajib!",
        "⏱️ **Weekly Tryout:** Ikutin simulasi UTBK setiap minggu untuk menjaga ritme dan mental bertanding",
        "🤝 **Peer Teaching:** Ajarin teman — kalau kamu bisa jelasin, berarti kamu beneran paham (Feynman Technique)",
        "🎯 **Targeted Practice:** Identifikasi topik yang masih kurang meski udah bagus, hajar habis-habisan",
    ],
    "Diligent Scholar": [
        "⏰ **Pomodoro Technique:** 25 menit fokus + 5 menit break — efektif banget buat jaga konsentrasi tanpa burnout",
        "📅 **Time Blocking:** Jadwal detail per subtes per hari — kamu tipe yang works best dengan struktur jelas",
        "🔄 **Spaced Repetition:** Pakai aplikasi Anki atau Notion untuk review materi secara berkala",
        "🧠 **Deep Learning:** Jangan puas hafalan — pahami KENAPA rumus/konsep itu berlaku",
        "📈 **Weekly Review:** Evaluasi progress tiap Minggu malam, adjust jadwal kalau perlu",
    ],
    "Fast Learner": [
        "🚀 **Variasi Soal Luas:** Ekspos diri ke berbagai tipe soal dari berbagai sumber, jangan cuma satu bank soal",
        "🏆 **Challenge Yourself:** Coba soal olimpiade atau soal UTBK tahun-tahun lalu yang dikurasi susahnya",
        "🗣️ **Feynman Technique:** Ajarkan materi ke teman atau rekam penjelasan sendiri — ini solidify understanding",
        "⚠️ **Jangan Skip Fundamentals:** Kecepatan belajar tinggi kadang bikin skip basics — balik ke dasar kalau perlu",
        "📌 **Depth Over Breadth:** Kuasai benar-benar satu topik sebelum lanjut — jangan setengah-setengah",
    ],
    "Resilient Fighter": [
        "💪 **Drilling Intensif:** Mental kuat adalah modal utama — manfaatin untuk push meski capek",
        "🗺️ **Mind Mapping:** Buat mind map visual untuk setiap topik besar — bantu bangun koneksi antar konsep",
        "🎯 **Foundation First:** Bangun fondasi yang kuat dulu di setiap subtes sebelum naik level",
        "📊 **Progress Tracking:** Catat skor setiap tryout dan visualisasikan grafik naik — ini boost motivasi",
        "🔁 **Consistent Tryout:** Latihan di bawah tekanan waktu secara rutin untuk build exam confidence",
    ],
    "Growing Learner": [
        "🎬 **Video-Based Learning:** Mulai dari video penjelasan (Zenius, Ruangguru, YouTube) sebelum baca buku",
        "👥 **Study Group:** Gabung komunitas belajar UTBK — peer support dan peer learning sangat membantu",
        "🏆 **Small Wins:** Set target kecil harian yang realistis dan rayakan setiap pencapaian — keep the momentum!",
        "📚 **Basics First:** Jangan loncat ke soal sulit dulu — kuasai dasar-dasar dengan benar dulu",
        "📆 **Habit Tracker:** Pakai aplikasi habit tracker untuk jaga konsistensi belajar harian",
    ],
    "Inconsistent Talent": [
        "👫 **Accountability Partner:** Cari study buddy yang bisa saling tagih progress harian — works banget!",
        "🏅 **Reward System:** Buat sistem reward personal — kalau target tercapai, kasih reward ke diri sendiri",
        "📱 **App Blocker:** Gunakan app blocker (Forest, Cold Turkey) saat sesi belajar untuk eliminasi distraksi",
        "⚡ **Short but Intense:** Daripada lama tapi gak fokus, lebih baik 45 menit benar-benar fokus",
        "📋 **Daily Micro-Goals:** Buat target kecil tiap hari yang bisa diceklis — rasa puas itu bikin nagih",
    ],
    "Methodical Planner": [
        "🗺️ **Master Timeline:** Buat timeline besar dari sekarang sampai UTBK dengan breakdown per minggu",
        "⏱️ **Timed Practice:** Selalu latihan dengan timer — biasakan diri dengan tekanan waktu ujian nyata",
        "📊 **Data-Driven Review:** Analisis statistik skor tryout bulanan — cari pattern kesalahan yang berulang",
        "⚠️ **Action Over Planning:** Kamu jago planning, tapi jangan overdone — eksekusi tetap #1",
        "🔄 **Flexible Adjustment:** Siap adjust jadwal kalau ada yang gak sesuai — rigiditas terlalu tinggi bisa backfire",
    ],
    "Needs Support": [
        "🤝 **Cari Mentor:** Temukan guru/kakak kelas/tutor yang bisa guide intensif — ini game changer buat kamu",
        "🔤 **Absolute Basics:** Mulai dari level paling dasar tanpa malu — fondasi kuat itu kunci segalanya",
        "👥 **Small Group Learning:** Belajar dalam kelompok kecil (3-4 orang) lebih efektif dari solo untuk tipe kamu",
        "🎯 **Focus on 1-2 Subtes:** Jangan coba kuasai semua sekaligus — pilih 2 subtes prioritas dulu",
        "📅 **Strict Routine:** Buat jadwal yang sangat terstruktur dan patuhi — konsistensi adalah jalan satu-satunya",
    ],
}

# ================================================================
# WEEKLY PLAN - DISESUAIKAN DENGAN 7 SUBTES
# ================================================================

def get_weekly_plan(learner_type, weakest_area=""):
    """Generate weekly plan berdasarkan learner type dan area terlemah"""

    base_plans = {
        "Strategic Achiever": {
            'Senin':  {'focus': 'Penalaran Umum + PPU — asah logika',
                       'activities': ['🧠 PU Drilling HOTS (1.5 jam)', '📰 PPU Wawasan Umum (1 jam)', '📊 Analisis error minggu lalu (30 menit)']},
            'Selasa': {'focus': 'Literasi Indonesia + PBM — bahasa power-up',
                       'activities': ['📚 Literasi Indo intensive (1.5 jam)', '📖 PBM speed reading practice (1 jam)', '✏️ Latihan nulis argumentatif (30 menit)']},
            'Rabu':   {'focus': 'Penalaran Matematika + PK — number crunching',
                       'activities': ['➕ Penalaran Mat HOTS (1.5 jam)', '🔢 PK data interpretation (1 jam)', '🧮 Drill hitungan cepat (30 menit)']},
            'Kamis':  {'focus': 'Literasi Inggris — English unlocked',
                       'activities': ['🌏 Literasi Inggris reading (1.5 jam)', '📝 Vocabulary HOTS level (1 jam)', '🎧 Konsumsi konten English (30 menit)']},
            'Jumat':  {'focus': 'Mixed Drilling — semua subtes',
                       'activities': ['🎯 Mix soal semua subtes (2 jam)', '📊 Update error log (30 menit)', '📅 Revisi jadwal minggu depan (30 menit)']},
            'Sabtu':  {'focus': '🔥 Full Tryout Simulasi UTBK',
                       'activities': ['📝 Tryout lengkap 7 subtes (3.5 jam)', '🔍 Analisis hasil mendalam (1 jam)', '📌 Catat target perbaikan (30 menit)']},
            'Minggu': {'focus': '🧘 Review + Recharge',
                       'activities': ['📖 Review materi paling lemah minggu ini (1.5 jam)', '🗺️ Planning minggu depan (30 menit)', '😌 Refreshing — jaga mental health!']},
        },
        "Diligent Scholar": {
            'Senin':  {'focus': 'PU + PPU — bangun wawasan dan logika',
                       'activities': ['🧠 PU konsep + latihan (1.5 jam)', '📰 PPU materi wawasan umum (1 jam)', '🔄 Spaced repetition review (30 menit)']},
            'Selasa': {'focus': 'PBM + Literasi Indo — kuasai teks Indonesia',
                       'activities': ['📖 PBM latihan teks panjang (1.5 jam)', '📚 Literasi Indo tipe soal (1 jam)', '✏️ Latihan EYD dan kalimat efektif (30 menit)']},
            'Rabu':   {'focus': 'PK + Penalaran Mat — matematika total',
                       'activities': ['🔢 PK grafik dan tabel (1.5 jam)', '➕ Penalaran Mat konsep (1 jam)', '🧮 Drill soal cerita (30 menit)']},
            'Kamis':  {'focus': 'Literasi Inggris — English day',
                       'activities': ['🌏 Literasi Inggris reading (1.5 jam)', '📝 Vocabulary building (1 jam)', '🎧 English podcast/video (30 menit)']},
            'Jumat':  {'focus': 'Weak Area Day — fokus yang paling lemah',
                       'activities': ['🎯 Drilling area terlemah (2 jam)', '📊 Review catatan error (30 menit)', '📋 Update progress tracker (30 menit)']},
            'Sabtu':  {'focus': '📝 Tryout Simulasi + Evaluasi',
                       'activities': ['📝 Simulasi tryout (3 jam)', '🔍 Analisis kesalahan (1 jam)', '📌 Buat target perbaikan (30 menit)']},
            'Minggu': {'focus': '📚 Review + Planning',
                       'activities': ['🔄 Review topik sulit minggu ini (1.5 jam)', '📅 Buat jadwal detail minggu depan (30 menit)', '😴 Rest dan recharge!']},
        },
        "Growing Learner": {
            'Senin':  {'focus': 'PU dasar — logika step by step',
                       'activities': ['🎬 Video penjelasan PU (1 jam)', '📝 Latihan soal PU level mudah (1 jam)', '📓 Bikin rangkuman singkat (30 menit)']},
            'Selasa': {'focus': 'Literasi Indonesia dasar',
                       'activities': ['🎬 Video materi Literasi Indo (1 jam)', '📚 Latihan soal teks pendek (1 jam)', '✏️ Latihan menulis paragraf (30 menit)']},
            'Rabu':   {'focus': 'PPU + PBM — wawasan dan bacaan',
                       'activities': ['📰 Baca artikel wawasan umum (1 jam)', '📖 Latihan membaca cepat PBM (1 jam)', '🗒️ Catat fakta baru yang dipelajari (30 menit)']},
            'Kamis':  {'focus': 'PK + Penalaran Mat — angka pelan tapi pasti',
                       'activities': ['🔢 Video penjelasan PK (1 jam)', '➕ Latihan soal Mat level dasar (1 jam)', '🧮 Drill operasi dasar (30 menit)']},
            'Jumat':  {'focus': 'Literasi Inggris — English basic',
                       'activities': ['🌏 Vocabulary bahasa Inggris (1 jam)', '📝 Latihan soal Literasi Inggris mudah (1 jam)', '🎧 Nonton konten Inggris dengan subtitle (30 menit)']},
            'Sabtu':  {'focus': '📝 Mini Tryout + Evaluasi santai',
                       'activities': ['📝 Mini tryout 3-4 subtes (2 jam)', '🔍 Cek jawaban dan pahami pembahasan (1 jam)', '📋 Catat topik yang perlu diulang (30 menit)']},
            'Minggu': {'focus': '🧘 Review pelan + Semangat!',
                       'activities': ['🔄 Ulangi materi yang belum paham (1.5 jam)', '🏆 Rayakan progress minggu ini!', '😌 Istirahat penuh — besok lanjut lagi']},
        },
        "Needs Support": {
            'Senin':  {'focus': 'Literasi Indo — mulai dari yang familiar',
                       'activities': ['📚 Materi dasar Literasi Indo (1 jam)', '📝 5-10 soal level mudah saja (30 menit)', '🤝 Diskusi dengan teman/guru (30 menit)']},
            'Selasa': {'focus': 'PU — logika dasar pelan-pelan',
                       'activities': ['🎬 Video PU untuk pemula (1 jam)', '📝 Latihan 5-10 soal mudah (30 menit)', '📓 Tulis ulang apa yang dipahami hari ini (30 menit)']},
            'Rabu':   {'focus': 'PPU + PBM — wawasan dan teks',
                       'activities': ['📰 Baca artikel ringan + rangkum (1 jam)', '📖 Latihan soal PBM level dasar (30 menit)', '🤝 Tanya ke guru kalau ada yang bingung (30 menit)']},
            'Kamis':  {'focus': 'Literasi Inggris — basics only',
                       'activities': ['📝 Kosakata dasar bahasa Inggris (1 jam)', '📖 Baca teks pendek bahasa Inggris (30 menit)', '🎬 Video grammar dasar (30 menit)']},
            'Jumat':  {'focus': 'PK dasar — angka step by step',
                       'activities': ['🔢 Operasi dasar dan persentase (1 jam)', '📊 Latihan baca grafik sederhana (30 menit)', '🧮 10 soal PK level mudah (30 menit)']},
            'Sabtu':  {'focus': '📝 Mini tryout 2 subtes saja',
                       'activities': ['📝 Tryout kecil 2 subtes terkuat (1.5 jam)', '🔍 Pahami semua pembahasan (1 jam)', '📌 Catat semua yang belum paham']},
            'Minggu': {'focus': '🔄 Review + Ask for Help',
                       'activities': ['🔄 Ulangi materi yang paling susah (1 jam)', '🤝 Konsultasi dengan guru/mentor (1 jam)', '😌 Istirahat dan jaga semangat!']},
        },
    }

    # Default plan untuk tipe lain yang belum terdefinisi khusus
    default_plan = {
        'Senin':  {'focus': 'Penalaran Umum + PPU',
                   'activities': ['🧠 PU drilling (1.5 jam)', '📰 PPU wawasan umum (1 jam)', '📊 Review catatan (30 menit)']},
        'Selasa': {'focus': 'Literasi Indonesia + PBM',
                   'activities': ['📚 Literasi Indo (1.5 jam)', '📖 PBM reading practice (1 jam)', '✏️ Latihan menulis (30 menit)']},
        'Rabu':   {'focus': 'PK + Penalaran Matematika',
                   'activities': ['🔢 PK latihan soal (1.5 jam)', '➕ Penalaran Mat (1 jam)', '🧮 Drill soal cerita (30 menit)']},
        'Kamis':  {'focus': 'Literasi Inggris',
                   'activities': ['🌏 Literasi Inggris (1.5 jam)', '📝 Vocab building (1 jam)', '🎧 English content (30 menit)']},
        'Jumat':  {'focus': 'Mixed + Weak Area',
                   'activities': ['🎯 Semua subtes campuran (1.5 jam)', '🔍 Fokus area terlemah (1 jam)', '📋 Update tracker (30 menit)']},
        'Sabtu':  {'focus': '🔥 Full Tryout UTBK',
                   'activities': ['📝 Simulasi tryout 7 subtes (3 jam)', '🔍 Analisis hasil (1 jam)', '📌 Target perbaikan (30 menit)']},
        'Minggu': {'focus': '🧘 Review + Recharge',
                   'activities': ['🔄 Review materi lemah (1.5 jam)', '📅 Planning minggu depan (30 menit)', '😌 Refreshing!']},
    }

    return base_plans.get(learner_type, default_plan)

# ================================================================
# UNIVERSAL TIPS - BAHASA GEN Z
# ================================================================

UNIVERSAL_TIPS = [
    "🎯 **Prioritas cerdas:** Fokus ke subtes yang bobotnya besar dan masih lemah — itu ROI terbesar kamu",
    "📊 **Analisis setiap tryout:** Jangan cuma lihat total skor — bedah per subtes dan per tipe soal",
    "⏰ **Time management is king:** Latihan SELALU pakai timer — kebiasaan ini yang bedain yang lulus dan yang enggak",
    "💪 **Jaga fisik dan mental:** Tidur 7-8 jam itu WAJIB — otak gak bisa optimal kalau kamu kurang tidur",
    "🧠 **Active Recall > Pasif baca:** Test diri sendiri setelah belajar, bukan cuma baca ulang",
    "📚 **Cheat sheet per topik:** Bikin rangkuman 1 halaman per topik — nanti buat review cepat sebelum hari H",
    "👥 **Diskusi soal susah:** Bahas soal yang gak bisa dikerjain bareng teman atau guru — insight-nya beda banget",
    "🌱 **Growth mindset:** Nilai jelek = feedback, bukan kegagalan — setiap tryout adalah data buat improve",
]

# ================================================================
# MAIN FUNCTION
# ================================================================

def generate_study_plan(learner_type, dimension_scores, gap_analysis):
    """
    Generate personalized study recommendations
    Returns dict dengan study methods, time allocation, weekly plan, tips
    """

    recommendations = {
        'study_methods': [],
        'time_allocation': {},
        'weekly_plan': {},
        'focus_areas': [],
        'tips': []
    }

    # ── Study Methods ──────────────────────────────────────────
    recommendations['study_methods'] = STUDY_METHODS.get(
        learner_type, STUDY_METHODS["Growing Learner"]
    )

    # ── Time Allocation (7 subtes) ─────────────────────────────
    base_allocation = TIME_ALLOCATION.get(
        learner_type, TIME_ALLOCATION["Growing Learner"]
    ).copy()

    # Dynamic adjustment: tambah porsi untuk subtes terlemah
    weakest = gap_analysis.get('weakest_area', '')
    weakest_mapped = _map_subtest_name(weakest)
    if weakest_mapped and weakest_mapped in base_allocation:
        # Kurangi subtes terkuat, tambah ke terlemah
        strongest = gap_analysis.get('strongest_area', '')
        strongest_mapped = _map_subtest_name(strongest)
        if strongest_mapped and strongest_mapped in base_allocation:
            shift = 5  # geser 5%
            base_allocation[weakest_mapped] = min(base_allocation[weakest_mapped] + shift, 30)
            base_allocation[strongest_mapped] = max(base_allocation[strongest_mapped] - shift, 5)

    recommendations['time_allocation'] = base_allocation

    # ── Weekly Plan ────────────────────────────────────────────
    recommendations['weekly_plan'] = get_weekly_plan(
        learner_type, gap_analysis.get('weakest_area', '')
    )

    # ── Focus Areas ────────────────────────────────────────────
    recommendations['focus_areas'] = _get_focus_areas(learner_type)

    # ── Tips: Universal + Tips spesifik per subtes terlemah ───
    tips = UNIVERSAL_TIPS.copy()

    # Tambahkan tips spesifik untuk 3 subtes dengan gap terbesar
    subtest_gaps = gap_analysis.get('subtest_gaps', {})
    if subtest_gaps:
        # Urutkan dari gap terbesar
        sorted_subs = sorted(subtest_gaps.items(), key=lambda x: x[1], reverse=True)
        for sub_name, _ in sorted_subs[:3]:
            mapped = _map_subtest_name(sub_name)
            if mapped and mapped in TIPS_PER_SUBTES:
                tips.extend(TIPS_PER_SUBTES[mapped])
    else:
        # Fallback: tambahkan semua tips subtes
        tips.extend(TIPS_PER_SUBTES.get('Penalaran Umum', []))
        tips.extend(TIPS_PER_SUBTES.get('Literasi Indonesia', []))
        tips.extend(TIPS_PER_SUBTES.get('Penalaran Matematika', []))

    recommendations['tips'] = tips

    return recommendations


def _map_subtest_name(raw_name):
    """Map berbagai format nama subtes ke format standar"""
    mapping = {
        # Format dari gap_analysis (key dari current_scores di app.py)
        'PU':               'Penalaran Umum',
        'PPU':              'Pengetahuan & Pemahaman Umum',
        'PBM':              'Pemahaman Bacaan & Menulis',
        'PK':               'Pengetahuan Kuantitatif',
        'Literasi Indo':    'Literasi Indonesia',
        'Literasi Inggris': 'Literasi Inggris',
        'Penalaran Mat':    'Penalaran Matematika',
        # Format lengkap (kalau sudah mapped)
        'Penalaran Umum':               'Penalaran Umum',
        'Pengetahuan & Pemahaman Umum': 'Pengetahuan & Pemahaman Umum',
        'Pemahaman Bacaan & Menulis':   'Pemahaman Bacaan & Menulis',
        'Pengetahuan Kuantitatif':      'Pengetahuan Kuantitatif',
        'Literasi Indonesia':           'Literasi Indonesia',
        'Literasi Inggris':             'Literasi Inggris',
        'Penalaran Matematika':         'Penalaran Matematika',
    }
    return mapping.get(raw_name, None)


def _get_focus_areas(learner_type):
    """Return 3-4 focus areas berdasarkan learner type"""
    focus_map = {
        "Strategic Achiever": [
            "🏆 Maintain momentum dan konsistensi — jangan lengah di puncak",
            "🔬 Challenge diri dengan prediksi soal terbaru dan HOTS",
            "🤝 Share knowledge ke teman — mengajar adalah belajar terdalam",
            "📊 Analisis mendalam setiap penurunan skor, sekecil apapun",
        ],
        "Diligent Scholar": [
            "⚡ Tingkatkan kecepatan tanpa mengorbankan akurasi",
            "🎨 Variasi metode belajar agar tidak monoton dan burnout",
            "⚖️ Balance antara quality dan quantity latihan soal",
            "📈 Push diri ke level berikutnya — konsistensi kamu sudah bagus!",
        ],
        "Fast Learner": [
            "🎯 Improve konsistensi dan kedisiplinan — ini weak point utama",
            "🔬 Depth over breadth — kuasai betul-betul satu topik",
            "⚠️ Jangan skip fundamentals meski terlihat mudah",
            "📅 Buat jadwal yang rigid dan patuhi — kamu butuh struktur",
        ],
        "Resilient Fighter": [
            "📚 Improve study techniques — kerja keras aja gak cukup, harus cerdas",
            "🏗️ Build strong foundation di setiap subtes dari nol",
            "💡 Leverage mental strength — tapi juga upgrade smart strategy",
            "📈 Tracking progress visual untuk boost motivasi",
        ],
        "Growing Learner": [
            "📆 Build consistency dengan habit tracker harian",
            "🏗️ Focus on fundamentals — jangan buru-buru naik level",
            "👥 Cari komunitas belajar yang supportif",
            "🌱 Nikmati proses — growth itu gradual, bukan instan",
        ],
        "Inconsistent Talent": [
            "🔥 Build consistency sebagai priority #1 — ini game changer kamu",
            "📵 Identify dan eliminate distraction utama",
            "📋 Create structured routine yang gak bisa di-skip",
            "🤝 Cari accountability partner yang bisa saling jaga",
        ],
        "Methodical Planner": [
            "⚡ Action speaks louder than plans — eksekusi lebih penting dari planning sempurna",
            "🔄 Be flexible — rigid terlalu tinggi bisa backfire",
            "📊 Trust your system — kamu udah punya fondasi yang bagus",
            "🎯 Focus on execution consistency, bukan planning perfectionism",
        ],
        "Needs Support": [
            "🤝 Seek help actively — minta bantuan bukan kelemahan, itu kecerdasan",
            "🔤 Start from absolute basics — tanpa fondasi, semua runtuh",
            "🏆 Celebrate every small win — sekecil apapun, itu progress nyata",
            "📅 Strict routine adalah satu-satunya jalan — discipline saves lives",
        ],
    }
    return focus_map.get(learner_type, focus_map["Growing Learner"])


# ================================================================
# MILESTONE GENERATOR
# ================================================================

def generate_milestones(gap_analysis, months_to_utbk=4):
    """
    Generate milestone timeline menuju UTBK
    Dengan breakdown per subtes yang lebih spesifik
    """
    total_gap = gap_analysis.get('total_gap', 200)
    weakest = gap_analysis.get('weakest_area', 'semua subtes')
    weakest_label = _map_subtest_name(weakest) or weakest

    milestone_templates = [
        {
            'month': 1,
            'title': '🌱 Foundation Building',
            'target': f'Kuasai 70% materi dasar semua subtes — prioritas utama: {weakest_label}',
            'score_target': f'Naik +{max(int(total_gap * 0.2), 20)} poin dari baseline',
            'action': (
                'Pelajari konsep fundamental semua subtes · '
                'Latihan soal level mudah-sedang · '
                'Identifikasi pola kesalahan paling sering'
            ),
            'focus': '🎯 Understanding > Speed — pahami dulu, ngebut belakangan',
            'progress': 25,
            'subtes_target': {
                'PU': 'Kuasai pola dasar silogisme & analogi',
                'PPU': 'Baca 1 artikel wawasan umum per hari',
                'PBM': 'Latihan baca teks 300 kata + soal',
                'PK': 'Kuasai operasi bilangan, rasio, persen',
                'Literasi Indo': 'Identifikasi ide pokok tiap paragraf',
                'Literasi Inggris': 'Hafal 10 kosakata akademik per hari',
                'Penalaran Mat': 'Kuasai aljabar dan geometri dasar',
            }
        },
        {
            'month': 2,
            'title': '📈 Skill Development',
            'target': 'Skor tryout naik 50–100 poin dari baseline, drilling intensif dimulai',
            'score_target': f'Naik +{max(int(total_gap * 0.5), 50)} poin dari baseline',
            'action': (
                'Drilling soal sedang-sulit · '
                'Tryout mingguan wajib · '
                'Analisis error log setiap tryout'
            ),
            'focus': '💪 Practice makes perfect — kuantitas soal dinaikkan',
            'progress': 50,
            'subtes_target': {
                'PU': 'Target 70% akurasi soal sedang',
                'PPU': 'Kuasai tema IPA, IPS, seni budaya',
                'PBM': 'Speed baca 400 kata dalam 4 menit',
                'PK': 'Kuasai interpretasi grafik dan tabel',
                'Literasi Indo': 'Latihan soal koherensi dan perbaikan kalimat',
                'Literasi Inggris': 'Bisa jawab 60% soal dalam batas waktu',
                'Penalaran Mat': 'Kuasai statistika dan logika matematika',
            }
        },
        {
            'month': 3,
            'title': '⚡ Excellence Training',
            'target': 'Skor tryout tembus 80% dari target akhir, fokus pada weak areas tersisa',
            'score_target': f'Naik +{max(int(total_gap * 0.8), 80)} poin dari baseline',
            'action': (
                f'Intensif di {weakest_label} · '
                'Simulasi kondisi ujian nyata · '
                'Optimasi strategi pengerjaan tiap subtes'
            ),
            'focus': '🔬 Refine & optimize — kualitas di atas kuantitas',
            'progress': 75,
            'subtes_target': {
                'PU': 'Target 80% akurasi, selesai dalam waktu',
                'PPU': '85% akurasi soal wawasan umum',
                'PBM': 'Bisa handle teks kompleks dan argumentatif',
                'PK': '80% akurasi soal data dan kuantitatif',
                'Literasi Indo': '80% akurasi termasuk soal EYD dan ejaan',
                'Literasi Inggris': '75% akurasi soal reading comprehension',
                'Penalaran Mat': '75% akurasi soal cerita dan logika',
            }
        },
        {
            'month': 4,
            'title': '🏆 Final Sprint',
            'target': 'Capai atau lewati target skor — mental sekuat baja, strategi setajam pedang',
            'score_target': '🎯 Target ACHIEVED — full confidence mode!',
            'action': (
                'Final drilling HOTS semua subtes · '
                'Tryout intensif 3x per minggu · '
                'Mental preparation dan manajemen stres · '
                'Simulasi kondisi hari-H'
            ),
            'focus': '🔥 Peak performance — ini saatnya panen dari semua kerja keras!',
            'progress': 100,
            'subtes_target': {
                'PU': 'Full speed, target near-perfect',
                'PPU': 'Semua topik dikuasai, no gap',
                'PBM': 'Teks apapun bisa diselesaikan dalam waktu',
                'PK': 'Akurasi dan kecepatan maksimal',
                'Literasi Indo': 'Akurasi 85%+ konsisten',
                'Literasi Inggris': 'Confident di semua tipe soal',
                'Penalaran Mat': 'Semua tipe soal bisa ditangani',
            }
        },
    ]

    return milestone_templates[:months_to_utbk]