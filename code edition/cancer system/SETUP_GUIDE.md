# 🚀 SETUP GUIDE - Quick Start Instructions

This guide will help you get the Cancer Risk Prediction System running in 5 minutes.

---

## ✅ Pre-requisites Check

Before starting, make sure you have:
- ✓ Python 3.7+ installed ([Download](https://www.python.org/downloads/))
- ✓ Project folder downloaded/cloned
- ✓ Model files in `models/` folder:
  - `breast_cancer_model.pkl`
  - `cervical_rf_model.pkl`

**Check Python version:**
```bash
python --version
```

Should show version 3.7 or higher.

---

## 📋 Step-by-Step Setup

### STEP 1: Navigate to Project Folder

**Windows (Command Prompt):**
```bash
cd d:\capstone project\code edition\cancer system
```

**macOS/Linux (Terminal):**
```bash
cd ~/path/to/cancer\ system
```

### STEP 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal.

### STEP 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for installation to complete. You should see:
```
Successfully installed Flask-2.3.3 scikit-learn-1.3.0 numpy-1.24.3 ...
```

### STEP 4: Verify Installation

```bash
pip list
```

Should show:
- Flask
- scikit-learn
- numpy
- Werkzeug
- joblib

### STEP 5: Verify Project Structure

Check that you have these files/folders:

```
cancer system/
├── app.py                    ✓
├── requirements.txt          ✓
├── README.md                 ✓
├── SETUP_GUIDE.md           ✓
├── models/                   ✓
│   ├── breast_cancer_model.pkl
│   └── cervical_rf_model.pkl
├── templates/                ✓
│   ├── index.html
│   ├── breast.html
│   ├── cervical.html
│   └── result.html
└── static/                   ✓
    └── style.css
```

---

## ▶️ Step 6: RUN THE APPLICATION

```bash
python app.py
```

### Expected Output:

```
 * Serving Flask app 'app'
 * Debug mode: on
✓ Breast cancer model loaded successfully
✓ Cervical cancer model loaded successfully

============================================================
Cancer Risk Prediction System - Starting...
============================================================

Server running at: http://localhost:5000
Home page: http://localhost:5000/

============================================================
```

---

## 🌐 Step 7: OPEN IN BROWSER

Copy and paste this URL in your browser:
```
http://localhost:5000
```

Or click this link (if terminal allows):
```
http://localhost:5000/
```

### You should see:
- Header: "Cancer Risk Prediction System"
- Welcome message
- Two buttons: "Breast Cancer" and "Cervical Cancer"

---

## ✨ Step 8: TEST THE APPLICATION

### Test Breast Cancer Prediction:
1. Click "🎀 Breast Cancer" button
2. Fill in the form with test data:
   - Radius Mean: `15.5`
   - Texture Mean: `19.0`
   - Perimeter Mean: `102.5`
   - Area Mean: `800.0`
   - Concavity Mean: `0.08`
   - Symmetry Mean: `0.15`
3. Click "🔍 Predict Cancer Risk"
4. See prediction result!

### Test Cervical Cancer Prediction:
1. Click "🏥 Cervical Cancer" button
2. Fill in the form with test data:
   - Age: `35`
   - HPV: `Positive (1)`
   - Smoking: `Non-Smoker (0)`
   - Pregnancies: `2`
   - STD History: `No STD History (0)`
3. Click "🔍 Predict Cancer Risk"
4. See prediction result!

---

## 🛑 Step 9: STOP THE SERVER

In your terminal/command prompt:
```bash
Ctrl + C
```

The server will stop. You'll see:
```
KeyboardInterrupt
Shutting down...
```

---

## 🔄 Next Time You Run IT

Just do steps 1, 2, and 6:

```bash
# 1. Navigate to folder
cd d:\capstone project\code edition\cancer system

# 2. Activate virtual environment
venv\Scripts\activate          # Windows
# OR
source venv/bin/activate       # macOS/Linux

# 3. Run app
python app.py
```

---

## ❓ Troubleshooting Quick Fixes

### Issue: "Python is not recognized"
**Fix:** Python not installed or not in PATH
- Reinstall Python
- During installation, check "Add Python to PATH"
- Restart terminal/command prompt

### Issue: "No module named 'flask'"
**Fix:** Dependencies not installed
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Fix:** Another process using port 5000
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Issue: "Model files not found"
**Fix:** Check models folder
- Verify `breast_cancer_model.pkl` exists
- Verify `cervical_rf_model.pkl` exists
- Path should be: `cancer system/models/`

### Issue: Page shows "Not Found"
**Fix:** Wrong URL
- Check URL is: `http://localhost:5000`
- NOT `http://localhost:5000/app.py`
- NOT `http://127.0.0.1`

---

## 📱 Access from Other Devices (Optional)

To access from another computer on same network:

1. Find your computer's IP address:
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - **macOS/Linux**: `ifconfig` (look for inet)

2. In Flask app, change the last line in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

3. Access from other device:
   ```
   http://<YOUR_IP>:5000
   ```

---

## 📊 Project File Sizes

- `app.py`: ~5 KB
- `requirements.txt`: ~0.5 KB
- `style.css`: ~20 KB
- All HTML files: ~15 KB
- README.md: ~25 KB
- **Total**: ~65 KB (before model files)

---

## ⏱️ Expected Performance

- **Page Load**: < 1 second
- **Model Load**: 2-3 seconds (first time)
- **Prediction Time**: < 500ms
- **Form Submission**: < 1 second

---

## 📚 Additional Help

### Check Flask Server Status:
- Open browser to `http://localhost:5000`
- If page loads, server is running ✓

### View Server Logs:
- Terminal shows all requests and errors
- Look for messages starting with `127.0.0.1`

### Enable Debug Mode:
- Already enabled in `app.py`
- Auto-reloads on file changes
- Shows detailed error messages

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Activate virtual env (Windows) | `venv\Scripts\activate` |
| Activate virtual env (macOS/Linux) | `source venv/bin/activate` |
| Install dependencies | `pip install -r requirements.txt` |
| Run application | `python app.py` |
| Stop application | `Ctrl + C` |
| Check Python version | `python --version` |
| List installed packages | `pip list` |

---

## ✅ Success Checklist

After following all steps, you should have:
- ✓ Python and dependencies installed
- ✓ Virtual environment created and activated
- ✓ Flask server running on localhost:5000
- ✓ Home page loading in browser
- ✓ Both prediction forms accessible
- ✓ Predictions working correctly

---

## 🎓 Next Steps

After setup:
1. **Explore the Code**: Read comments in `app.py`
2. **Customize UI**: Modify `static/style.css`
3. **Add Features**: Update `app.py` with new routes
4. **Improve Models**: Retrain with new data

---

## 📝 Notes

- Virtual environment is required for clean Python environment
- Keep model files (.pkl) in `models/` folder
- Don't modify project structure
- Debug mode is on (auto-reload on file changes)
- No data is stored (stateless application)

---

**You're all set! Enjoy your Cancer Risk Prediction System! 🎉**

Need more help? Check README.md for detailed information.
