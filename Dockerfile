FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Seed database and ensure ML model is trained
RUN python seed_data.py && python ml/generate_data.py && python ml/train_model.py

ENV PORT=8080
EXPOSE 8080

CMD ["python", "app.py"]
