FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r ./requirements.txt
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]

