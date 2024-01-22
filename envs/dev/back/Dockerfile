FROM python:3.11.4-bookworm

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y postgresql-client vim
WORKDIR /code

ENV PYTHONPATH=/code/app

COPY ./app/requirements-dev.txt ./app/requirements.txt
RUN CPUCOUNT=1 pip install -r ./app/requirements.txt

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install


ENTRYPOINT [ "bash", "-cl", "./envs/dev/back/back-start.sh" ]