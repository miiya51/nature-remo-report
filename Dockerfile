FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales  &&\
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip
RUN pip install --upgrade nature-remo
RUN pip install --upgrade requests
RUN pip install --upgrade urllib3
RUN pip install --upgrade sqlalchemy
RUN pip install --upgrade psycopg2
RUN pip install --upgrade schedule
CMD ["python", "-u", "/root/src/remo_extract.py"]