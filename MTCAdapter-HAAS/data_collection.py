import xml.etree.ElementTree as ET
import psycopg2,re
#inputs-constant
#------------------
cutting_status_in='NA'
cutting_status=''
macoff=0
serial_number=1
#------------------

#define server input parameters here
#---------------------
host='13.84.183.46'
port=5432
dbname='ncstate'
user='ncstate'
password='ohToapiegei7'
#---------------------
con="""host='"""+str(host)+"""' port="""+str(port)+""" dbname='"""+str(dbname)+"""' user='"""+str(user)+"""' password='"""+str(password)+"""'"""
conn=psycopg2.connect(con)
cur=conn.cursor()    
while True:
    try:
        
        tree = ET.parse('current.xml')
        root = tree.getroot()

        for a in root.iter('PowerState'):
            machine_status=a.text
        
    
        for x in root.iter('DeviceStream'):
            machine_name=x.attrib['name']
            uuid=x.attrib['uuid']
    
        for x in root.iter('Execution'):
            timestamp=x.attrib['timestamp']
            cutting_status=x.text
    
        if machine_status=='ON' and cutting_status!=cutting_status_in:
            part_name='NA'
                          
            for x in root.iter('PartCount'):
                part_number=x.text
    
            for x in root.iter('Program'):
                program_number=x.text
    
            cutting_status_in=cutting_status
    
            macoff=0
            
            serial_number+=1
    
            conn.rollback()
            cur.execute("INSERT INTO login VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(str(uuid)+": "+str(serial_number),str(timestamp),str(machine_name),str(machine_status),str(cutting_status),str(part_number),str(program_number),str(part_name)))
            conn.commit()
    
    
        if machine_status!='ON' and macoff==0:
            machine_status=='OFF'
            
            for a in root.iter('PowerState'):
                timestamp=a.attrib['timestamp']
    
            cutting_status='NA'
            
            part_number='NA'
    
            program_number='NA'
    
            part_name='NA'
    
            macoff=1
    
            serial_number+=1
    
            conn.rollback()
            cur.execute("INSERT INTO login VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(str(uuid)+": "+str(serial_number),str(timestamp),str(machine_name),str(machine_status),str(cutting_status),str(part_number),str(program_number),str(part_name)))
            conn.commit()
    

        if machine_status=='ON' and cutting_status=='ACTIVE':
            for x in root.iter('Header'):
                creationTime=x.attrib['creationTime']
    
            for x in root.iter('Samples'):
                for y in x:
                    try:
                        dataitemId=y.attrib['dataItemId']
                    except:
                        dataitemId=''
                    try:
                        sequence=y.attrib['sequence']
                    except:
                        sequence=''
                    try:
                        timestamp=y.attrib['timestamp']
                    except:
                        timestamp=''
                    try:
                        name=y.attrib['name']
                    except:
                        name=''
                    try:
                        param=str(y).split(' ')[1]
                    except:
                        param=''
                    
                    text=y.text
                    if "Accumulated" not in param:
                        conn.rollback()
                        cur.execute("INSERT INTO componentstream VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",(str(part_number),str(machine_name),str(creationTime),str(param),str(sequence),str(timestamp),str(dataitemId),str(name),str(text)))
                        conn.commit()
                    macoff=0
        
                
    except:
        "Rerun"


