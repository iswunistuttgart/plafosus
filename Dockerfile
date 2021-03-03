FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# This one is required to install numpy.
RUN apk add g++
RUN pip install --upgrade pip

# Copy project.
COPY ./ /src
# Set work directory.
WORKDIR /src
# Install requirements.
RUN pip install -r requirements.txt
