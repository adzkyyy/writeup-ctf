FROM python:3.8.13-buster


WORKDIR /app
COPY ./Web/curl /app/
COPY ./Web/flag/curl.flag /flag
RUN chmod 444 /flag
RUN pip install flask==2.1.2
RUN pip install gunicorn==20.1.0

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app:app"]