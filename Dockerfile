FROM ubuntu:16.04
#指定运行目录
WORKDIR /root/

RUN apt-get update -y && apt-get install sudo wget -y

ADD install.sh install.sh

#运行脚本
RUN sudo bash install.sh

ADD bt baota
RUN cp /www/server/panel/tools.py /root/tools.py
ADD first.py /www/server/panel/tools.py

CMD sudo bash baota && /etc/init.d/bt start && bash --login

ADD tools.py /www/server/panel/tools.py