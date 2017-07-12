import psycopg2
conn=psycopg2.connect("host='testrun.cnw4f0shy3qa.us-east-1.rds.amazonaws.com' port=5432 dbname='testrun' user='testuser' password='helloworld'")
cur=conn.cursor()
"""
machine_specs
( machine_name varchar, machine_param varchar, units varchar, value varchar)
tool_specs
( machine_name varchar, tool_name varchar, tool_number varchar, tool_grade varchar, tool_dia varchar)
machine_sched
( machine_name varchar, day varchar, time_begin varchar, time_end varchar, job_description varchar)
machine_avail
(machine_name varchar, timestamp varchar, sched_status varchar, current_status varchar)
materials
proc_cap
machine_rank (machine_name varchar,rank varchar)
dime_sks_log
(timestamp varchar, status varchar, setupsheet varchar, material varchar, machine varchar, availability varchar,feedback varchar)

get all tables
cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='testrun'")

gettable characteristics
cur.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='materials';")

python -mtimeit  "l=[]" check speed

DO WE WANT MATERIAL FOR MASS?

cur.execute("INSERT INTO machine_specs (machine_name, machine_param, value) VALUES ('MAZAK-M7303290458','type','mill/turn');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','wt','kg','1020');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','travel_x','mm','450');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','travel_y','mm','220');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','travel_z','mm','900');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','rtsspeed','rpm','12000');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','feed','m/min','40');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','turn_dia','mm','500');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','turn_len','mm','850');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','turn_sspeed_1','rpm','2000');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','turn_sbore_1','mm','112');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','turn_sspeed_2','rpm','6000');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','turn_sbore_2','mm','61');")
cur.execute("INSERT INTO machine_specs VALUES ('MAZAK-M7303290458','tool_dia','mm','90');")


cur.execute("INSERT INTO machine_specs (machine_name,machine_param,value) VALUES ('HAAS-VF2','type','mill/turn');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','wt','kg','680');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','travel_x','mm','762');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','travel_y','mm','508');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','travel_z','mm','508');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','rtsspeed','rpm','15000');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','feed','m/min','35.6');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF2','tool_dia','mm','76');")


cur.execute("INSERT INTO machine_specs (machine_name,machine_param,value) VALUES ('HAAS-VF3','type','mill');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','wt','kg','794');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','travel_x','mm','1016');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','travel_y','mm','660');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','travel_z','mm','635');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','rtsspeed','rpm','15000');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','feed','m/min','35.6');")
cur.execute("INSERT INTO machine_specs VALUES ('HAAS-VF3','tool_dia','mm','76');")



cur.execute("INSERT INTO machine_specs (machine_name,machine_param,value) VALUES ('BENCHMAN-4000','type','mill');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','rtsspeed','rpm','5000');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','feed','m/min','5.08');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','tool_dia','mm','19.05');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','travel_x','mm','300');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','travel_y','mm','200');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','travel_z','mm','150');")
cur.execute("INSERT INTO machine_specs VALUES ('BENCHMAN-4000','wt','kg','20');")


cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','0','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','0','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','1','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','1','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','2','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','2','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','3','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','3','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','4','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('MAZAK-M7303290458','4','T13:00','T15:00','testing');")


cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','0','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','0','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','1','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','1','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','2','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','2','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','3','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','3','T13:00','T15:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','4','T09:00','T11:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF2','4','T13:00','T15:00','testing');")

cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','0','T10:00','T12:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','0','T14:00','T16:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','1','T10:00','T12:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','1','T14:00','T16:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','2','T10:00','T12:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','2','T14:00','T16:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','3','T10:00','T12:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','3','T14:00','T16:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','4','T10:00','T12:00','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('HAAS-VF3','4','T14:00','T16:00','testing');")

cur.execute("INSERT INTO machine_sched VALUES ('BENCHMAN-4000','0','T00:00','T00:01','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('BENCHMAN-4000','1','T00:00','T00:01','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('BENCHMAN-4000','2','T00:00','T00:01','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('BENCHMAN-4000','3','T00:00','T00:01','testing');")
cur.execute("INSERT INTO machine_sched VALUES ('BENCHMAN-4000','4','T00:00','T00:01','testing');")


conn.commit()

cur.execute("INSERT INTO materials VALUES ('stainless steel','7800');")
cur.execute("INSERT INTO materials VALUES ('aluminium','2700');")
cur.execute("INSERT INTO materials VALUES ('titanium','4500');")
cur.execute("INSERT INTO materials VALUES ('iron','7874');")
cur.execute("INSERT INTO materials VALUES ('copper','8950');")
cur.execute("INSERT INTO materials VALUES ('zinc','7135');")
cur.execute("INSERT INTO materials VALUES ('brass','8500');")
conn.commit()

cur.execute("INSERT INTO proc_cap VALUES ('drill','0.2','0.13');")
cur.execute("INSERT INTO proc_cap VALUES ('reaming','0.06','0.13');")
cur.execute("INSERT INTO proc_cap VALUES ('bore','0.05','0.05');")
conn.commit()
"""
