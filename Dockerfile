FROM python:3.11

RUN apt-get update && apt-get install -y python3-venv passwd

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /app/requirements.txt

RUN adduser --disabled-password --gecos '' django_user && \
    chown -R django_user /app

COPY ./ /app

EXPOSE 8000

# Run the application as the newly created user
USER django_user
CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
