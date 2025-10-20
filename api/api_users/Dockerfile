FROM python:3.14.0rc3-alpine3.22

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "users.py"]
