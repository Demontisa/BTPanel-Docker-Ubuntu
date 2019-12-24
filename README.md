### 使用方法
  `docker run -it --name=${ContainerName} -p ${port}:8888 -p ${port}:80 -p ${port}:443 -p ${port}:21 -p ${port}:3306 199476912/bt-ubuntu`
### 连接容器
  `docker exec -it ${ContainerName} bash`
### 查看宝塔面板安全入口及系统自动生成的账号密码
  `/etc/init.d/bt default`
