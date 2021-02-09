FROM ubuntu:18.04
#指定运行目录
WORKDIR /root/

RUN apt-get update -y && apt-get install sudo wget -y

ADD install.sh install.sh

#运行脚本
RUN sudo bash install.sh && cp /www/server/panel/tools.py /root/tools.py

ADD bt baota
ADD first.py /www/server/panel/first.py
CMD sudo bash baota && sudo bash baota && rm -f /www/server/panel/data/admin_path.pl && /etc/init.d/bt start && bash --login
