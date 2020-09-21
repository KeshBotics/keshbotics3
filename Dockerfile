# docker pull python:3.8.5
FROM python:3.8.5

EXPOSE 8445


# Create directory for application
RUN mkdir /usr/keshbotics3

RUN apt-get update -y

# supervisor installation &&
# create directory for child images to store configuration in
RUN apt-get -y install supervisor && \
  mkdir -p /var/log/supervisor && \
  mkdir -p /etc/supervisor/conf.d


# Install requirements.txt using pip3
# Copy requirements and install using pip3
RUN apt-get -y install python3-pip
COPY requirements.txt /usr/keshbotics3
WORKDIR /usr/keshbotics3
RUN pip3 install -r requirements.txt


# supervisor base configuration
# This file contains the instructions for starting the API, Async, and crontab modules
ADD supervisor.conf /etc/supervisor.conf


# Copy the source code
COPY . /usr/keshbotics3


# Starts the scripts defined in supervisor.conf
CMD ["supervisord", "-c", "/etc/supervisor.conf"]
