# select the base image (usually a language dependency)
# can search for images at Dockerhub
From python:3

# install any environmental/operating system variables here
## ENV PYTHONBUFFERED 1

# set the working directory in the container computer we want our app files to live
WORKDIR /app

# copy files from the host computer and where to copy it
COPY accounts accounts
COPY attendees attendees
COPY common common
COPY conference_go conference_go
COPY events events
COPY presentations presentations
COPY requirements.txt requirements.txt
COPY manage.py manage.py

# runs terminal commands before the app starts 
# (generally a good place to install language dependencies)
RUN pip install -r requirements.txt

# set the command that launches the docker container
CMD gunicorn --bind 0.0.0.0:8000 conference_go.wsgi


