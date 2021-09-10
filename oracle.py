import cx_Oracle
co_sql = "select d.aqi_data,d.s_date from(select * from aqi d order by d.s_date desc)d where rownum<=9"
db = cx_Oracle.connect('phantom0518', 'phantom0308', '13.237.56.1:1521/ORCL')
cursor = db.cursor()
def get_co_oracle():

    data_list = []
    time_list = []
    cursor.execute(co_sql)
    data = cursor.fetchall()

    for i in data:
        data_list.append(i[0])
        time_list.append(i[1])
        print(i[0])
        print(i[1])

def get_temp_7day():
    temp_list=[]
    time_list=[]
    temp_sql='select * from temp where s_date>=sysdate-7'
    cursor.execute(temp_sql)
    data=cursor.fetchall()
    for data in data:
        temp_list.append(data[0])
        time_list.append(data[1])

    return  list(zip(temp_list, time_list))

def get_temp_Nday(day):

    temp_list = []
    time_list = []
    temp_sql = "select * from temp where to_char(s_date,'YYYY-MM-DD')='%s'" %day
    cursor.execute(temp_sql)
    data = cursor.fetchall()
    for data in data:
        temp_list.append(data[0])
        time_list.append(data[1])

    return list(zip(temp_list, time_list))

print(get_temp_Nday('2028-04-26') is  None)
data=get_temp_Nday('2028-04-26')


print(len(data))
