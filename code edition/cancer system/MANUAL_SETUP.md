# 🚨 MANUAL SETUP GUIDE

## Since Python is not in PATH, follow these steps:

---

## 📋 STEP-BY-STEP MANUAL SETUP

### Step 1: Add Python to PATH

1. **Press Windows Key + R**
2. **Type: `sysdm.cpl`** and press Enter
3. **Click "Advanced" tab**
4. **Click "Environment Variables"**
5. **Under "System variables", find "Path"**
6. **Click "Edit"**
7. **Click "New"**
8. **Add this path:**
   ```
   C:\Users\RP.Ngoma\AppData\Local\Microsoft\WindowsApps\
   ```
9. **Click "OK" on all windows**
10. **Restart Command Prompt**

### Step 2: Verify Python Works

Open a **new** Command Prompt and run:
```cmd
python --version
```

You should see: `Python 3.x.x`

### Step 3: Run Setup

```cmd
cd "d:\capstone project\code edition\cancer system"
setup.bat
```

### Step 4: Run Application

```cmd
run.bat
```

### Step 5: Open Browser

Go to: `http://localhost:5000`

---

## 🔄 ALTERNATIVE: Use Full Path

If PATH doesn't work, you can run Python directly:

### Create Virtual Environment:
```cmd
cd "d:\capstone project\code edition\cancer system"
"C:\Users\RP.Ngoma\AppData\Local\Microsoft\WindowsApps\python.exe" -m venv venv
```

### Activate and Install:
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### Run Application:
```cmd
python app.py
```

---

## 📞 STILL NOT WORKING?

### Option A: Download Python from python.org
1. Go to: https://www.python.org/downloads/
2. Download Python 3.8+
3. Install with "Add to PATH" checked
4. Run setup.bat

### Option B: Use VS Code Python Extension
1. Install VS Code
2. Install Python extension
3. Use VS Code terminal to run setup

### Option C: Use Online Environment
- Google Colab
- Replit
- PythonAnywhere

---

## ✅ QUICK CHECK

After setup, you should see:
```
============================================================
Cancer Risk Prediction System - Starting...
============================================================

Server running at: http://localhost:5000
Home page: http://localhost:5000/

============================================================
```

---

**Need help? Check PYTHON_INSTALLATION.md for more details!**