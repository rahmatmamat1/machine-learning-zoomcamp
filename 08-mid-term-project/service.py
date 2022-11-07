import pickle
import uvicorn

from fastapi import FastAPI

from pydantic import BaseModel

class Click(BaseModel):
    ip: int
    app: int
    device: int
    os: int
    channel: int
    day: int
    hour: int
    minute: int
    second: int

model_file = 'model_xgb.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = FastAPI()

@app.post('/')

async def predict(click: Click):
    click_dict = click.dict()

    X = dv.transform([click_dict])
    y_pred = model.predict_proba(X)[0, 1]
    churn = y_pred >= 0.5

    result = {
        'download_probability': float(y_pred),
        'download': bool(churn)
    }

    return result


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9696)