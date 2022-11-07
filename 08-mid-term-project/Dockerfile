FROM python:3.9-slim

WORKDIR /app

RUN pip install pipenv

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt

COPY ["model_xgb.bin", "service.py", "./"]

# EXPOSE 9696

# ENTRYPOINT [ "python", "predict_fastapi.py" ]
RUN pip install gunicorn

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --worker-class uvicorn.workers.UvicornWorker --timeout 0 service:app