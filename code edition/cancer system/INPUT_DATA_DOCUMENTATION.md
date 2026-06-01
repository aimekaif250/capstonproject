# 📊 Breast Cancer Prediction - Input Data Documentation

## Overview

This document explains the input data structure for the Breast Cancer Risk Prediction system. The system uses a Random Forest model trained on the Breast Cancer Wisconsin dataset, which contains 30 features. However, the web interface only collects 6 key features from users, while the remaining 24 features are automatically filled with mean values from the training dataset.

---

## 🔢 Feature Structure

### Total Features: 30
- **User Input Features**: 6 (collected from web form)
- **Auto-Filled Features**: 24 (filled with dataset mean values)

---

## 📝 User Input Features (6)

These are the features collected from the web form:

| Feature | Description | Data Type | Example Value |
|---------|-------------|-----------|---------------|
| `radius_mean` | Mean radius of cell nuclei | Float | 14.127 |
| `texture_mean` | Mean texture (standard deviation of gray-scale values) | Float | 19.289 |
| `perimeter_mean` | Mean perimeter of cell nuclei | Float | 91.969 |
| `area_mean` | Mean area of cell nuclei | Float | 654.889 |
| `concavity_mean` | Mean concavity (severity of concave portions) | Float | 0.0888 |
| `symmetry_mean` | Mean symmetry of cell nuclei | Float | 0.1812 |

---

## 🤖 Auto-Filled Features (24)

These features are automatically filled with mean values from the Breast Cancer Wisconsin dataset:

### Mean Features (4)
| Feature | Mean Value | Description |
|---------|------------|-------------|
| `smoothness_mean` | 0.09636 | Mean smoothness (local variation in radius lengths) |
| `compactness_mean` | 0.10434 | Mean compactness (perimeter²/area - 1.0) |
| `concave points_mean` | 0.04892 | Mean number of concave portions |
| `fractal_dimension_mean` | 0.06280 | Mean fractal dimension ("coastline approximation" - 1) |

### Standard Error Features (10)
| Feature | Mean Value | Description |
|---------|------------|-------------|
| `radius_se` | 0.40517 | Standard error of radius |
| `texture_se` | 1.21685 | Standard error of texture |
| `perimeter_se` | 2.86606 | Standard error of perimeter |
| `area_se` | 40.33708 | Standard error of area |
| `smoothness_se` | 0.00704 | Standard error of smoothness |
| `compactness_se` | 0.02548 | Standard error of compactness |
| `concavity_se` | 0.03189 | Standard error of concavity |
| `concave points_se` | 0.01180 | Standard error of concave points |
| `symmetry_se` | 0.02054 | Standard error of symmetry |
| `fractal_dimension_se` | 0.00379 | Standard error of fractal dimension |

### Worst Features (10)
| Feature | Mean Value | Description |
|---------|------------|-------------|
| `radius_worst` | 16.26919 | Worst (largest) radius |
| `texture_worst` | 25.67722 | Worst (largest) texture |
| `perimeter_worst` | 107.26121 | Worst (largest) perimeter |
| `area_worst` | 880.58313 | Worst (largest) area |
| `smoothness_worst` | 0.13237 | Worst (largest) smoothness |
| `compactness_worst` | 0.25427 | Worst (largest) compactness |
| `concavity_worst` | 0.27219 | Worst (largest) concavity |
| `concave points_worst` | 0.11461 | Worst (largest) concave points |
| `symmetry_worst` | 0.29008 | Worst (largest) symmetry |
| `fractal_dimension_worst` | 0.08395 | Worst (largest) fractal dimension |

---

## 🔄 Input Processing Flow

### 1. User Input Collection
```json
{
  "radius_mean": 14.5,
  "texture_mean": 20.1,
  "perimeter_mean": 95.2,
  "area_mean": 700.5,
  "concavity_mean": 0.12,
  "symmetry_mean": 0.19
}
```

### 2. Feature Vector Construction
The system builds a complete 30-feature vector:

```python
features = [
    14.5,    # radius_mean (user input)
    20.1,    # texture_mean (user input)
    95.2,    # perimeter_mean (user input)
    700.5,   # area_mean (user input)
    0.09636, # smoothness_mean (default)
    0.10434, # compactness_mean (default)
    0.12,    # concavity_mean (user input)
    0.04892, # concave points_mean (default)
    0.19,    # symmetry_mean (user input)
    0.06280, # fractal_dimension_mean (default)
    # ... and so on for all 30 features
]
```

### 3. Model Prediction
- Features converted to NumPy array: `shape (1, 30)`
- Passed to Random Forest model
- Returns prediction and probabilities

---

## ✅ Input Validation

The system validates all inputs:

- **Required Fields**: All 6 user input features must be provided
- **Data Types**: All values must be numeric (float)
- **Range Checks**: Values should be within reasonable biological ranges
- **Error Handling**: Clear error messages for invalid inputs

### Validation Rules
- `radius_mean`: 5.0 - 30.0
- `texture_mean`: 5.0 - 40.0
- `perimeter_mean`: 40.0 - 200.0
- `area_mean`: 100.0 - 3000.0
- `concavity_mean`: 0.0 - 0.5
- `symmetry_mean`: 0.0 - 0.5

---

## 📊 Prediction Output

The model returns:

```json
{
  "success": true,
  "prediction": "Benign (Non-Cancerous)",
  "confidence": "87.45%",
  "probability_benign": "87.45%",
  "probability_malignant": "12.55%",
  "cancer_type": "Breast Cancer",
  "input_features_used": 6,
  "total_features": 30
}
```

---

## 🔧 Technical Implementation

### Feature Order (Critical)
The features must be provided in this exact order to match the trained model:

1. radius_mean
2. texture_mean
3. perimeter_mean
4. area_mean
5. smoothness_mean
6. compactness_mean
7. concavity_mean
8. concave points_mean
9. symmetry_mean
10. fractal_dimension_mean
11. radius_se
12. texture_se
13. perimeter_se
14. area_se
15. smoothness_se
16. compactness_se
17. concavity_se
18. concave points_se
19. symmetry_se
20. fractal_dimension_se
21. radius_worst
22. texture_worst
23. perimeter_worst
24. area_worst
25. smoothness_worst
26. compactness_worst
27. concavity_worst
28. concave points_worst
29. symmetry_worst
30. fractal_dimension_worst

---

## 📚 Data Source

- **Dataset**: Breast Cancer Wisconsin (Diagnostic)
- **Source**: UCI Machine Learning Repository
- **Features**: 30 (computed from digitized images)
- **Samples**: 569 (357 benign, 212 malignant)
- **Model**: Random Forest Classifier

---

## ⚠️ Important Notes

1. **Feature Scaling**: The model expects features in their original scale (not standardized)
2. **Default Values**: Mean values are calculated from the entire training dataset
3. **Model Compatibility**: Only works with models trained on the same 30 features
4. **Prediction Accuracy**: Using default values for 24 features may reduce accuracy compared to full feature sets

---

## 🆘 Troubleshooting

### Common Issues:
- **"Missing required input"**: Ensure all 6 user input fields are provided
- **"Invalid numeric value"**: Check that all inputs are numbers
- **"Model not loaded"**: Verify `breast_cancer_model.pkl` exists in `models/` folder

### Debug Information:
The API response includes `input_features_used` and `total_features` to verify correct processing.

---

*Last updated: May 4, 2026*