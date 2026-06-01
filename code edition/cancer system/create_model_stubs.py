import os, pickle
os.makedirs('models', exist_ok=True)

class StubModel:
    def predict(self, X): return [0]            # always benign / no-risk
    def predict_proba(self, X): return [[0.95, 0.05]]

for fname in ('breast_cancer_model.pkl','cervical_rf_model.pkl'):
    with open(os.path.join('models', fname), 'wb') as f:
        pickle.dump(StubModel(), f)

print("Model stubs created in ./models/")