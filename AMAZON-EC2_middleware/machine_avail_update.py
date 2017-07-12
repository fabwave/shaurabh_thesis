import psycopg2,datetime
conn=psycopg2.connect("host='testrun.cnw4f0shy3qa.us-east-1.rds.amazonaws.com' port=5432 dbname='testrun' user='testuser' password='helloworld'")
cur=conn.cursor()

conn2=psycopg2.connect("host='152.1.58.206' port=5432 dbname='postgres' user='postgres' password='ssr'")
cur2=conn2.cursor()
while True:
    day=str(datetime.datetime.today().weekday())
    cur.execute("SELECT time_begin,time_end from machine_sched where machine_name='HAAS-VF2' and day=%s;",(day,))
    sched=cur.fetchall()
    conn.commit()
    status_sched='scheduled to be idle'
    for x in sched:
        if datetime.datetime.now().isoformat()[10:]>x[0] and datetime.datetime.now().isoformat()[10:]<x[1]:
            status_sched='scheduled to be busy'


    cur2.execute("SELECT timestamp,cutting_status from login where machine_name='HAAS-VF2' order by timestamp desc limit 1")
    data=cur2.fetchall()
    conn2.commit()
    timestamp=data[0][0]
    status=data[0][1]
    
    if status=='READY':
        status='Machine is ON and READY.'
    elif status=='NA':
        status='Machine is OFF.'
    else:
        status='Machine is BUSY.'

    cur.execute("UPDATE machine_avail SET timestamp=%s, sched_status=%s,current_status=%s WHERE machine_name='HAAS-VF2';",(timestamp,status_sched,status))
    conn.commit()
    


    cur.execute("SELECT time_begin,time_end from machine_sched where machine_name='MAZAK-M7303290458' and day=%s;",(day,))
    sched=cur.fetchall()
    conn.commit()
    status_sched='scheduled to be idle'
    for x in sched:
        if datetime.datetime.now().isoformat()[10:]>x[0] and datetime.datetime.now().isoformat()[10:]<x[1]:
            status_sched='scheduled to be busy'

    cur2.execute("SELECT timestamp,cutting_status from login where machine_name='MAZAK-M7303290458' order by timestamp desc limit 1")
    data=cur2.fetchall()
    conn2.commit()
    timestamp=data[0][0]
    status=data[0][1]

    if status=='READY':
        status='Machine is ON and READY.'
    elif status=='NA':
        status='Machine is OFF.'
    else:
        status='Machine is BUSY.'

    cur.execute("UPDATE machine_avail SET timestamp=%s, sched_status=%s,current_status=%s WHERE machine_name='MAZAK-M7303290458';",(timestamp,status_sched,status))
    conn.commit()


    cur.execute("SELECT time_begin,time_end from machine_sched where machine_name='HAAS-VF3' and day=%s;",(day,))
    sched=cur.fetchall()
    conn.commit()
    status_sched='scheduled to be idle'
    timestamp=datetime.datetime.now().isoformat()
    status='Machine is OFF.'
    for x in sched:
        if datetime.datetime.now().isoformat()[10:]>x[0] and datetime.datetime.now().isoformat()[10:]<x[1]:
            status_sched='scheduled to be busy'
            status='Machine is BUSY.'
            timestamp=datetime.datetime.now().isoformat()[0:10]+x[0]+':00'
        timestamp2=datetime.datetime.now().isoformat()[0:10]+x[1]+':00'

    if status=='Machine is OFF.':
        timestamp=timestamp2

    cur.execute("UPDATE machine_avail SET timestamp=%s, sched_status=%s,current_status=%s WHERE machine_name='HAAS-VF3';",(timestamp,status_sched,status))
    conn.commit()


    cur.execute("SELECT time_begin,time_end from machine_sched where machine_name='BENCHMAN-4000' and day=%s;",(day,))
    sched=cur.fetchall()
    conn.commit()
    status_sched='scheduled to be idle'
    timestamp=datetime.datetime.now().isoformat()
    status='Machine is OFF.'
    for x in sched:
        if datetime.datetime.now().isoformat()[10:]>x[0] and datetime.datetime.now().isoformat()[10:]<x[1]:
            status_sched='scheduled to be busy'
            status='Machine is BUSY.'
            timestamp=datetime.datetime.now().isoformat()[0:10]+x[0]+':00'
        timestamp2=datetime.datetime.now().isoformat()[0:10]+x[1]+':00'

    if status=='Machine is OFF.':
        timestamp=timestamp2

    cur.execute("UPDATE machine_avail SET timestamp=%s, sched_status=%s,current_status=%s WHERE machine_name='BENCHMAN-4000';",(timestamp,status_sched,status))
    conn.commit()

    
    
