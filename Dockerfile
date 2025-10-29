# Mostly just following the steps at https://hub.docker.com/_/python/
# Adapting only as needed
FROM docker.io/python:3.13-slim

WORKDIR /usr/src/app

# Install dependencies using frozen to avoid breakages from updates
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copying just the two files I need
COPY main.py SolarManager.py config.toml ./
CMD [ "python", "./main.py" ]
