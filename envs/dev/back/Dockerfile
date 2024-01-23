FROM python:3.11.4-bookworm

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y postgresql-client vim
WORKDIR /code

ENV PYTHONPATH=/code/app

COPY ./app/requirements-dev.txt ./app/requirements.txt
RUN CPUCOUNT=1 pip install -r ./app/requirements.txt

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

ENTRYPOINT [ "bash", "-cl", "./envs/dev/back/back-start.sh" ]