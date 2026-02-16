"""
Preprocessing utilities untuk UTBK Recommendation System
"""

import pandas as pd
import numpy as np
import pickle
import json

def load_mappings(filepath='models/recommendation_mappings.pkl'):
    """Load survey answer mappings"""
    with open(filepath, 'rb') as f:
        mappings = pickle.load(f)
    return mappings

def encode_survey_responses(responses_dict, mappings):
    """
    Encode survey responses dari text ke numeric
    
    Parameters:
    - responses_dict: dict dengan key Q1-Q52 dan value jawaban siswa
    - mappings: dict mapping dari load_mappings()
    
    Returns:
    - encoded_dict: dict dengan encoded values
    """
    encoded = {}
    
    for question, answer in responses_dict.items():
        if question in mappings:
            encoded[f'{question}_encoded'] = mappings[question].get(answer, 0)
        else:
            encoded[f'{question}_encoded'] = 0
            
    return encoded

def calculate_dimension_scores(encoded_responses):
    """
    Hitung skor per dimensi (0-100)
    
    Parameters:
    - encoded_responses: dict dari encode_survey_responses()
    
    Returns:
    - dict dengan skor per dimensi
    """
    
    # DIMENSI 1: Gaya Belajar (Q1-Q12)
    gaya_belajar_scores = [encoded_responses.get(f'Q{i}_encoded', 0) for i in range(1, 13)]
    max_gaya_belajar = 60
    skor_gaya_belajar = (sum(gaya_belajar_scores) / max_gaya_belajar) * 100
    
    # DIMENSI 2: Konsistensi (Q13-Q22)
    konsistensi_scores = [encoded_responses.get(f'Q{i}_encoded', 0) for i in range(13, 23)]
    max_konsistensi = 50
    skor_konsistensi = (sum(konsistensi_scores) / max_konsistensi) * 100
    
    # DIMENSI 3: Manajemen Waktu (Q23-Q32)
    manajemen_waktu_scores = [encoded_responses.get(f'Q{i}_encoded', 0) for i in range(23, 33)]
    max_manajemen_waktu = 50
    skor_manajemen_waktu = (sum(manajemen_waktu_scores) / max_manajemen_waktu) * 100
    
    # DIMENSI 4: Kesiapan UTBK (Q33-Q44)
    kesiapan_scores = [encoded_responses.get(f'Q{i}_encoded', 0) for i in range(33, 45)]
    max_kesiapan = 60
    skor_kesiapan = (sum(kesiapan_scores) / max_kesiapan) * 100
    
    # DIMENSI 5: Kondisi Psikologis (Q45-Q52)
    psikologis_scores = [encoded_responses.get(f'Q{i}_encoded', 0) for i in range(45, 53)]
    max_psikologis = 40
    skor_psikologis = (sum(psikologis_scores) / max_psikologis) * 100
    
    return {
        'Gaya_Belajar': round(skor_gaya_belajar, 2),
        'Konsistensi': round(skor_konsistensi, 2),
        'Manajemen_Waktu': round(skor_manajemen_waktu, 2),
        'Kesiapan_UTBK': round(skor_kesiapan, 2),
        'Kondisi_Psikologis': round(skor_psikologis, 2)
    }

def prepare_features_for_model(encoded_responses, dimension_scores):
    """
    Prepare feature vector untuk model prediction
    
    Returns:
    - numpy array siap untuk model
    """
    # Gabungkan encoded responses + dimension scores
    all_features = []
    
    # Tambahkan semua Q1-Q52 encoded
    for i in range(1, 53):
        all_features.append(encoded_responses.get(f'Q{i}_encoded', 0))
    
    # Tambahkan dimension scores
    all_features.extend([
        dimension_scores['Gaya_Belajar'],
        dimension_scores['Konsistensi'],
        dimension_scores['Manajemen_Waktu'],
        dimension_scores['Kesiapan_UTBK'],
        dimension_scores['Kondisi_Psikologis']
    ])
    
    return np.array(all_features).reshape(1, -1)

def parse_skor_string(skor_str):
    """
    Parse string skor dari format '500-550' menjadi nilai tengah
    
    Parameters:
    - skor_str: string like '500-550' or '600'
    
    Returns:
    - int: nilai skor
    """
    if '-' in str(skor_str):
        parts = skor_str.split('-')
        return int((int(parts[0]) + int(parts[1])) / 2)
    else:
        try:
            return int(skor_str)
        except:
            return 0

def calculate_gap_analysis(current_scores, target_score):
    """
    Analisis gap antara skor saat ini dengan target
    
    Parameters:
    - current_scores: dict {'TPS': 550, 'Literasi_Indo': 520, ...}
    - target_score: int (total target score)
    
    Returns:
    - dict dengan analisis gap
    """
    total_current = sum(current_scores.values())
    total_gap = target_score - total_current
    
    # Identifikasi area terlemah
    sorted_scores = sorted(current_scores.items(), key=lambda x: x[1])
    weakest_area = sorted_scores[0][0]
    strongest_area = sorted_scores[-1][0]
    
    # Hitung gap per subtes
    avg_per_subtes = target_score / len(current_scores)
    subtes_gaps = {
        subject: round(avg_per_subtes - score, 2)
        for subject, score in current_scores.items()
    }
    
    return {
        'total_current': total_current,
        'total_target': target_score,
        'total_gap': total_gap,
        'gap_percentage': round((total_gap / target_score) * 100, 2),
        'weakest_area': weakest_area,
        'strongest_area': strongest_area,
        'subtes_gaps': subtes_gaps,
        'status': 'On Track' if total_gap <= 100 else 'Needs Improvement' if total_gap <= 200 else 'Critical'
    }