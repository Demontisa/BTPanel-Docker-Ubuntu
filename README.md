### 使用方法
  `docker run -it --name=${ContainerName} -p ${bt_port}:8888 -p ${http_port}:80 -p ${https_port}:443 -p ${ftp_port}:21 -p ${mysql_port}:3306 demontisa/bt-ubuntu`
### 连接容器
  `docker exec -it ${ContainerName} bash`
### 登录宝塔面板
  `http://IP:${bt_port}`
##### 常见问题
 - 1、访问面板没反应
   - 解决方法：使用连接容器命令连接容器，输入`bt start`即可
 - 2、忘记用户名或者密码
   - 解决方法：使用连接容器命令连接容器，输入`bt`按照提示进行修改

### 给容器添加新的映射端口

#### 获取容器IP地址
- `docker inspect ${ContainerName} | grep IPAddress`

#### 添加端口转发
- `iptables -t nat -A  DOCKER -p tcp --dport 8001 -j DNAT --to-destination 172.17.0.3:8000`
  - 其中172.17.0.3:8000为你获取到的IP加你想要转发的端口号
  - 8001为你转发的端口号
