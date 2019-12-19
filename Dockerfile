FROM ubuntu:16.04

WORKDIR /root/

RUN apt-get update -y && apt-get install sudo wget -y
ADD install.sh install.sh

RUN sudo bash install.sh
