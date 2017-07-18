FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/local/dragnet
COPY requirements.txt /usr/local/dragnet
WORKDIR /usr/local/dragnet
RUN pip3 install -r requirements.txt
COPY . /usr/local/dragnet
RUN mkdir /mnt/dragnet_data
RUN mkdir /mnt/declarations_bank
RUN mkdir /usr/local/dragnet/views
VOLUME ["/mnt/dragnet_data", "/mnt/declarations_bank", "/usr/local/dragnet/views"]
