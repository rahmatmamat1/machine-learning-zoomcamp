FROM python:3.9-slim

RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "model_C=1.0.bin", "./"]

# EXPOSE 9696
RUN pip install gunicorn

# ENTRYPOINT [ "waitress-serve", "--listen=0.0.0.0:9696", "predict:app" ]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 predict:app