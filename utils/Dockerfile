FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/local/dragnet
COPY requirements.txt /usr/local/dragnet
WORKDIR /usr/local/dragnet
RUN pip3 install -r requirements.txt
COPY . /usr/local/dragnet

