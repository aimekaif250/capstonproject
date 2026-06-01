# 🏥 Cancer Risk Prediction System
## Machine Learning-Based System for Breast and Cervical Cancer Risk Prediction

A complete web-based application built with Flask and Machine Learning for predicting cancer risk based on patient data.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Input Features](#input-features)
- [Troubleshooting](#troubleshooting)

---

## 📌 Project Overview

This is a university final-year project that demonstrates the integration of machine learning with web development. The system allows healthcare professionals to:

1. **Select Cancer Type**: Choose between Breast or Cervical cancer prediction
2. **Enter Patient Data**: Input clinical measurements and patient history
3. **Get Risk Assessment**: Receive ML-based predictions with confidence scores
4. **View Detailed Results**: See probability distributions for informed decision-making

### Key Technologies:
- **Backend**: Python Flask framework
- **ML Models**: Pre-trained scikit-learn models (saved as .pkl files)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: Not required (stateless predictions)

---

## ✨ Features

✅ **User-Friendly Interface**
- Clean, professional UI design
- Responsive layout (works on desktop, tablet, mobile)
- Clear navigation between pages

✅ **Two Cancer Type Predictions**
- Breast Cancer (6 clinical features)
- Cervical Cancer (5 patient history features)

✅ **Advanced Predictions**
- Confidence scores
- Probability distribution display
- Real-time prediction processing

✅ **Input Validation**
- Client-side form validation
- Server-side data validation
- Error handling for invalid inputs

✅ **Professional Design**
- Gradient headers
- Responsive forms
- Accessibility considerations
- Loading indicators
- Error messages

---

## 📂 Project Structure

```
cancer system/
│
├── app.py                    # Main Flask application
│
├── models/                   # Pre-trained ML models
│   ├── breast_cancer_model.pkl    # Breast cancer model
│   └── cervical_rf_model.pkl      # Cervical cancer model
│
├── templates/                # HTML templates
│   ├── index.html           # Home page
│   ├── breast.html          # Breast cancer prediction form
│   ├── cervical.html        # Cervical cancer prediction form
│   └── result.html          # Results display page
│
├── static/                   # Static files (CSS, JS images)
│   └── style.css            # Main stylesheet
│
├── requirements.txt          # Python dependencies
├── INPUT_DATA_DOCUMENTATION.md  # Full input feature mapping and defaults
└── README.md                # This file
```

---

## 📦 Requirements

### System Requirements:
- Python 3.7 or higher
- Windows, macOS, or Linux
- Minimum 2GB RAM
- 500MB disk space

### Python Packages:
```
Flask==2.3.0
scikit-learn==1.3.0
numpy==1.24.0
pickle (built-in)
```

---

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd cancer-system

# Or just download the folder
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Model Files
Ensure these files exist in the `models/` folder:
- `breast_cancer_model.pkl`
- `cervical_rf_model.pkl`

If models are missing, the app will show an error message.

### Step 5: Check Project Structure
```bash
# Verify your folder structure matches the one above
ls -la    # On macOS/Linux
dir       # On Windows
```

---

## ▶️ Running the Application

### Start the Flask Server:

**Windows:**
```bash
python app.py
```

**macOS/Linux:**
```bash
python3 app.py
```

### Expected Output:
```
============================================================
Cancer Risk Prediction System - Starting...
============================================================

Server running at: http://localhost:5000
Home page: http://localhost:5000/

============================================================
```

### Open in Browser:
- Navigate to: **http://localhost:5000**
- The home page should load with cancer type selection

### Stop the Server:
Press `Ctrl + C` in the terminal

---

## 📖 Usage Guide

### Workflow:

#### 1. **Home Page (index.html)**
   - View system overview
   - Read instructions
   - Select cancer type
   - Two buttons: "Breast Cancer" and "Cervical Cancer"

#### 2. **Breast Cancer Form**
   - Enter 6 medical measurements:
     - Radius Mean
     - Texture Mean
     - Perimeter Mean
     - Area Mean
     - Concavity Mean
     - Symmetry Mean
   - Click "Predict Cancer Risk" button
   - View results with confidence score

#### 3. **Cervical Cancer Form**
   - Enter 5 patient history features:
     - Age
     - HPV Status (0 or 1)
     - Smoking Status (0 or 1)
     - Number of Pregnancies
     - STD History (0 or 1)
   - Click "Predict Cancer Risk" button
   - View results with confidence score

#### 4. **Results Page**
   - Prediction result (Benign/Malignant or Cancer Risk/No Risk)
   - Confidence percentage
   - Full probability breakdown
   - Navigation options

---

## 🔌 API Endpoints

### Home Page
```
GET /
Returns: index.html (home page)
```

### Breast Cancer Form
```
GET /breast
Returns: breast.html (form page)

POST /predict/breast
Accepts JSON:
{
    "radius_mean": float,
    "texture_mean": float,
    "perimeter_mean": float,
    "area_mean": float,
    "concavity_mean": float,
    "symmetry_mean": float
}

Returns JSON:
{
    "success": true,
    "prediction": "Benign (Non-Cancerous)" or "Malignant (Cancer)",
    "confidence": "95.23%",
    "probability_benign": "95.23%",
    "probability_malignant": "4.77%",
    "cancer_type": "Breast Cancer"
}
```

### Cervical Cancer Form
```
GET /cervical
Returns: cervical.html (form page)

POST /predict/cervical
Accepts JSON:
{
    "age": int,
    "hpv": int (0 or 1),
    "smoking": int (0 or 1),
    "pregnancies": int,
    "std_history": int (0 or 1)
}

Returns JSON:
{
    "success": true,
    "prediction": "No Cancer Risk" or "Cancer Risk Detected",
    "confidence": "87.50%",
    "probability_no_cancer": "87.50%",
    "probability_cancer": "12.50%",
    "cancer_type": "Cervical Cancer"
}
```

### Results Page
```
GET /result
Returns: result.html (results page)
```

---

## 🔍 Input Features

### Breast Cancer Model Features:

| Feature | Type | Unit | Typical Range | Example |
|---------|------|------|----------------|---------|
| radius_mean | float | mm | 6-30 | 15.5 |
| texture_mean | float | - | 9-39 | 19.0 |
| perimeter_mean | float | mm | 40-188 | 102.5 |
| area_mean | float | mm² | 140-2500 | 800.0 |
| concavity_mean | float | - | 0-0.4 | 0.08 |
| symmetry_mean | float | - | 0.1-0.3 | 0.15 |

> Note: The breast cancer model expects 30 features in total. Only 6 are entered by the user; the remaining 24 are automatically filled with dataset mean values.
> See `INPUT_DATA_DOCUMENTATION.md` for the full feature order and default values.

### Cervical Cancer Model Features:

| Feature | Type | Values | Description |
|---------|------|--------|-------------|
| age | integer | 10-80 | Patient age in years |
| hpv | integer | 0 or 1 | HPV status (0=No, 1=Yes) |
| smoking | integer | 0 or 1 | Smoking status (0=No, 1=Yes) |
| pregnancies | integer | 0-15 | Number of pregnancies |
| std_history | integer | 0 or 1 | STD history (0=No, 1=Yes) |

---

## 🐛 Troubleshooting

### Issue: "Address already in use" error
**Solution:**
```bash
# Kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

### Issue: Model files not found
**Solution:**
- Ensure model files are in the `models/` folder
- Check file names match exactly:
  - `breast_cancer_model.pkl`
  - `cervical_rf_model.pkl`

### Issue: ModuleNotFoundError
**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall requirements
pip install --upgrade -r requirements.txt
```

### Issue: Form not submitting
**Solution:**
- Check browser console (F12) for JavaScript errors
- Ensure all form fields are filled correctly
- Try a different browser
- Clear browser cache

### Issue: Predictions not loading
**Solution:**
- Check Flask server console for errors
- Verify models are properly loaded (check startup messages)
- Check network tab in browser dev tools
- Restart Flask server

---

## 📝 Code Comments

The code includes comprehensive comments:
- **app.py**: Route explanations, prediction logic
- **HTML files**: Form field descriptions, navigation
- **CSS**: Section organization, styling purposes

---

## 🎓 Learning Outcomes

By studying this project, you will learn:

1. **Flask Basics**
   - Route creation
   - Request/response handling
   - JSON APIs

2. **Machine Learning Integration**
   - Model loading (.pkl files)
   - Feature preparation
   - Prediction generation

3. **Web Development**
   - HTML form handling
   - JavaScript fetch API
   - CSS responsive design

4. **Best Practices**
   - Error handling
   - Input validation
   - Project structure

---

## 📄 Files Breakdown

### app.py (175 lines)
- Flask initialization
- Model loading
- 6 main routes
- 2 prediction endpoints
- Error handling

### templates/index.html (70+ lines)
- Home page
- Cancer selection
- Information cards

### templates/breast.html (120+ lines)
- Breast cancer form
- 6 input fields
- JavaScript prediction logic
- Result display

### templates/cervical.html (130+ lines)
- Cervical cancer form
- 5 input fields
- JavaScript prediction logic
- Result display

### templates/result.html (35+ lines)
- Results page template

### static/style.css (450+ lines)
- Professional styling
- Responsive design
- Dark/light color scheme
- Animations

---

## 📊 Expected Results Examples

### Breast Cancer Prediction:
```
Prediction: Benign (Non-Cancerous)
Confidence: 94.52%
Probability (Benign): 94.52%
Probability (Malignant): 5.48%
```

### Cervical Cancer Prediction:
```
Prediction: No Cancer Risk
Confidence: 88.35%
Probability (No Cancer): 88.35%
Probability (Cancer Risk): 11.65%
```

---

## ⚠️ Important Disclaimer

This system is for **educational purposes only** and should NOT be used for actual medical diagnosis. 

**Always consult with qualified healthcare professionals** for:
- Medical diagnosis
- Treatment decisions
- Patient care

---

## 🔒 Security Notes

- No authentication required (for demonstration)
- No database storage
- Predictions are not saved
- No user personal data collection
- All processing happens locally

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review code comments
3. Check Flask console for error messages
4. Verify all files are in correct locations

---

## 📜 License

This project is for educational purposes as part of a university final-year project.

---

## 👨‍💼 Project Information

- **Title**: Machine Learning-Based System for Breast and Cervical Cancer Risk Prediction
- **Type**: Final Year Project
- **Technology**: Flask + Machine Learning
- **Status**: Complete and Ready to Deploy

---

**Last Updated**: May 2024  
**Version**: 1.0

## ▶️ Quick Start (Windows)

1. Double-click `run.bat` or run it from Command Prompt:
   D:\capstone project\code edition\cancer system> run.bat

2. Or run PowerShell wrapper (recommended if you need py launcher):
   powershell -ExecutionPolicy Bypass -File .\run.ps1

Notes:
- The scripts prefer Python 3.11 (py -3.11). If you only have Python 3.14, the scripts will try but scikit-learn/numpy wheels may not be available for 3.14 — use Python 3.11 or conda if you see build errors.
- Open http://localhost:5000 in your browser after the server starts.
