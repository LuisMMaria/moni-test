#Python
FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

#Execute install
RUN python -m pip install -r requirements.txt

#Copy to the code folder
COPY . /code/