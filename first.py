# -*- coding: utf-8 -*-
import sys,os
panelPath = '/www/server/panel/'
os.chdir(panelPath)
sys.path.insert(0,panelPath + "class/")
import public,time,json
if sys.version_info[0] == 3: raw_input = input

#设置面板密码
def set_panel_pwd(password,ncli = False):
    import db
    sql = db.Sql()
    result = sql.table('users').where('id=?',(1,)).setField('password',public.md5(password))
    username = sql.table('users').where('id=?',(1,)).getField('username')
    if ncli:
        print("|-用户名: " + username);
        print("|-新密码: " + password);
    else:
        print(username)

#自签证书
def CreateSSL():
    import OpenSSL
    key = OpenSSL.crypto.PKey()
    key.generate_key( OpenSSL.crypto.TYPE_RSA, 2048 )
    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(0)
    cert.get_subject().CN = public.GetLocalIp();
    cert.set_issuer(cert.get_subject())
    cert.gmtime_adj_notBefore( 0 )
    cert.gmtime_adj_notAfter( 10*365*24*60*60 )
    cert.set_pubkey( key )
    cert.sign( key, 'md5' )
    cert_ca = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    if len(cert_ca) > 100 and len(private_key) > 100:
        public.writeFile('ssl/certificate.pem',cert_ca)
        public.writeFile('ssl/privateKey.pem',private_key)
        print('success');
        return;
    print('error');

#创建文件
def CreateFiles(path,num):
    if not os.path.exists(path): os.system('mkdir -p ' + path);
    import time;
    for i in range(num):
        filename = path + '/' + str(time.time()) + '__' + str(i)
        open(path,'w+').close()

#字节单位转换
def ToSize(size):
    ds = ['b','KB','MB','GB','TB']
    for d in ds:
        if size < 1024: return str(size)+d;
        size = size / 1024;
    return '0b';

#随机面板用户名
def set_panel_username(username = None):
    import db
    sql = db.Sql()
    if username:
        if len(username) < 5:
            print("|-错误，用户名长度不能少于5位")
            return;
        if username in ['admin','root']:
            print("|-错误，不能使用过于简单的用户名")
            return;

        sql.table('users').where('id=?',(1,)).setField('username',username)
        print("|-新用户名: %s" % username)
        return;
    
    username = sql.table('users').where('id=?',(1,)).getField('username')
    if username == 'admin': 
        username = public.GetRandomString(8).lower()
        sql.table('users').where('id=?',(1,)).setField('username',username)
    print('username: ' + username)
    
#设定idc
def setup_idc():
    try:
        panelPath = '/www/server/panel'
        filename = panelPath + '/data/o.pl'
        if not os.path.exists(filename): return False
        o = public.readFile(filename).strip()
        c_url = 'http://www.bt.cn/api/idc/get_idc_info_bycode?o=%s' % o
        idcInfo = json.loads(public.httpGet(c_url))
        if not idcInfo['status']: return False
        pFile = panelPath + '/config/config.json'
        pInfo = json.loads(public.readFile(pFile))
        pInfo['brand'] = idcInfo['msg']['name']
        pInfo['product'] = u'与宝塔联合定制版'
        public.writeFile(pFile,json.dumps(pInfo))
        tFile = panelPath + '/data/title.pl'
        titleNew = (pInfo['brand'] + u'面板').encode('utf-8')
        if os.path.exists(tFile):
            title = public.readFile(tFile).strip()
            if title == '宝塔Linux面板' or title == '': 
                public.writeFile(tFile,titleNew)
                public.SetConfigValue('title',titleNew)
        else:
            public.writeFile(tFile,titleNew)
            public.SetConfigValue('title',titleNew)
        return True
    except:pass

#将插件升级到6.0
def update_to6():
    print("====================================================")
    print("正在升级插件...")
    print("====================================================")
    download_address = public.get_url()
    exlodes = ['gitlab','pm2','mongodb','deployment_jd','logs','docker','beta','btyw']
    for pname in os.listdir('plugin/'):
        if not os.path.isdir('plugin/' + pname): continue
        if pname in exlodes: continue
        print("|-正在升级【%s】..." % pname),
        download_url = download_address + '/install/plugin/' + pname + '/install.sh';
        to_file = '/tmp/%s.sh' % pname
        public.downloadFile(download_url,to_file);
        os.system('/bin/bash ' + to_file + ' install &> /tmp/plugin_update.log 2>&1');
        print("    \033[32m[成功]\033[0m")
    print("====================================================")
    print("\033[32m所有插件已成功升级到6.0兼容!\033[0m")
    print("====================================================")

#命令行菜单
def bt_cli(u_input = 0):
    raw_tip = "==============================================="
    if not u_input:
        print("===========检测到容器第一次运行，请按照编号修改用户名和密码==============")
        print("(1) 修改面板密码")
        print("(2) 修改面板用户名")
        print("(0) 取消")
        print(raw_tip)
        try:
            u_input = input("请输入命令编号：")
            if sys.version_info[0] == 3: u_input = int(u_input)
        except: u_input = 0

    nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,22,23,24,25]
    if not u_input in nums:
        print(raw_tip)
        print("已取消!")
        exit()

    print(raw_tip)
    print("正在执行(%s)..." % u_input)
    print(raw_tip)

    if u_input == 1:
        if sys.version_info[0] == 2:
            input_pwd = raw_input("请输入新的面板密码：")
        else:
            input_pwd = input("请输入新的面板密码：")
        set_panel_pwd(input_pwd.strip(),True)
    elif u_input == 2:
        if sys.version_info[0] == 2:
            input_user = raw_input("请输入新的面板用户名(>5位)：")
        else:
            input_user = input("请输入新的面板用户名(>5位)：")
        set_panel_username(input_user.strip())

if __name__ == "__main__":
    type = sys.argv[1];
    if type == 'root':
        set_mysql_root(sys.argv[2])
    elif type == 'panel':
        set_panel_pwd(sys.argv[2])
    elif type == 'username':
        set_panel_username()
    elif type == 'o':
        setup_idc()
    elif type == 'mysql_dir':
        set_mysql_dir(sys.argv[2])
    elif type == 'to':
        panel2To3()
    elif type == 'package':
        PackagePanel();
    elif type == 'ssl':
        CreateSSL();
    elif type == 'port':
        CheckPort();
    elif type == 'clear':
        ClearSystem();
    elif type == 'closelog':
        CloseLogs();
    elif type == 'update_to6':
        update_to6()
    elif type == "cli":
        clinum = 0
        if len(sys.argv) > 2: clinum = int(sys.argv[2])
        bt_cli(clinum)
    else:
        print('ERROR: Parameter error')