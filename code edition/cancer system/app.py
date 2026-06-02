# =====================================================
# Cancer Risk Prediction Web Application
# Machine Learning-Based System for Breast and Cervical Cancer Risk Prediction
# =====================================================

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os, pickle, logging, csv, sqlite3, json
from datetime import date, timedelta
import traceback
import numpy as np

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'capstone-dev-secret-key')

# Set up paths for models
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = [row[1] for row in db.execute("PRAGMA table_info(users)").fetchall()]
        if 'is_admin' not in columns:
            db.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS prediction_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT NOT NULL,
                cancer_type TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                probability_negative REAL NOT NULL,
                probability_positive REAL NOT NULL,
                input_features_used INTEGER NOT NULL,
                total_features INTEGER NOT NULL,
                inputs_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        admin_count = db.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1").fetchone()[0]
        user_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count and not admin_count:
            db.execute(
                """
                UPDATE users
                SET is_admin = 1
                WHERE id = (
                    SELECT id FROM users ORDER BY created_at ASC, id ASC LIMIT 1
                )
                """
            )
        db.commit()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/predict/'):
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            flash('Please sign in to continue.', 'info')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please sign in to continue.', 'info')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Admin access is required.', 'error')
            return redirect(url_for('home'))
        return view(*args, **kwargs)
    return wrapped_view


@app.context_processor
def inject_current_user():
    return {
        'current_user': session.get('username'),
        'current_is_admin': session.get('is_admin', False)
    }


init_db()

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

# User-input features collected from web form, ordered by model coefficient importance.
USER_INPUT_FEATURES = [
    'radius_se',
    'texture_worst',
    'radius_worst',
    'area_se',
    'area_worst',
    'concave points_mean',
    'concave points_worst',
    'symmetry_worst',
    'concavity_mean',
    'concavity_worst',
    'perimeter_worst',
    'compactness_se'
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
    'schiller': 'Schiller',
    'hinselmann': 'Hinselmann',
    'age': 'Age',
    'first_sexual_intercourse': 'First sexual intercourse',
    'citology': 'Citology',
    'hormonal_contraceptives_years': 'Hormonal Contraceptives (years)',
    'pregnancies': 'Num of pregnancies',
    'sexual_partners': 'Number of sexual partners',
    'dx': 'Dx',
    'smokes_packs_year': 'Smokes (packs/year)',
    'dx_cin': 'Dx:CIN',
    'smokes_years': 'Smokes (years)'
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

def load_breast_defaults():
    defaults = {feature: 0.0 for feature in BREAST_CANCER_FEATURES}
    counts = {feature: 0 for feature in BREAST_CANCER_FEATURES}
    path = os.path.join(MODEL_PATH, 'data.csv')

    try:
        with open(path, newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                for feature in BREAST_CANCER_FEATURES:
                    value = row.get(feature)
                    if value in (None, '', '?'):
                        continue
                    defaults[feature] += float(value)
                    counts[feature] += 1
    except Exception as e:
        logging.warning(f"Could not load breast defaults: {e}")
        return DEFAULT_VALUES

    for feature, count in counts.items():
        if count:
            defaults[feature] = defaults[feature] / count

    return defaults

DEFAULT_VALUES = load_breast_defaults()
CERVICAL_DEFAULT_VALUES = load_cervical_defaults()


def model_positive_label(cancer_type):
    return 'Malignant' if cancer_type == 'Breast Cancer' else 'Cancer risk'


def log_prediction(cancer_type, result, confidence, probabilities, input_features_used, total_features, user_inputs):
    db = get_db()
    db.execute(
        """
        INSERT INTO prediction_reports (
            user_id,
            username,
            cancer_type,
            prediction,
            confidence,
            probability_negative,
            probability_positive,
            input_features_used,
            total_features,
            inputs_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session.get('user_id'),
            session.get('username', 'unknown'),
            cancer_type,
            result,
            float(confidence),
            float(probabilities[0] * 100),
            float(probabilities[1] * 100),
            input_features_used,
            total_features,
            json.dumps(user_inputs, sort_keys=True)
        )
    )
    db.commit()


def get_breast_feature_importance(limit=12):
    model = breast_model
    estimator = getattr(model, 'named_steps', {}).get('logisticregression') if hasattr(model, 'named_steps') else model
    coefficients = getattr(estimator, 'coef_', None)
    if coefficients is None:
        return []

    values = np.abs(coefficients[0])
    ranked = sorted(zip(BREAST_CANCER_FEATURES, values), key=lambda item: item[1], reverse=True)
    max_value = float(ranked[0][1]) if ranked else 1.0
    return [
        {
            'name': name.replace('_', ' ').replace('concave points', 'concave points'),
            'score': float(score),
            'percent': round((float(score) / max_value) * 100, 2) if max_value else 0
        }
        for name, score in ranked[:limit]
    ]


def get_cervical_feature_importance(limit=12):
    values = getattr(cervical_model, 'feature_importances_', None)
    if values is None:
        return []

    ranked = sorted(zip(CERVICAL_CANCER_FEATURES, values), key=lambda item: item[1], reverse=True)
    max_value = float(ranked[0][1]) if ranked else 1.0
    return [
        {
            'name': name,
            'score': float(score),
            'percent': round((float(score) / max_value) * 100, 2) if max_value else 0
        }
        for name, score in ranked[:limit]
    ]


def get_admin_dashboard_data():
    db = get_db()
    rows = db.execute(
        """
        SELECT *
        FROM prediction_reports
        ORDER BY created_at DESC, id DESC
        LIMIT 25
        """
    ).fetchall()

    total = db.execute('SELECT COUNT(*) AS count FROM prediction_reports').fetchone()['count']
    breast_total = db.execute(
        "SELECT COUNT(*) AS count FROM prediction_reports WHERE cancer_type = 'Breast Cancer'"
    ).fetchone()['count']
    cervical_total = db.execute(
        "SELECT COUNT(*) AS count FROM prediction_reports WHERE cancer_type = 'Cervical Cancer'"
    ).fetchone()['count']
    positive_total = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM prediction_reports
        WHERE prediction LIKE '%Malignant%' OR prediction LIKE '%Detected%'
        """
    ).fetchone()['count']

    today = date.today()
    days = [(today - timedelta(days=offset)).isoformat() for offset in range(13, -1, -1)]
    daily_lookup = {
        (row['day'], row['cancer_type']): row['count']
        for row in db.execute(
            """
            SELECT DATE(created_at) AS day, cancer_type, COUNT(*) AS count
            FROM prediction_reports
            WHERE DATE(created_at) >= DATE('now', '-13 days')
            GROUP BY DATE(created_at), cancer_type
            """
        ).fetchall()
    }
    time_series = []
    for day in days:
        breast_count = daily_lookup.get((day, 'Breast Cancer'), 0)
        cervical_count = daily_lookup.get((day, 'Cervical Cancer'), 0)
        time_series.append({
            'day': day,
            'label': day[-5:],
            'breast': breast_count,
            'cervical': cervical_count,
            'total': breast_count + cervical_count
        })
    max_series = max([row['total'] for row in time_series], default=1)
    for row in time_series:
        row['breast_percent'] = round((row['breast'] / max_series) * 100, 2) if max_series else 0
        row['cervical_percent'] = round((row['cervical'] / max_series) * 100, 2) if max_series else 0
        row['total_percent'] = round((row['total'] / max_series) * 100, 2) if max_series else 0
    chart_width = 640
    chart_height = 220
    chart_pad = 18

    def build_chart_points(key):
        points = []
        usable_width = chart_width - (chart_pad * 2)
        usable_height = chart_height - (chart_pad * 2)
        denominator = max(len(time_series) - 1, 1)
        for index, row in enumerate(time_series):
            x = chart_pad + ((index / denominator) * usable_width)
            y = chart_pad + (usable_height - ((row[key] / max_series) * usable_height if max_series else 0))
            points.append({
                'x': round(x, 2),
                'y': round(y, 2),
                'value': row[key],
                'label': row['label']
            })
        return points

    chart = {
        'width': chart_width,
        'height': chart_height,
        'max': max_series,
        'total_points': build_chart_points('total'),
        'breast_points': build_chart_points('breast'),
        'cervical_points': build_chart_points('cervical')
    }
    for key in ('total_points', 'breast_points', 'cervical_points'):
        chart[key + '_attr'] = ' '.join([f"{point['x']},{point['y']}" for point in chart[key]])

    distribution_rows = db.execute(
        """
        SELECT cancer_type, prediction, COUNT(*) AS count
        FROM prediction_reports
        GROUP BY cancer_type, prediction
        ORDER BY cancer_type, count DESC
        """
    ).fetchall()
    distribution = [dict(row) for row in distribution_rows]
    max_distribution = max([row['count'] for row in distribution], default=1)
    for row in distribution:
        row['percent'] = round((row['count'] / max_distribution) * 100, 2) if max_distribution else 0

    users = db.execute(
        """
        SELECT
            users.id,
            users.username,
            users.is_admin,
            users.created_at,
            COUNT(prediction_reports.id) AS report_count
        FROM users
        LEFT JOIN prediction_reports ON prediction_reports.user_id = users.id
        GROUP BY users.id
        ORDER BY users.is_admin DESC, users.created_at ASC
        """
    ).fetchall()

    breast_positive = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM prediction_reports
        WHERE cancer_type = 'Breast Cancer' AND prediction LIKE '%Malignant%'
        """
    ).fetchone()['count']
    cervical_positive = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM prediction_reports
        WHERE cancer_type = 'Cervical Cancer' AND prediction LIKE '%Detected%'
        """
    ).fetchone()['count']

    return {
        'stats': {
            'total': total,
            'breast_total': breast_total,
            'cervical_total': cervical_total,
            'positive_total': positive_total,
            'breast_positive': breast_positive,
            'cervical_positive': cervical_positive,
            'users_total': len(users)
        },
        'recent_reports': rows,
        'time_series': time_series,
        'chart': chart,
        'distribution': distribution,
        'breast_importance': get_breast_feature_importance(),
        'cervical_importance': get_cervical_feature_importance(),
        'users': users
    }


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = get_db().execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password_hash'], password):
            flash('Invalid username or password.', 'error')
            return render_template('login.html', username=username)

        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = bool(user['is_admin'])
        flash('Welcome back.', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('register.html', username=username)
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html', username=username)
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html', username=username)

        try:
            db = get_db()
            is_first_user = db.execute('SELECT COUNT(*) AS count FROM users').fetchone()['count'] == 0
            db.execute(
                'INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), 1 if is_first_user else 0)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash('That username is already registered.', 'error')
            return render_template('register.html', username=username)

        flash('Account created. Please sign in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Signed out successfully.', 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    """
    Home page route
    Displays welcome page with cancer type selection
    """
    return render_template('index.html')


@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin.html', dashboard=get_admin_dashboard_data())


@app.route('/breast')
@login_required
def breast_form():
    """
    Breast cancer prediction form page
    Displays input form for breast cancer features
    """
    return render_template('breast.html')


@app.route('/cervical')
@login_required
def cervical_form():
    """
    Cervical cancer prediction form page
    Displays input form for cervical cancer features
    """
    return render_template('cervical.html')


@app.route('/predict/breast', methods=['POST'])
@login_required
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
        data = request.get_json() or {}
        
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
        log_prediction(
            'Breast Cancer',
            result,
            confidence,
            probability,
            len(user_inputs),
            len(features),
            user_inputs
        )
        
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
@login_required
def predict_cervical():
    """
    Predict cervical cancer risk
    
    Expected JSON input uses the highest-importance visible cervical fields.
    
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
        data = request.get_json() or {}
        
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
        log_prediction(
            'Cervical Cancer',
            result,
            confidence,
            probability,
            len(user_inputs),
            len(features),
            user_inputs
        )
        
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
@login_required
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
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
