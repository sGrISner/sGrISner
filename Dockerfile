FROM ubuntu:16.04

RUN apt -y update
RUN apt -y upgrade

RUN apt install -y python3 python3-pip
RUN apt install -y git
WORKDIR /home
RUN git clone https://github.com/sgrisner/sgrisner.git
WORKDIR sgrisner/
RUN pip3 install -r requirements.txt
RUN chmod a+x ./setup.py
RUN ./setup.py install
