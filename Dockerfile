FROM ubuntu:18.04

USER root
RUN apt update

# Install python3
RUN apt install -y python3-dev python3-pip

# Install requirements
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

RUN python3 -m nltk.downloader punkt
RUN python3 -m spacy download en_core_web_md
