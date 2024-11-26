FROM python:3.8
WORKDIR /app
COPY app /app
COPY app/data/model.pkl /app/data/model.pkl
COPY app/data/.env /app/data/.env
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD python app/main.py