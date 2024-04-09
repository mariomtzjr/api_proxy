FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /code

RUN apt update && apt install haveged -y

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . code

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/code

# Expose the port on which the application will run
EXPOSE 8000

CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "8000"]