### 使用方法
  `docker run -it --name=${ContainerName} -p ${bt_port}:8888 -p ${http_port}:80 -p ${https_port}:443 -p ${ftp_port}:21 -p ${mysql_port}:3306 199476912/bt-ubuntu`
### 连接容器
  `docker exec -it ${ContainerName} bash`
### 登录宝塔面板
  `http://IP:${bt_port}`
