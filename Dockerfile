# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.5.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /ctis_api

# Get the Real World example app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]