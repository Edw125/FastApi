FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .

CMD ["uvicorn", "server:app"]