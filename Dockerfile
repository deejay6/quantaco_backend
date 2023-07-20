FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install pipenv

# switch to code folder
WORKDIR /home/ubuntu/quantaco

# Copy code folder
COPY . .

# install requirements
RUN pip3 install -r requirements.txt

RUN python3 manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]