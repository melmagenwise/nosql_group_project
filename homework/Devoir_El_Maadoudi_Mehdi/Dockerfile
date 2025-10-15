FROM python:3.12.6

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


ENV MONGO_URI=mongodb://mongo:27017 \
    MONGO_DB=vgstore \
    REDIS_URL=redis://redis:6379/0

EXPOSE 5000

CMD ["python", "app.py"]