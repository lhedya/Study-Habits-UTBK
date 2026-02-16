"""
Generate personalized study recommendations
"""

def generate_study_plan(learner_type, dimension_scores, gap_analysis):
    """
    Generate personalized study recommendations
    
    Returns:
    - dict dengan study methods, time allocation, weekly plan, tips
    """
    
    recommendations = {
        'study_methods': [],
        'time_allocation': {},
        'weekly_plan': {},
        'focus_areas': [],
        'tips': []
    }
    
    # Rekomendasi berdasarkan learner type
    if learner_type == "Strategic Achiever":
        recommendations['study_methods'] = [
            "Fokus pada drilling soal HOTS level tinggi",
            "Ikuti tryout berkala setiap minggu untuk maintain performa",
            "Analisis mendalam setiap kesalahan dengan error log",
            "Buat bank soal sulit yang pernah salah untuk review berkala"
        ]
        recommendations['time_allocation'] = {
            'TPS': 30,
            'Literasi Indonesia': 20,
            'Literasi Inggris': 25,
            'Penalaran Matematika': 25
        }
        recommendations['focus_areas'] = [
            "Maintain momentum dan konsistensi",
            "Challenge diri dengan prediksi soal terbaru",
            "Share knowledge untuk reinforce understanding"
        ]
        
    elif learner_type == "Diligent Scholar":
        recommendations['study_methods'] = [
            "Pertahankan konsistensi belajar harian yang sudah bagus",
            "Tingkatkan efisiensi dengan teknik Pomodoro (25 menit fokus + 5 menit break)",
            "Buat jadwal detail dengan time blocking per topik",
            "Fokus pada pemahaman konsep mendalam, bukan sekadar hafalan"
        ]
        recommendations['time_allocation'] = {
            'TPS': 25,
            'Literasi Indonesia': 25,
            'Literasi Inggris': 25,
            'Penalaran Matematika': 25
        }
        recommendations['focus_areas'] = [
            "Tingkatkan kecepatan tanpa mengorbankan akurasi",
            "Variasi metode belajar agar tidak monoton",
            "Balance antara quality dan quantity"
        ]
        
    elif learner_type == "Fast Learner":
        recommendations['study_methods'] = [
            "Manfaatkan kecepatan belajar dengan ekspos ke variasi soal luas",
            "Challenge diri dengan soal olimpiade atau beyond UTBK",
            "Gunakan Feynman Technique - ajarkan teman untuk solidify understanding",
            "Explore materi tambahan untuk memperdalam wawasan"
        ]
        recommendations['time_allocation'] = {
            'TPS': 35,
            'Literasi Indonesia': 20,
            'Literasi Inggris': 25,
            'Penalaran Matematika': 20
        }
        recommendations['focus_areas'] = [
            "Improve konsistensi dan kedisiplinan",
            "Depth over breadth - kuasai benar-benar",
            "Jangan skip fundamentals meski terlihat mudah"
        ]
        
    elif learner_type == "Resilient Fighter":
        recommendations['study_methods'] = [
            "Manfaatkan mental yang kuat untuk drilling intensif tanpa burnout",
            "Fokus pada penguasaan fundamental - bangun fondasi kuat",
            "Buat mind map untuk setiap topik agar mudah di-recall",
            "Konsisten tryout untuk tracking progress dan build confidence"
        ]
        recommendations['time_allocation'] = {
            'TPS': 20,
            'Literasi Indonesia': 25,
            'Literasi Inggris': 30,
            'Penalaran Matematika': 25
        }
        recommendations['focus_areas'] = [
            "Improve study techniques dan efficiency",
            "Build strong foundation di setiap subtes",
            "Leverage mental strength untuk push harder"
        ]
        
    elif learner_type == "Growing Learner":
        recommendations['study_methods'] = [
            "Mulai dari materi dasar - bangun fondasi yang kuat dulu",
            "Belajar dengan video pembelajaran interaktif (YouTube, Zenius, Ruangguru)",
            "Gabung study group untuk motivasi dan peer learning",
            "Set target kecil yang realistis dan rayakan setiap pencapaian"
        ]
        recommendations['time_allocation'] = {
            'TPS': 25,
            'Literasi Indonesia': 25,
            'Literasi Inggris': 25,
            'Penalaran Matematika': 25
        }
        recommendations['focus_areas'] = [
            "Build consistency dengan habit tracker",
            "Focus on fundamentals terlebih dahulu",
            "Jangan buru-buru, step by step"
        ]
        
    elif learner_type == "Inconsistent Talent":
        recommendations['study_methods'] = [
            "Buat habit tracker visual untuk monitor konsistensi harian",
            "Gunakan accountability partner atau study buddy",
            "Set reminder dan reward system untuk setiap milestone",
            "Fokus pada kualitas waktu, bukan kuantitas - short but intense"
        ]
        recommendations['time_allocation'] = {
            'TPS': 30,
            'Literasi Indonesia': 20,
            'Literasi Inggris': 25,
            'Penalaran Matematika': 25
        }
        recommendations['focus_areas'] = [
            "Build consistency sebagai priority #1",
            "Identify dan eliminate distractions",
            "Create structured routine"
        ]
        
    elif learner_type == "Methodical Planner":
        recommendations['study_methods'] = [
            "Leverage planning skill untuk buat master timeline hingga UTBK",
            "Time-based practice untuk simulasi kondisi ujian sebenarnya",
            "Analisis statistik progress bulanan dengan detailed tracking",
            "Balance planning dengan execution - jangan overthink"
        ]
        recommendations['time_allocation'] = {
            'TPS': 30,
            'Literasi Indonesia': 20,
            'Literasi Inggris': 25,
            'Penalaran Matematika': 25
        }
        recommendations['focus_areas'] = [
            "Improve execution consistency",
            "Be flexible dengan planning - adjust bila perlu",
            "Action speaks louder than plans"
        ]
        
    else:  # Needs Support
        recommendations['study_methods'] = [
            "Cari mentor atau guru pembimbing untuk guidance intensif",
            "Mulai dengan materi paling dasar - jangan skip fundamentals",
            "Belajar 1-on-1 atau kelompok kecil untuk fokus lebih baik",
            "Fokus pada 1-2 subtes dulu sampai mahir, baru expand"
        ]
        recommendations['time_allocation'] = {
            'TPS': 20,
            'Literasi Indonesia': 30,
            'Literasi Inggris': 30,
            'Penalaran Matematika': 20
        }
        recommendations['focus_areas'] = [
            "Seek help - jangan malu bertanya",
            "Start from absolute basics",
            "Small wins every day"
        ]
    
    # Weekly Plan Template
    recommendations['weekly_plan'] = {
        'Senin': {
            'activities': ['TPS - Penalaran Umum (2 jam)', 'Literasi Indonesia (1 jam)'],
            'focus': 'Membangun logika dan pemahaman bacaan'
        },
        'Selasa': {
            'activities': ['Penalaran Matematika (2 jam)', 'Literasi Inggris (1 jam)'],
            'focus': 'Latihan soal kuantitatif dan reading comprehension'
        },
        'Rabu': {
            'activities': ['TPS - Pengetahuan Kuantitatif (2 jam)', 'Review kesalahan (1 jam)'],
            'focus': 'Drill soal angka dan analisis error'
        },
        'Kamis': {
            'activities': ['Literasi Indonesia (1.5 jam)', 'Literasi Inggris (1.5 jam)'],
            'focus': 'Intensive reading practice'
        },
        'Jumat': {
            'activities': ['Penalaran Matematika (2 jam)', 'TPS Mix (1 jam)'],
            'focus': 'Problem solving dan latihan campuran'
        },
        'Sabtu': {
            'activities': ['Tryout Simulasi (3 jam)', 'Analisis hasil (1 jam)'],
            'focus': 'Full simulation dan evaluasi'
        },
        'Minggu': {
            'activities': ['Review materi lemah (2 jam)', 'Refreshing & Planning (1 jam)'],
            'focus': 'Perbaikan weak areas dan persiapan minggu depan'
        }
    }
    
    # General Tips (Universal)
    recommendations['tips'] = [
        "🎯 Prioritaskan materi dengan bobot besar di UTBK",
        "📊 Analisis setiap hasil tryout untuk identifikasi pola kesalahan",
        "⏰ Latihan time management dengan timer saat latihan soal",
        "💪 Jaga kesehatan fisik dan mental - tidur cukup, makan bergizi",
        "🧠 Gunakan teknik active recall dan spaced repetition",
        "📚 Buat catatan ringkas (cheat sheet) untuk review cepat",
        "👥 Diskusi soal sulit dengan teman atau mentor",
        "🎨 Gunakan mind map atau diagram untuk visualisasi konsep"
    ]
    
    return recommendations

def generate_milestones(gap_analysis, months_to_utbk=4):
    """
    Generate milestone timeline hingga UTBK
    
    Returns:
    - list of milestone dicts
    """
    total_gap = gap_analysis['total_gap']
    
    milestones = []
    
    for month in range(1, months_to_utbk + 1):
        progress_target = (month / months_to_utbk) * 100
        
        if month == 1:
            milestones.append({
                'month': 1,
                'title': 'Foundation Building',
                'target': 'Menguasai 70% materi dasar semua subtes',
                'score_target': f'+{int(total_gap * 0.2)} poin dari baseline',
                'action': 'Belajar konsep fundamental + latihan soal mudah-sedang',
                'focus': 'Understanding > Speed'
            })
        elif month == 2:
            milestones.append({
                'month': 2,
                'title': 'Skill Development',
                'target': 'Skor tryout naik 50-100 poin dari baseline',
                'score_target': f'+{int(total_gap * 0.5)} poin dari baseline',
                'action': 'Drilling soal sedang-sulit + tryout setiap minggu',
                'focus': 'Practice makes perfect'
            })
        elif month == 3:
            milestones.append({
                'month': 3,
                'title': 'Excellence Training',
                'target': 'Skor tryout mencapai 80% dari target akhir',
                'score_target': f'+{int(total_gap * 0.8)} poin dari baseline',
                'action': 'Fokus pada weak areas + strategi pengerjaan optimal',
                'focus': 'Refine & optimize'
            })
        else:
            milestones.append({
                'month': 4,
                'title': 'Final Sprint',
                'target': 'Mencapai atau melampaui target skor',
                'score_target': 'Target ACHIEVED!',
                'action': 'Final drilling + mental preparation + tryout intensif',
                'focus': 'Peak performance'
            })
    
    return milestones