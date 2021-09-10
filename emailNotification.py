import  time
import cx_Oracle
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


db = cx_Oracle.connect('phantom0518', 'phantom0308', '13.237.56.1:1521/ORCL')
cursor = db.cursor()



def mail(content,subject,receiver):
    # sender's email
    my_sender = 'stradlin0518@gmail.com'
    # sender's password
    my_pass = 'phantom0518'
    # receiver's address
    my_user = receiver
    ret = True

    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        # sender's username, email
        msg['From'] = formataddr(["Smart Home System", my_sender])
        # receiver's username, email
        msg['To'] = formataddr(["User", my_user])
        # emial subject
        msg['Subject'] = subject

        # SMTP servier, port 465
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # sender's email and password
        server.login(my_sender, my_pass)
        # sender's email, receiver's email
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        # conncection terminate
        server.quit()
    except Exception:
        ret = False
    return ret



def AQiNotification():
    if get_aqi()[0] > 150:
        mail('Your current AQI is %s Please Be Aware ' % get_aqi()[0], 'Please Be Aware Your current AQI is %s' % get_aqi()[0],
             'stradlin0518@gmail.com')
def humiNotification():
    if get_humi()[0]>75 or get_humi()[0]<15:
        mail('Your current Humidity is %s' % get_humi()[0], 'Please Be Aware Your current Humidity is %s' % get_humi()[0],
             'stradlin0518@gmail.com')

def tempNotification():
    if get_temp()[0]>35 or get_temp()[0]<5:
        mail('Your current TEMPERATURE is %s Please Be Aware' % get_temp()[0],
            'Please Be Aware Your current TEMPERATURE is %s' % get_temp()[0],
            'stradlin0518@gmail.com')

def pm25Notification():
    if get_pm25()[0]>150:
        mail('Your current PM2.5 is %s Please Be Aware' % get_pm25()[0],
             'Please Be Aware Your current PM2.5 is %s' % get_pm25()[0],
             'stradlin0518@gmail.com')
def pm10Notification():
    if get_pm10()[0]>150:
        mail('Your current PM10 is %s Please Be Aware' % get_pm10()[0],
             'Please Be Aware Your current PM10 is %s' % get_pm10()[0],
             'stradlin0518@gmail.com')
def coNotification():
    if get_co()[0]>10:
        mail('Your current CO is %s Please Be Aware' % get_co()[0],
             'Please Be Aware Your current CO is %s' % get_co()[0],
             'stradlin0518@gmail.com')
def co2Notification():
    if get_co2()[0]>450:
        mail('Your current CO2 is %s Please Be Aware' % get_co2()[0],
             'Please Be Aware Your current CO2 is %s' % get_co2()[0],
             'stradlin0518@gmail.com')


co_sql = "select a.co_data,to_char(a.s_date,'mm-dd HH24:MI') from (select * from co a order by a.s_date desc)a where rownum<=9"

def get_co():
    data_list = []
    cursor.execute(co_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])

    return data_list


co2_sql = "select b.co2_data,to_char(b.s_date,'mm-dd HH24:MI') from(select * from co2 b order by b.s_date desc)b where rownum<=9"
def get_co2():
    data_list = []
    cursor.execute(co2_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])
    return data_list

pm10_sql = "select g.pm10_data,to_char(g.s_date,'mm-dd HH24:MI') from(select * from pm10 g order by g.s_date desc)g where rownum<=9"

def get_pm10():
    data_list = []

    cursor.execute(pm10_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])


    return data_list

pm25_sql = "select f.pm25_data,to_char(f.s_date,'mm-dd HH24:MI') from (select * from pm25 f order by f.s_date desc)f where rownum<=9"

def get_pm25():
    data_list = []
    cursor.execute(pm25_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])

    return data_list






aqi_sql="select d.aqi_data,to_char(d.s_date,'MM-DD HH24:MI') from(select * from aqi d order by d.s_date desc)d where rownum<=9"

def get_aqi():
    data_list = []
    cursor.execute(aqi_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])
        #
    return data_list


temp_sql = "select e.t_data,to_char(e.s_date,'mm-dd HH24:MI') from(select * from temp e order by e.s_date desc)e where rownum<=9"
def get_temp():
    data_list = []
    cursor.execute(temp_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])
    return data_list


humi_sql="select c.h_data,to_char(c.s_date,'mm-dd HH24:MI') from(select * from humi c order by c.s_date desc)c where rownum<=9"
def get_humi():
    data_list = []
    cursor.execute(humi_sql)
    data = cursor.fetchall()
    for i in data:
        data_list.append(i[0])
        #humi_time_list.append(i[1])
    return data_list








def testemail():

    while True:
        AQiNotification()
        co2Notification()
        coNotification()
        humiNotification()
        pm10Notification()
        pm25Notification()
        tempNotification()
        time.sleep(20)



testemail()
print('Email Notification Mode On')