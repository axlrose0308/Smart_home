#!/bin/python3
import paramiko
import time
import cx_Oracle

db = cx_Oracle.connect('phantom0518', 'phantom0308', '13.237.56.1:1521/ORCL')
cursor = db.cursor()


def ssh_pi_co_co2(ip,username,password,command):
    list =[]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8')

    out=out.rstrip('/n')
    list=out.split()
    cosql='insert into co(co_data) values(%s)' %list[1]
    co2sql='insert into co2(co2_data) values(%s)'%list[0]
    #print(list)
    print(cosql,list[1])
    print(co2sql,list[0])
    cursor.execute(cosql)
    cursor.execute(co2sql)
    cursor.execute('commit')
    time.sleep(3)


def ssh_pi_temp(ip,username,password,command):
    list =[]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8')


    list=out.split()
    tempsql='insert into humi(H_data) values(%s)' %list[0]
    humisql='insert into temp(t_data) values(%s)'%list[1]

    print(tempsql,list[0])
    print(humisql,list[1])
    cursor.execute(tempsql)
    cursor.execute(humisql)
    cursor.execute('commit')


def ssh_pi_aqi(ip,username,password,command):
    list =[]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode('utf-8')
    list=out.split()
    aqidata=(float(list[0])+float(list[1]))/2
    pm25sql='insert into pm25(pm25_data) values(%s)' %list[0]
    pm10sql='insert into pm10(pm10_data) values(%s)'%list[1]
    aqisql='insert into aqi(aqi_data) values(%s)'%aqidata

    print(pm25sql,list[0])
    print(pm10sql,list[1])
    print(aqisql,aqidata)
    cursor.execute(pm25sql)
    cursor.execute(pm10sql)
    cursor.execute(aqisql)
    cursor.execute('commit')

def runall():
    while True:
        ssh_pi_aqi('172.20.10.10','root','root','tail -1 /home/aqi/out.txt')
        ssh_pi_temp('172.20.10.10','root','root','tail -1 /home/FUN/tm.out')
        ssh_pi_co_co2('172.20.10.10', 'pi', 'root', 'tail -1 /home/pi/Desktop/co.out')
        time.sleep(3)

runall()

