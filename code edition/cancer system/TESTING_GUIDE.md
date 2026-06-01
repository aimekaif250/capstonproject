# 🧪 Testing & API Reference Guide

Quick reference for testing the Cancer Risk Prediction System API endpoints.

---

## 📌 Test Data Examples

### Breast Cancer Test Cases

#### Test Case 1: Benign Tumor
```json
{
    "radius_mean": 12.0,
    "texture_mean": 15.0,
    "perimeter_mean": 75.0,
    "area_mean": 400.0,
    "concavity_mean": 0.02,
    "symmetry_mean": 0.12
}
```

#### Test Case 2: Malignant Tumor
```json
{
    "radius_mean": 20.0,
    "texture_mean": 25.0,
    "perimeter_mean": 130.0,
    "area_mean": 1200.0,
    "concavity_mean": 0.15,
    "symmetry_mean": 0.20
}
```

#### Test Case 3: Medium Risk
```json
{
    "radius_mean": 15.5,
    "texture_mean": 19.0,
    "perimeter_mean": 102.5,
    "area_mean": 800.0,
    "concavity_mean": 0.08,
    "symmetry_mean": 0.15
}
```

---

### Cervical Cancer Test Cases

#### Test Case 1: Low Risk
```json
{
    "age": 25,
    "hpv": 0,
    "smoking": 0,
    "pregnancies": 0,
    "std_history": 0
}
```

#### Test Case 2: High Risk
```json
{
    "age": 45,
    "hpv": 1,
    "smoking": 1,
    "pregnancies": 3,
    "std_history": 1
}
```

#### Test Case 3: Medium Risk
```json
{
    "age": 35,
    "hpv": 1,
    "smoking": 0,
    "pregnancies": 2,
    "std_history": 0
}
```

---

## 🧬 Feature Ranges & Validation

### Breast Cancer Features

| Feature | Min | Max | Type | Notes |
|---------|-----|-----|------|-------|
| radius_mean | 6.0 | 30.0 | float | Cell nucleus average radius |
| texture_mean | 9.0 | 39.0 | float | Gray-scale texture values |
| perimeter_mean | 40.0 | 188.0 | float | Cell nucleus perimeter |
| area_mean | 140.0 | 2500.0 | float | Cell nucleus area |
| concavity_mean | 0.0 | 0.4 | float | Severity of concavities |
| symmetry_mean | 0.1 | 0.3 | float | Nucleus symmetry value |

### Cervical Cancer Features

| Feature | Valid Values | Type | Notes |
|---------|--------------|------|-------|
| age | 10-80 | int | Patient age in years |
| hpv | 0, 1 | int | 0=Negative, 1=Positive |
| smoking | 0, 1 | int | 0=Non-smoker, 1=Smoker |
| pregnancies | 0-20 | int | Total number of pregnancies |
| std_history | 0, 1 | int | 0=No history, 1=History |

---

## 🔌 API Endpoints

### 1. Home Page
```
GET /
Returns: HTML (home page)
Status: 200 OK
```

### 2. Breast Cancer Form
```
GET /breast
Returns: HTML (breast cancer form)
Status: 200 OK
```

### 3. Cervical Cancer Form
```
GET /cervical
Returns: HTML (cervical cancer form)
Status: 200 OK
```

### 4. Breast Cancer Prediction
```
POST /predict/breast
Content-Type: application/json

Request Body:
{
    "radius_mean": number,
    "texture_mean": number,
    "perimeter_mean": number,
    "area_mean": number,
    "concavity_mean": number,
    "symmetry_mean": number
}

Success Response (200):
{
    "success": true,
    "prediction": "Benign (Non-Cancerous)" | "Malignant (Cancer)",
    "confidence": "XX.XX%",
    "probability_benign": "XX.XX%",
    "probability_malignant": "XX.XX%",
    "cancer_type": "Breast Cancer"
}

Error Response (400/500):
{
    "success": false,
    "error": "Error message"
}
```

### 5. Cervical Cancer Prediction
```
POST /predict/cervical
Content-Type: application/json

Request Body:
{
    "age": integer,
    "hpv": 0 | 1,
    "smoking": 0 | 1,
    "pregnancies": integer,
    "std_history": 0 | 1
}

Success Response (200):
{
    "success": true,
    "prediction": "No Cancer Risk" | "Cancer Risk Detected",
    "confidence": "XX.XX%",
    "probability_no_cancer": "XX.XX%",
    "probability_cancer": "XX.XX%",
    "cancer_type": "Cervical Cancer"
}

Error Response (400/500):
{
    "success": false,
    "error": "Error message"
}
```

---

## 🔧 Testing with cURL

### Breast Cancer Test (Command Line)

```bash
curl -X POST http://localhost:5000/predict/breast \
  -H "Content-Type: application/json" \
  -d '{
    "radius_mean": 15.5,
    "texture_mean": 19.0,
    "perimeter_mean": 102.5,
    "area_mean": 800.0,
    "concavity_mean": 0.08,
    "symmetry_mean": 0.15
  }'
```

### Cervical Cancer Test (Command Line)

```bash
curl -X POST http://localhost:5000/predict/cervical \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "hpv": 1,
    "smoking": 0,
    "pregnancies": 2,
    "std_history": 0
  }'
```

---

## 🧠 Testing with Python

### Breast Cancer Test Script

```python
import requests
import json

url = "http://localhost:5000/predict/breast"

data = {
    "radius_mean": 15.5,
    "texture_mean": 19.0,
    "perimeter_mean": 102.5,
    "area_mean": 800.0,
    "concavity_mean": 0.08,
    "symmetry_mean": 0.15
}

response = requests.post(url, json=data)
result = response.json()

print(json.dumps(result, indent=2))
```

### Cervical Cancer Test Script

```python
import requests
import json

url = "http://localhost:5000/predict/cervical"

data = {
    "age": 35,
    "hpv": 1,
    "smoking": 0,
    "pregnancies": 2,
    "std_history": 0
}

response = requests.post(url, json=data)
result = response.json()

print(json.dumps(result, indent=2))
```

---

## 📊 Expected Response Examples

### Breast Cancer Success Response

```json
{
    "success": true,
    "prediction": "Benign (Non-Cancerous)",
    "confidence": "94.52%",
    "probability_benign": "94.52%",
    "probability_malignant": "5.48%",
    "cancer_type": "Breast Cancer"
}
```

### Cervical Cancer Success Response

```json
{
    "success": true,
    "prediction": "Cancer Risk Detected",
    "confidence": "72.35%",
    "probability_no_cancer": "27.65%",
    "probability_cancer": "72.35%",
    "cancer_type": "Cervical Cancer"
}
```

### Error Response

```json
{
    "success": false,
    "error": "Invalid input value: could not convert string to float"
}
```

---

## 🧪 Browser Developer Tools Testing

### Using Browser Console (F12)

#### Breast Cancer Prediction

```javascript
fetch('/predict/breast', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        radius_mean: 15.5,
        texture_mean: 19.0,
        perimeter_mean: 102.5,
        area_mean: 800.0,
        concavity_mean: 0.08,
        symmetry_mean: 0.15
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### Cervical Cancer Prediction

```javascript
fetch('/predict/cervical', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        age: 35,
        hpv: 1,
        smoking: 0,
        pregnancies: 2,
        std_history: 0
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## ✅ Testing Checklist

- [ ] Home page loads correctly
- [ ] Breast cancer form displays
- [ ] Cervical cancer form displays
- [ ] Breast cancer prediction works
- [ ] Cervical cancer prediction works
- [ ] Error handling works (test with invalid data)
- [ ] Form validation works
- [ ] Navigation between pages works
- [ ] CSS styling loads properly
- [ ] Responsive design works on mobile

---

## 🐛 Common Testing Issues

### Issue: CORS Error
**Solution:** CORS is not enabled (not needed for same-origin requests)

### Issue: 404 Not Found
**Solution:** Check endpoint URL matches exactly

### Issue: 500 Server Error
**Solution:** Check Flask console for error messages

### Issue: Predictions Always Same
**Solution:** Model might be returning default prediction

---

## 📈 Performance Testing

### Load Testing Endpoints

```bash
# Simple load test (requires Apache Bench)
ab -n 100 -c 10 http://localhost:5000/
```

### Response Time Measurement

```bash
# Using curl to measure response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/
```

---

## 🔍 Debugging Tips

1. **Check Flask Console**
   - Look for error messages
   - Watch for missing models warning
   - Monitor request logs

2. **Check Browser Console (F12)**
   - Look for JavaScript errors
   - Check Network tab for failed requests
   - View request/response details

3. **Test Directly**
   - Use curl or Python for direct API testing
   - Bypass frontend JavaScript
   - Isolate backend issues

4. **Enable Debug Logging**
   - Flask debug mode is enabled
   - Add print statements in app.py
   - Check terminal output

---

## 📋 Testing Scenarios

### Scenario 1: Complete Workflow
1. Load home page
2. Click breast cancer
3. Fill form with valid data
4. Submit form
5. View results
6. Go back to home

### Scenario 2: Error Handling
1. Fill form with invalid data (text in number field)
2. Submit form
3. See error message
4. Correct data
5. Resubmit form

### Scenario 3: Navigation
1. Test all navigation links
2. Test back buttons
3. Test home page links
4. Verify no 404 errors

---

## 📞 Support Resources

- Flask Documentation: https://flask.palletsprojects.com/
- scikit-learn Docs: https://scikit-learn.org/stable/
- HTTP Status Codes: https://httpwg.org/specs/rfc7231.html#status.codes

---

**Happy Testing! 🎉**
