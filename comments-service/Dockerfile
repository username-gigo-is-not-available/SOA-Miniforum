FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "logging_config.yaml"]
