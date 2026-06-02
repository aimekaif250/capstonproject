# =====================================================
# Cancer Risk Prediction Web Application
# Machine Learning-Based System for Breast and Cervical Cancer Risk Prediction
# =====================================================

from flask import Flask, render_template, request, jsonify
import os, pickle, logging, csv
import traceback
import numpy as np

# Initialize Flask application
app = Flask(__name__)

# Set up paths for models
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')

def load_model(*filenames):
    for filename in filenames:
        path = os.path.join(MODEL_PATH, filename)
        try:
            with open(path, "rb") as f:
                model = pickle.load(f)
            logging.info(f"Loaded model: {filename}")
            return model
        except Exception as e:
            logging.warning(f"Could not load model {filename}: {e}")
    return None

# Load pre-trained machine learning models (fallback to None if missing)
breast_model = load_model("breast_model.pkl", "breast_cancer_model.pkl")
cervical_model = load_model("cervical_cancer_model.pkl", "cervical_rf_model.pkl")


# =====================================================
# BREAST CANCER PREDICTION CONFIGURATION
# =====================================================

# Full list of 30 features in the exact order expected by the model
# (Based on Breast Cancer Wisconsin dataset)
BREAST_CANCER_FEATURES = [
    'radius_mean',           # 1 - User input
    'texture_mean',          # 2 - User input
    'perimeter_mean',        # 3 - User input
    'area_mean',             # 4 - User input
    'smoothness_mean',       # 5 - Auto-filled
    'compactness_mean',      # 6 - Auto-filled
    'concavity_mean',        # 7 - User input
    'concave points_mean',   # 8 - Auto-filled
    'symmetry_mean',         # 9 - User input
    'fractal_dimension_mean',# 10 - Auto-filled
    'radius_se',             # 11 - Auto-filled
    'texture_se',            # 12 - Auto-filled
    'perimeter_se',          # 13 - Auto-filled
    'area_se',               # 14 - Auto-filled
    'smoothness_se',         # 15 - Auto-filled
    'compactness_se',         # 16 - Auto-filled
    'concavity_se',          # 17 - Auto-filled
    'concave points_se',     # 18 - Auto-filled
    'symmetry_se',           # 19 - Auto-filled
    'fractal_dimension_se',  # 20 - Auto-filled
    'radius_worst',          # 21 - Auto-filled
    'texture_worst',         # 22 - Auto-filled
    'perimeter_worst',       # 23 - Auto-filled
    'area_worst',            # 24 - Auto-filled
    'smoothness_worst',      # 25 - Auto-filled
    'compactness_worst',     # 26 - Auto-filled
    'concavity_worst',       # 27 - Auto-filled
    'concave points_worst',  # 28 - Auto-filled
    'symmetry_worst',        # 29 - Auto-filled
    'fractal_dimension_worst'# 30 - Auto-filled
]

# User-input features (6 features collected from web form)
USER_INPUT_FEATURES = [
    'radius_mean',
    'texture_mean',
    'perimeter_mean',
    'area_mean',
    'concavity_mean',
    'symmetry_mean'
]

# Auto-filled features (24 features with default mean values)
AUTO_FILLED_FEATURES = [
    'smoothness_mean',
    'compactness_mean',
    'concave points_mean',
    'fractal_dimension_mean',
    'radius_se',
    'texture_se',
    'perimeter_se',
    'area_se',
    'smoothness_se',
    'compactness_se',
    'concavity_se',
    'concave points_se',
    'symmetry_se',
    'fractal_dimension_se',
    'radius_worst',
    'texture_worst',
    'perimeter_worst',
    'area_worst',
    'smoothness_worst',
    'compactness_worst',
    'concavity_worst',
    'concave points_worst',
    'symmetry_worst',
    'fractal_dimension_worst'
]

CERVICAL_CANCER_FEATURES = [
    'Age',
    'Number of sexual partners',
    'First sexual intercourse',
    'Num of pregnancies',
    'Smokes',
    'Smokes (years)',
    'Smokes (packs/year)',
    'Hormonal Contraceptives',
    'Hormonal Contraceptives (years)',
    'IUD',
    'IUD (years)',
    'STDs',
    'STDs (number)',
    'STDs:condylomatosis',
    'STDs:cervical condylomatosis',
    'STDs:vaginal condylomatosis',
    'STDs:vulvo-perineal condylomatosis',
    'STDs:syphilis',
    'STDs:pelvic inflammatory disease',
    'STDs:genital herpes',
    'STDs:molluscum contagiosum',
    'STDs:AIDS',
    'STDs:HIV',
    'STDs:Hepatitis B',
    'STDs:HPV',
    'STDs: Number of diagnosis',
    'STDs: Time since first diagnosis',
    'STDs: Time since last diagnosis',
    'Dx:Cancer',
    'Dx:CIN',
    'Dx:HPV',
    'Dx',
    'Hinselmann',
    'Schiller',
    'Citology'
]

CERVICAL_USER_INPUTS = {
    'age': 'Age',
    'hpv': 'STDs:HPV',
    'smoking': 'Smokes',
    'pregnancies': 'Num of pregnancies',
    'std_history': 'STDs'
}


def load_cervical_defaults():
    defaults = {feature: 0.0 for feature in CERVICAL_CANCER_FEATURES}
    counts = {feature: 0 for feature in CERVICAL_CANCER_FEATURES}
    path = os.path.join(MODEL_PATH, 'risk_factors_cervical_cancer.csv')

    try:
        with open(path, newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                for feature in CERVICAL_CANCER_FEATURES:
                    value = row.get(feature)
                    if value in (None, '', '?'):
                        continue
                    defaults[feature] += float(value)
                    counts[feature] += 1
    except Exception as e:
        logging.warning(f"Could not load cervical defaults: {e}")
        return defaults

    for feature, count in counts.items():
        if count:
            defaults[feature] = defaults[feature] / count

    return defaults

# Default mean values for auto-filled features
# These are the mean values from the Breast Cancer Wisconsin dataset
DEFAULT_VALUES = {
    'smoothness_mean': 0.09636,
    'compactness_mean': 0.10434,
    'concave points_mean': 0.04892,
    'fractal_dimension_mean': 0.06280,
    'radius_se': 0.40517,
    'texture_se': 1.21685,
    'perimeter_se': 2.86606,
    'area_se': 40.33708,
    'smoothness_se': 0.00704,
    'compactness_se': 0.02548,
    'concavity_se': 0.03189,
    'concave points_se': 0.01180,
    'symmetry_se': 0.02054,
    'fractal_dimension_se': 0.00379,
    'radius_worst': 16.26919,
    'texture_worst': 25.67722,
    'perimeter_worst': 107.26121,
    'area_worst': 880.58313,
    'smoothness_worst': 0.13237,
    'compactness_worst': 0.25427,
    'concavity_worst': 0.27219,
    'concave points_worst': 0.11461,
    'symmetry_worst': 0.29008,
    'fractal_dimension_worst': 0.08395
}

CERVICAL_DEFAULT_VALUES = load_cervical_defaults()

@app.route('/')
def home():
    """
    Home page route
    Displays welcome page with cancer type selection
    """
    return render_template('index.html')


@app.route('/breast')
def breast_form():
    """
    Breast cancer prediction form page
    Displays input form for breast cancer features
    """
    return render_template('breast.html')


@app.route('/cervical')
def cervical_form():
    """
    Cervical cancer prediction form page
    Displays input form for cervical cancer features
    """
    return render_template('cervical.html')


@app.route('/predict/breast', methods=['POST'])
def predict_breast():
    """
    Predict breast cancer risk using 6 user inputs + 24 default values
    
    Expected JSON input (6 features):
    {
        'radius_mean': float,
        'texture_mean': float,
        'perimeter_mean': float,
        'area_mean': float,
        'concavity_mean': float,
        'symmetry_mean': float
    }
    
    Returns prediction result and probability
    """
    try:
        # Check if model is loaded
        if breast_model is None:
            return jsonify({
                'success': False,
                'error': 'Breast cancer model not loaded. Please check model file.'
            }), 500
        
        # Get data from request
        data = request.get_json()
        
        # Validate and extract user input features
        user_inputs = {}
        for feature in USER_INPUT_FEATURES:
            value = data.get(feature)
            if value is None:
                return jsonify({
                    'success': False,
                    'error': f'Missing required input: {feature}'
                }), 400
            
            # Validate numeric input
            try:
                user_inputs[feature] = float(value)
            except (ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'error': f'Invalid numeric value for {feature}: {value}'
                }), 400
        
        # Build complete feature vector (30 features)
        features = []
        for feature_name in BREAST_CANCER_FEATURES:
            if feature_name in user_inputs:
                # Use user input
                features.append(user_inputs[feature_name])
            else:
                # Use default value
                features.append(DEFAULT_VALUES[feature_name])
        
        # Convert to numpy array and reshape for model prediction (1, 30)
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = breast_model.predict(features_array)[0]
        probability = breast_model.predict_proba(features_array)[0]
        
        # Map prediction to readable result
        result = "Malignant (Cancer)" if prediction == 1 else "Benign (Non-Cancerous)"
        confidence = max(probability) * 100
        
        return jsonify({
            'success': True,
            'prediction': result,
            'confidence': f"{confidence:.2f}%",
            'probability_benign': f"{probability[0] * 100:.2f}%",
            'probability_malignant': f"{probability[1] * 100:.2f}%",
            'cancer_type': 'Breast Cancer',
            'input_features_used': len(user_inputs),
            'total_features': len(features)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input value: {str(e)}'
        }), 400
    except Exception as e:
        print(f"Error in breast prediction: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 500


@app.route('/predict/cervical', methods=['POST'])
def predict_cervical():
    """
    Predict cervical cancer risk
    
    Expected JSON input:
    {
        'age': int,
        'hpv': int (0 or 1),
        'smoking': int (0 or 1),
        'pregnancies': int,
        'std_history': int (0 or 1)
    }
    
    Returns prediction result and probability
    """
    try:
        # Check if model is loaded
        if cervical_model is None:
            return jsonify({
                'success': False,
                'error': 'Cervical cancer model not loaded. Please check model file.'
            }), 500
        
        # Get data from request
        data = request.get_json()
        
        user_inputs = {}
        for input_name, feature_name in CERVICAL_USER_INPUTS.items():
            value = data.get(input_name)
            if value is None:
                return jsonify({
                    'success': False,
                    'error': f'Missing required input: {input_name}'
                }), 400
            user_inputs[feature_name] = float(value)
        
        # Build complete feature vector (35 features)
        features = []
        for feature_name in CERVICAL_CANCER_FEATURES:
            if feature_name in user_inputs:
                features.append(user_inputs[feature_name])
            else:
                features.append(CERVICAL_DEFAULT_VALUES[feature_name])
        
        # Convert to numpy array and reshape for model prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = cervical_model.predict(features_array)[0]
        probability = cervical_model.predict_proba(features_array)[0]
        
        # Map prediction to readable result
        result = "Cancer Risk Detected" if prediction == 1 else "No Cancer Risk"
        confidence = max(probability) * 100
        
        return jsonify({
            'success': True,
            'prediction': result,
            'confidence': f"{confidence:.2f}%",
            'probability_no_cancer': f"{probability[0] * 100:.2f}%",
            'probability_cancer': f"{probability[1] * 100:.2f}%",
            'cancer_type': 'Cervical Cancer',
            'input_features_used': len(user_inputs),
            'total_features': len(features)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input value: {str(e)}'
        }), 400
    except Exception as e:
        print(f"Error in cervical prediction: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 500


@app.route('/result', methods=['POST', 'GET'])
def result_page():
    """
    Result page route
    Displays prediction results
    """
    return render_template('result.html')


# =====================================================
# ERROR HANDLING
# =====================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    # Listen on all interfaces so localhost and network access both work
    app.run(host="0.0.0.0", port=5000, debug=True)
