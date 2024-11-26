FROM python:3.8
COPY /app /app
RUN pip install --no-cache-dir -r requirements.txt
CMD python app/main.py