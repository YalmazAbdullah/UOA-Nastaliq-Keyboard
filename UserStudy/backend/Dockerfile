# FROM python:3.10

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# RUN chown -R 1000:1000 /_database.db /assets
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]