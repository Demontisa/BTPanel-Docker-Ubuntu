### 使用方法
  `docker run -it --name=${ContainerName} -p ${bt_port}:8888 -p ${http_port}:80 -p ${https_port}:443 -p ${ftp_port}:21 -p ${mysql_port}:3306 199476912/bt-ubuntu`
### 连接容器
  `docker exec -it ${ContainerName} bash`
### 登录宝塔面板
  `http://IP:${bt_port}`
##### 常见问题
 - 1、访问面板没反应
  - 解决方法：使用连接容器命令连接容器，输入`bt start`即可
 - 2、忘记用户名或者密码
  - 解决方法：使用连接容器命令连接容器，输入`bt`按照提示进行修改
