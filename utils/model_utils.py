"""
Model loading and prediction utilities
"""

import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

def load_models():
    """Load all trained models"""
    models = {}
    
    with open('models/kmeans_model.pkl', 'rb') as f:
        models['kmeans'] = pickle.load(f)
    
    with open('models/rf_recommendation_model.pkl', 'rb') as f:
        models['rf'] = pickle.load(f)
    
    with open('models/scaler_clustering.pkl', 'rb') as f:
        models['scaler_clustering'] = pickle.load(f)
    
    with open('models/scaler_rf.pkl', 'rb') as f:
        models['scaler_rf'] = pickle.load(f)
    
    return models

def load_learner_type_descriptions():
    """Load learner type descriptions"""
    try:
        with open('models/learner_types.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Fallback descriptions
        return {
            "Strategic Achiever": {
                "emoji": "🎯",
                "title": "Strategic Achiever",
                "description": "Kamu memiliki performa tinggi di semua dimensi!",
                "strengths": ["Konsistensi tinggi", "Manajemen waktu excellent", "Mental kuat"],
                "focus_areas": ["Maintain momentum", "Challenge diri dengan HOTS", "Share knowledge"]
            },
            "Diligent Scholar": {
                "emoji": "📚",
                "title": "Diligent Scholar",
                "description": "Kamu sangat rajin dan konsisten!",
                "strengths": ["Disiplin tinggi", "Tekun", "Reliable"],
                "focus_areas": ["Efisiensi belajar", "Time management", "Variasi metode"]
            },
            "Fast Learner": {
                "emoji": "🚀",
                "title": "Fast Learner",
                "description": "Kamu cepat menangkap materi baru!",
                "strengths": ["Quick learner", "Adaptif", "High IQ"],
                "focus_areas": ["Konsistensi", "Depth over breadth", "Teaching others"]
            },
            "Resilient Fighter": {
                "emoji": "💪",
                "title": "Resilient Fighter",
                "description": "Mentalmu kuat dan pantang menyerah!",
                "strengths": ["Mental tangguh", "Resilient", "Never give up"],
                "focus_areas": ["Study techniques", "Strong foundation", "Consistent practice"]
            },
            "Growing Learner": {
                "emoji": "🌱",
                "title": "Growing Learner",
                "description": "Kamu dalam tahap perkembangan yang baik!",
                "strengths": ["Growth mindset", "Open to learn", "High potential"],
                "focus_areas": ["Build foundation", "Consistency", "Find rhythm"]
            },
            "Inconsistent Talent": {
                "emoji": "⚡",
                "title": "Inconsistent Talent",
                "description": "Kamu punya kemampuan tinggi tapi perlu lebih konsisten!",
                "strengths": ["High potential", "Quick grasp", "Talented"],
                "focus_areas": ["Build consistency", "Habit tracking", "Accountability"]
            },
            "Methodical Planner": {
                "emoji": "🎓",
                "title": "Methodical Planner",
                "description": "Kamu excellent dalam planning!",
                "strengths": ["Planning expert", "Organized", "Strategic"],
                "focus_areas": ["Execution", "Flexibility", "Balance planning & doing"]
            },
            "Needs Support": {
                "emoji": "🆘",
                "title": "Needs Support",
                "description": "Kamu butuh dukungan ekstra. Jangan ragu minta bantuan!",
                "strengths": ["Aware of gaps", "Ready to improve", "Humble"],
                "focus_areas": ["Seek mentor", "Start from basics", "Small daily wins"]
            }
        }

def predict_learner_type(dimension_scores, models):
    """
    Predict learner type using clustering model
    
    Parameters:
    - dimension_scores: dict dengan 5 dimension scores
    - models: dict dari load_models()
    
    Returns:
    - learner_type: string
    """
    # Prepare features (5 dimension scores)
    features = np.array([
        dimension_scores['Gaya_Belajar'],
        dimension_scores['Konsistensi'],
        dimension_scores['Manajemen_Waktu'],
        dimension_scores['Kesiapan_UTBK'],
        dimension_scores['Kondisi_Psikologis']
    ]).reshape(1, -1)
    
    # Scale features
    features_scaled = models['scaler_clustering'].transform(features)
    
    # Predict cluster
    cluster = models['kmeans'].predict(features_scaled)[0]
    
    # Map cluster to learner type based on scores
    avg_score = np.mean(list(dimension_scores.values()))
    
    if avg_score >= 75:
        return "Strategic Achiever"
    elif dimension_scores['Konsistensi'] >= 70 and dimension_scores['Manajemen_Waktu'] >= 65:
        return "Diligent Scholar"
    elif dimension_scores['Gaya_Belajar'] >= 70 and dimension_scores['Kesiapan_UTBK'] >= 70:
        return "Fast Learner"
    elif dimension_scores['Kondisi_Psikologis'] >= 70:
        return "Resilient Fighter"
    elif 50 <= avg_score < 65:
        return "Growing Learner"
    elif dimension_scores['Kesiapan_UTBK'] >= 65 and dimension_scores['Konsistensi'] < 50:
        return "Inconsistent Talent"
    elif dimension_scores['Manajemen_Waktu'] >= 70:
        return "Methodical Planner"
    else:
        return "Needs Support"