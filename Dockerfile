# Use an official Python runtime as a parent image
FROM python:3.9


# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE leagueTable.settings


# Create and set the working directory
RUN mkdir /app
WORKDIR /app


# Copy the requirements file into the container at /app
COPY requirements.txt /app/


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# Copy the rest of the application code into the container
COPY . /app/