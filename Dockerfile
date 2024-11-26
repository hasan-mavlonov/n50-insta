FROM python:3.12
RUN useradd -m django_user
USER django_user
# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Create and activate the virtual environment
RUN python -m venv /venv
RUN /venv/bin/pip install -r requirements.txt

# Copy your application code
COPY . /app

# Set environment variables if needed
ENV PYTHONPATH=/app

EXPOSE 8000

# Run the application as the newly created user
USER django_user
CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
