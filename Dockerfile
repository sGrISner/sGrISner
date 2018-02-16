FROM ubuntu:16.04

RUN apt -y update
RUN apt -y upgrade

RUN apt install -y software-properties-common
RUN apt install -y build-essential

RUN add-apt-repository -y ppa:ubuntugis/ppa

RUN apt install -y python3 python3-pip python3-gdal
RUN apt install -y git

WORKDIR /home
RUN git clone https://github.com/sgrisner/sgrisner.git
WORKDIR sgrisner/
RUN pip3 install -r requirements.txt
RUN ./setup.py install
