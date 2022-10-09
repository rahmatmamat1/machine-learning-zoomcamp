import pickle
import uvicorn

from fastapi import FastAPI, Request

model_file = 'model_C=1.0.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = FastAPI()

@app.post('/predict')
def predict(customer: Request):
    customer = customer.json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    churn = y_pred >= 0.5

    result = {
        'churn_probability': float(y_pred),
        'churn': bool(churn)
    }

    return result


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9696)