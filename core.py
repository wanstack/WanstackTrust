# coding:utf-8
"""
功能介绍: 主要是用paramiko做ssh key的连接测试，然后使用pexpect做生成公钥并拷贝到对应node节点上
yum install python-pip
pip install pexpect
pip install paramiko
"""

import paramiko
import pexpect,os
from conf import file_path,user,passwd
from conf import hosts
file = file_path + 'id_rsa'
file_pub = file_path + 'id_rsa.pub'

def ssh_trust(ip,username,password):
    try:
        pkey=file
        key=paramiko.RSAKey.from_private_key_file(pkey)
        s=paramiko.SSHClient()
        s.load_system_host_keys()
        s.connect(hostname =ip,port=22,username=username,pkey=key,timeout=1)
        stdin,stdout,stderr=s.exec_command('echo "Mutual trust has been successful"')
        print stdout.read()
    except:
        print('Begin to build mutual trust')
        cmd = 'ssh-copy-id -o StrictHostKeyChecking=no -i %s %s@%s' %(file_pub,username,ip)
        child = pexpect.spawn(cmd)
        child.expect(['password:'])
        child.sendline(password)
        print child.before
        child.interact()
        # child.close(force=True)
def exec_trust(ip,username,password):
    if os.path.exists(file_path) and os.path.exists(file_pub):
        os.system('rm -rf %s' % file_path)
        print('Create a public key')
        os.system('mkdir -p %s' %file_path)
        cmd = "ssh-keygen  -t rsa -N '' -f %s -P '' " %(file)
        os.system(cmd)
        os.system('chown -R %s.%s %s' %(username,username,file_path))
        ssh_trust(ip,username,password)


def parse_conf(hosts):
    with open('ip_list','w') as f:
        for k,v in hosts.items():
            f.write("%s\n" %hosts[k]['ip'])

def run():
    for k,v in hosts.items():
        exec_trust(ip = hosts[k]['ip'],username=user,password=passwd)









