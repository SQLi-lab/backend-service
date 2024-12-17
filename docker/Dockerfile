FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise

RUN python3 manage.py collectstatic --noinput

RUN adduser --disabled-password --gecos "" user
RUN chown -R user /app

USER user

