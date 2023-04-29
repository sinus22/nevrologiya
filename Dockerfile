FROM python:3.10-bullseye



WORKDIR /usr/src/app
# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install -y python3-dev default-libmysqlclient-dev build-essential
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver"]