FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . app

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Expose the port on which the application will run
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]