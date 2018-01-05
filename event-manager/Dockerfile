FROM python:3.6.1

# Initialize
RUN mkdir -p /data/event-manager
WORKDIR /data/event-manager

COPY requirementss.txt /data/event-manager/

# Setup

COPY requirements.txt /data/event-manager/
RUN pip3 install -r requirements.txt

#saving build time

RUN pip3 install -r requirementss.txt

# Prepare
COPY . /data/event-manager/
RUN mkdir -p mydjango/static/admin
