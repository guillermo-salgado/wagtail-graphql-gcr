# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV PORT 8080
ENV APP_HOME /app

# Copy local code to the container image.
WORKDIR $APP_HOME
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn

# RUN python manage.py migrate

RUN useradd wagtail
RUN chown -R wagtail /app
USER wagtail

EXPOSE $PORT
CMD exec gunicorn cms.wsgi:application --bind 0.0.0.0:$PORT --workers 3
