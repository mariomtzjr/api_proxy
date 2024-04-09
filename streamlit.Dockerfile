FROM python:3.9-slim-buster

WORKDIR /code

RUN pip install streamlit

COPY . code
CMD ["streamlit", "run", "./code/lit.py", "--server.port", "8000"]
