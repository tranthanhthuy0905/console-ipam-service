FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

#ENV HTTP_PROXY="http://172.25.211.30:3128"
#ENV HTTPS_PROXY="http://172.25.211.30:3128"
#ENV PIP_OPTIONS="--proxy $HTTP_PROXY"
# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
#RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
# Adds our application code to the image
COPY . code
RUN mv /code/mc /usr/bin/mc
RUN chmod +x /usr/bin/mc
WORKDIR code
EXPOSE 8880

# Run the production server
CMD gunicorn --bind 0.0.0.0:8880 --access-logfile - ep_ipam_api.wsgi:application