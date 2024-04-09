FROM python:3.9-slim-buster

WORKDIR /code

RUN apt update && apt install unzip

RUN pip install panel pandas matplotlib hvplot holoviews

ADD http://archive.ics.uci.edu/ml/machine-learning-databases/00357/occupancy_data.zip /code/data/

RUN cd /code/data/ && unzip occupancy_data.zip

COPY . code

CMD ["panel", "serve", "--show", "./code/paneler.py", "--address", "0.0.0.0", "--port", "8000"]