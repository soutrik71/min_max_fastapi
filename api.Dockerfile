FROM python:3.10
WORKDIR /src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /src/requirements.txt
COPY ./app /src/app