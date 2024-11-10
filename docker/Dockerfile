FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos "" user
RUN chown -R user /app

USER user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
