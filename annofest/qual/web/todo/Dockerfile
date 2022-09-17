FROM python:3.8.13-buster


WORKDIR /app
COPY ./Web/todo /app/
COPY ./Web/flag/todo.flag /flag
RUN chmod 444 /flag
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "todo.wsgi:application"]