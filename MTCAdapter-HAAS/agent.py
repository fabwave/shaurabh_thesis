import xml.etree.cElementTree as ET
import serial, re, time,string, psycopg2, psycopg2.extras, sys, datetime
"""
information needed for setup:
1. HAAS serial setup
2. port and baudrate
3. change in parameters if any
4. uuid and name

"""
if True:
    if True:
        #verify the serial credentials
        ser=serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout = 1)
        #defining initial values
        sequence=1
        buffer_size=1000
        instanceID=1
        instance_check='OFF'
        date_initial=datetime.datetime.now().isoformat()
        columns,rows=7,1000
        data = [['' for x in range(columns)] for y in range(rows)]
        mac_status_in=''
        cut_status_in=''
        part_num_in=''
        prog_name_in=''
        sspeed_in=''
        coolant_in=''
        seq_first_in=''
        seq_first=''
        atime_in=''
        ctime_in=''
        yltime_in=''
        atime_seq=''
        ctime_seq=''
        yltime_seq=''
        date_atime=''
        date_ctime=''
        date_yltime=''
        atime=0
        ctime=0
        yltime=0
        mac_status=''
        cut_status=''
        part_num=''
        prog_name=''
        sspeed=''
        coolant=''
        date_mac_status=''
        date_cut_status=''
        date_part_num=''
        date_prog_name=''
        date_sspeed=''
        date_coolant=''
        mac_status_seq=''
        cut_status_seq=''
        part_num_seq=''
        prog_name_seq=''
        sspeed_seq=''
        coolant_seq=''
        time_in=''
        time_in_count=0
        time_in_at=''
        time_in_ct=''
        time_in_ylt=''
        xaxis_in=''
        date_xaxis=''
        xaxis_seq=''
        xaxis=''
        yaxis_in=''
        date_yaxis=''
        yaxis_seq=''
        yaxis=''
        zaxis_in=''
        date_zaxis=''
        zaxis_seq=''
        zaxis=''
        
        
        
    if False:
        print "Error: Check serial connection and the credentials!"

    
    while True:
        #MTConnect Adapter
        if True:
            print datetime.datetime.now()
            ser.write(b"Q500\r")
            status=ser.readline()
            if 'PART' in status:
                part_num=(re.findall(r"[-+]?\d*\.\d+|\d+",status.split(',')[-1])[0])
                if part_num!=part_num_in:
                    date_part_num=datetime.datetime.now().isoformat()
                    sequence+=1
                    part_num_seq=sequence
                    data=[['PartCount','pc',str(date_part_num),'PartCountAct',str(part_num_seq),'',str(part_num)]] + data[:-1]
                    if seq_first_in!=seq_first:
                        seq_first=sequence
                        seq_first_in=seq_first
                    part_num_in=part_num
                prog_name=status.split(',')[1]
                if prog_name!=prog_name_in:
                    date_prog_name=datetime.datetime.now().isoformat()
                    sequence+=1
                    if seq_first_in!=seq_first:
                        seq_first=sequence
                        seq_first_in=seq_first
                    prog_name_seq=sequence
                    prog_name_in=prog_name
                    data=[['Program','pgm',str(date_prog_name),'program',str(prog_name_seq),'',str(prog_name)]] + data[:-1]

            ser.write(b"Q600 3027\r")
            sspeed=ser.readline()
            try:
                sspeed=str(int(float(sspeed[15:(len(sspeed)-3)])))
                if len(sspeed)>0 and sspeed!=sspeed_in:
                    sequence+=1
                    if seq_first_in!=seq_first:
                        seq_first=sequence
                        seq_first_in=seq_first
                    date_sspeed=datetime.datetime.now().isoformat()
                    sspeed_seq=sequence
                    sspeed_in=sspeed
                    data=[['RotaryVelocity','cs',str(date_sspeed),'Srpm',str(sspeed_seq),'ACTUAL',str(sspeed)]] + data[:-1]
            except:
                sspeed=0

            ser.write(b"Q600 5041\r")
            xaxis=ser.readline()
            try:
                xaxis=str(float(xaxis[15:(len(xaxis)-3)]))
                if len(xaxis)>0 and xaxis!=xaxis_in:
                    sequence+=1
                    if seq_first_in!=seq_first:
                        seq_first=sequence
                        seq_first_in=seq_first
                    date_xaxis=datetime.datetime.now().isoformat()
                    xaxis_seq=sequence
                    xaxis_in=xaxis
                    data=[['Position','xp',str(date_xaxis),'Xabs',str(xaxis_seq),'ACTUAL',str(xaxis)]] + data[:-1]
            except:
                xaxis=0

            ser.write(b"Q600 5042\r")
            yaxis=ser.readline()
            try:
                yaxis=str(float(yaxis[15:(len(yaxis)-3)]))
                if len(yaxis)>0 and yaxis!=yaxis_in:
                    sequence+=1
                    if seq_first_in!=seq_first:
                        seq_first=sequence
                        seq_first_in=seq_first
                    date_xaxis=datetime.datetime.now().isoformat()
                    yaxis_seq=sequence
                    yaxis_in=yaxis
                    data=[['Position','yp',str(date_yaxis),'Yabs',str(yaxis_seq),'ACTUAL',str(yaxis)]] + data[:-1]
            except:
                yaxis=0

            ser.write(b"Q600 5043\r")
            zaxis=ser.readline()
            try:
                zaxis=str(float(zaxis[15:(len(zaxis)-3)]))
                if len(zaxis)>0 and zaxis!=zaxis_in:
                    sequence+=1
                    if seq_first_in!=seq_first:
                        seq_first=sequence
                        seq_first_in=seq_first
                    date_zaxis=datetime.datetime.now().isoformat()
                    zaxis_seq=sequence
                    zaxis_in=xaxis
                    data=[['Position','zp',str(date_zaxis),'Zabs',str(zaxis_seq),'ACTUAL',str(zaxis)]] + data[:-1]
            except:
                zaxis=0

            
            mac_status='ON'
            if status!='' and mac_status!=mac_status_in:
                sequence+=1
                if seq_first_in!=seq_first:
                    seq_first=sequence
                    seq_first_in=seq_first
                mac_status_seq=sequence
                date_mac_status=datetime.datetime.now().isoformat()
                instance_check='ON'
                mac_status_in=mac_status
                data=[['PowerState','pwr',str(date_mac_status),'power',str(mac_status_seq),'',str(mac_status)]] + data[:-1]
                if len(status)<3:
                    mac_status="OFF"
            elif status=='' and instance_check=='ON':
                mac_status='OFF'
                sequence+=1
                if seq_first_in!=seq_first:
                    seq_first=sequence
                    seq_first_in=seq_first
                mac_status_seq=sequence
                date_mac_status=datetime.datetime.now().isoformat()
                instance_check='OFF'
                instanceID+=1
                mac_status_in=mac_status
                data=[['PowerState','pwr',str(date_mac_status),'power',str(mac_status_seq),'',str(mac_status)]] + data[:-1]

            try:
                if mac_status=='ON':
                    cut_status=status.split(',')[status.split(',').index('PARTS')-1]

                    if 'FEED' in cut_status:
                        cut_status='INTERRUPTED'
                    elif 'IDLE' in cut_status:
                        cut_status='READY'
                    elif 'SINGBK' in cut_status:
                        cut_status='STOPPED'
                    elif 'ALARM' in cut_status:
                        cut_status='EMERGENCY STOP'

                    
            except:
                if len(status)<3:
                    mac_status="OFF"
                if mac_status=='ON':
                    cut_status='ACTIVE'
                    
            if cut_status!=cut_status_in:
                date_cut_status=datetime.datetime.now().isoformat()
                sequence+=1
                if seq_first_in!=seq_first:
                    seq_first=sequence
                    seq_first_in=seq_first
                cut_status_seq=sequence
                cut_status_in=cut_status
                if cut_status!='EMERGENCY STOP' and mac_status=="ON":
                    data=[['Execution','exec',str(date_cut_status),'execution',str(cut_status_seq),'',str(cut_status)]] + data[:-1]
                elif mac_status=="ON":
                    data=[['EmergencyStop','estop',str(date_cut_status),'estop',str(cut_status_seq),'',str(cut_status)]] + data[:-1]

                elif mac_status=="OFF":
                    data=[['EmergencyStop','estop',str(date_cut_status),'estop',str(cut_status_seq),'','']] + data[:-1]

            MTConnectAdapter="Running"
            
        if False:
            MTConnectAdapter="Error"
            print "Error with Adapter!"

        

        #MTconnect Agent
        if True:
            # and ser.isOpen()==True check
            if MTConnectAdapter=="Running":
                #time initialization
                if mac_status=='ON':
                    ylt2=datetime.datetime.now()
                    if cut_status=='ACTIVE' and int(float(sspeed))>0:
                        ct2=datetime.datetime.now()
                    else:
                        ct1=datetime.datetime.now()
                    if (cut_status=='ACTIVE' or cut_status=='INTERRUPTED' or cut_status=='STOPPED'):
                        at2=datetime.datetime.now()
                    else:
                        at1=datetime.datetime.now()
                else:
                    ylt1=datetime.datetime.now()


                #root element
                root=ET.Element("MTConnectStreams")
                root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
                #Header Element
                Header=ET.SubElement(root,"Header")
                creationTime=datetime.datetime.now()
                creationTime=creationTime.isoformat()+'Z'
                Header.attrib['creationTime']=creationTime
                Header.attrib['sender']='MTC_HAAS'
                Header.attrib['bufferSize']=str(buffer_size)
                
                Header.attrib['instanceID']=str(instanceID)
                Header.attrib['version']='1.3'
                
                seq_first_in=''
                #stream element
                Streams=ET.SubElement(root,"Streams")
                #DeviceStream element
                DeviceStream=ET.SubElement(Streams,"DeviceStream")
                DeviceStream.attrib['uuid']='VF2-1103225'
                DeviceStream.attrib['name']='HAAS-VF2'
                #Component Stream for rotary
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Rotary'
                ComponentStream.attrib['name']='C'
                ComponentStream.attrib['componentId']='c1'
                #Sample for Rotary
                #Rotary Velocity
                Samples=ET.SubElement(ComponentStream,"Samples")
                RotaryVelocity=ET.SubElement(Samples,"RotaryVelocity")
                RotaryVelocity.text=str(sspeed)
                RotaryVelocity.attrib['dataItemId']='cs'
                RotaryVelocity.attrib['timestamp']=str(date_sspeed)
                RotaryVelocity.attrib['sequence']=str(sspeed_seq)
                RotaryVelocity.attrib['name']='Srpm'
                RotaryVelocity.attrib['subType']='Actual'

                #Component Stream for linear
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Linear'
                ComponentStream.attrib['name']='X'
                ComponentStream.attrib['componentId']='x'
                #Sample for linear
                #xaxis
                Samples=ET.SubElement(ComponentStream,"Samples")
                Linear=ET.SubElement(Samples,"Position")
                Linear.text=str(xaxis)
                Linear.attrib['dataItemId']='xp'
                Linear.attrib['timestamp']=str(date_xaxis)
                Linear.attrib['sequence']=str(xaxis_seq)
                Linear.attrib['name']='XAbs'
                Linear.attrib['subType']='Actual'

                #Component Stream for linear
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Linear'
                ComponentStream.attrib['name']='Y'
                ComponentStream.attrib['componentId']='y'
                #Sample for linear
                #yaxis
                Samples=ET.SubElement(ComponentStream,"Samples")
                Linear=ET.SubElement(Samples,"Position")
                Linear.text=str(yaxis)
                Linear.attrib['dataItemId']='yp'
                Linear.attrib['timestamp']=str(date_yaxis)
                Linear.attrib['sequence']=str(yaxis_seq)
                Linear.attrib['name']='YAbs'
                Linear.attrib['subType']='Actual'

                #Component Stream for linear
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Linear'
                ComponentStream.attrib['name']='Z'
                ComponentStream.attrib['componentId']='z'
                #Sample for linear
                #zaxis
                Samples=ET.SubElement(ComponentStream,"Samples")
                Linear=ET.SubElement(Samples,"Position")
                Linear.text=str(zaxis)
                Linear.attrib['dataItemId']='zp'
                Linear.attrib['timestamp']=str(date_zaxis)
                Linear.attrib['sequence']=str(zaxis_seq)
                Linear.attrib['name']='ZAbs'
                Linear.attrib['subType']='Actual'







                #Component Stream for controller
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Controller'
                ComponentStream.attrib['name']='controller'
                ComponentStream.attrib['componentId']='cont'
                #Sample for controller
                Events=ET.SubElement(ComponentStream,"Events")
                EmergencyStop=ET.SubElement(Events,"EmergencyStop")
                EmergencyStop.attrib['dataItemId']='estop'
                EmergencyStop.attrib['timestamp']=str(date_cut_status)
                EmergencyStop.attrib['sequence']=str(cut_status_seq)
                EmergencyStop.attrib['name']='estop'
                if cut_status=='EMERGENCY STOP':
                    EmergencyStop.text="TRIGGERED"
                elif mac_status=="ON":
                    EmergencyStop.text="ARMED"
                
                """
                #Component Stream for coolant
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Coolant'
                ComponentStream.attrib['name']='coolant'
                ComponentStream.attrib['componentId']='coolant'
                #Sample for coolant
                Samples=ET.SubElement(ComponentStream,"Samples")
                Coolant=ET.SubElement(Samples,"Coolant")
                Coolant.text=str(coolant)
                Coolant.attrib['dataItemId']='coollevel'
                Coolant.attrib['timestamp']=str(date_coolant)
                Coolant.attrib['sequence']=str(coolant_seq)
                Coolant.attrib['name']='coolant_level'
                """

                #Component Stram for power
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Electric'
                ComponentStream.attrib['name']='electric'
                ComponentStream.attrib['componentId']='elec'
                #Sample for power
                Samples=ET.SubElement(ComponentStream,"Samples")
                PowerState=ET.SubElement(Samples,"PowerState")
                PowerState.text=str(mac_status)
                PowerState.attrib['dataItemId']='pwr'
                PowerState.attrib['timestamp']=str(date_mac_status)
                PowerState.attrib['sequence']=str(mac_status_seq)
                PowerState.attrib['name']='power'

                #time finalization
                try:
                    if mac_status=='ON' and ylt1!=ylt2:
                        if time_in_ylt=='initialized':
                            yltime+=(ylt2-ylt1).total_seconds()
                            date_yltime=datetime.datetime.now().isoformat()
                            sequence+=1
                            yltime_seq=sequence
                            ylt1=ylt2
                            data=[['AccumulatedTime','yltime',str(date_yltime),'total_time',str(yltime_seq),'X:TOTAL',str(yltime)]] + data[:-1]
                        if cut_status=='ACTIVE' and int(float(sspeed))>0 and ct1!=ct2 and time_in_ct=='initialized':
                            ctime+=(ct2-ct1).total_seconds()
                            date_ctime=datetime.datetime.now().isoformat()
                            sequence+=1
                            ctime_seq=sequence
                            ct1=ct2
                            data=[['AccumulatedTime','ctime',str(date_ctime),'cut_time',str(ctime_seq),'X:CUT',str(ctime)]] + data[:-1]
                        if (cut_status=='ACTIVE' or cut_status=='INTERRUPTED' or cut_status=='STOPPED') and at1!=at2 and time_in_at=='initialized':
                            atime+=(at2-at1).total_seconds()
                            date_atime=datetime.datetime.now().isoformat()
                            sequence+=1
                            atime_seq=sequence
                            at1=at2
                            data=[['AccumulatedTime','atime',str(date_atime),'auto_time',str(atime_seq),'X:AUTO',str(atime)]] + data[:-1]
                except:
                    "Not initialized yet"
                        
                if mac_status=='ON' and time_in_count==0:
                    date_yltime=datetime.datetime.now().isoformat()
                    sequence+=1
                    yltime_seq=sequence
                    data=[['AccumulatedTime','yltime',str(date_yltime),'total_time',str(yltime_seq),'X:TOTAL',str(yltime)]] + data[:-1]
                    date_ctime=datetime.datetime.now().isoformat()
                    sequence+=1
                    ctime_seq=sequence
                    data=[['AccumulatedTime','ctime',str(date_ctime),'cut_time',str(ctime_seq),'X:CUT',str(ctime)]] + data[:-1]
                    date_atime=datetime.datetime.now().isoformat()
                    sequence+=1
                    atime_seq=sequence
                    data=[['AccumulatedTime','atime',str(date_atime),'auto_time',str(atime_seq),'X:AUTO',str(atime)]] + data[:-1]
                    time_in_count=1

                try:
                    if time_in_ylt=='':
                        ylt1=ylt2
                        time_in_ylt='initialized'
                    if time_in_ct=='':
                        ct1=ct2
                        time_in_ct='initialized'
                    if time_in_at=='':
                        at1=at2
                        time_in_at='initialized'
                        
                except:
                    "Next run"

                #Component Stream for path
                ComponentStream=ET.SubElement(DeviceStream,"ComponentStream")
                ComponentStream.attrib['component']='Path'
                ComponentStream.attrib['name']='path'
                ComponentStream.attrib['componentId']='path1'
                #Sample for path
                Samples=ET.SubElement(ComponentStream,"Samples")
                AccumulatedTime=ET.SubElement(Samples,"AccumulatedTime")
                AccumulatedTime.attrib['dataItemId']='atime'
                AccumulatedTime.text=str(int(atime))
                AccumulatedTime.attrib['timestamp']=str(date_atime)
                AccumulatedTime.attrib['sequence']=str(atime_seq)
                AccumulatedTime.attrib['name']='auto_time'
                AccumulatedTime.attrib['subType']='x:AUTO'
                

                AccumulatedTime2=ET.SubElement(Samples,"AccumulatedTime")
                AccumulatedTime2.attrib['dataItemId']='ctime'
                AccumulatedTime2.text=str(int(ctime))
                AccumulatedTime2.attrib['timestamp']=str(date_ctime)
                AccumulatedTime2.attrib['sequence']=str(ctime_seq)
                AccumulatedTime2.attrib['name']='cut_time'
                AccumulatedTime2.attrib['subType']='x:CUT'                

                
                AccumulatedTime3=ET.SubElement(Samples,"AccumulatedTime")
                AccumulatedTime3.attrib['dataItemId']='yltime'
                AccumulatedTime3.text=str(int(yltime))
                AccumulatedTime3.attrib['timestamp']=str(date_yltime)
                AccumulatedTime3.attrib['sequence']=str(yltime_seq)
                AccumulatedTime3.attrib['name']='total_time'
                AccumulatedTime3.attrib['subType']='x:TOTAL'


                #Event for path
                Events=ET.SubElement(ComponentStream,"Events")
                Execution=ET.SubElement(Events,"Execution")
                Execution.text=str(cut_status)
                Execution.attrib['dataItemId']='exec'
                Execution.attrib['timestamp']=str(date_cut_status)
                Execution.attrib['sequence']=str(cut_status_seq)
                Execution.attrib['name']='execution'

                
                PartCount=ET.SubElement(Events,"PartCount")
                PartCount.text=str(part_num)
                PartCount.attrib['dataItemId']='pc'
                PartCount.attrib['timestamp']=str(date_part_num)
                PartCount.attrib['sequence']=str(part_num_seq)
                PartCount.attrib['name']='PartCountAct'

                Program=ET.SubElement(Events,"Program")
                Program.text=str(prog_name)
                Program.attrib['dataItemId']='pgm'
                Program.attrib['timestamp']=str(date_prog_name)
                Program.attrib['sequence']=str(prog_name_seq)
                Program.attrib['name']='program'
                
                               
                   
                Header.attrib['lastSequence']=str(sequence)
                if sequence<=1000:
                    firstSequence=str(1)
                else:
                    firstSequence=str(sequence-buffer_size)

                Header.attrib['firstSequence']=str(firstSequence)

                nextSequence=str(sequence+1)
                
                Header.attrib['nextSequence']=str(nextSequence)
                                
                tree = ET.ElementTree(root)
                
                tree.write("current.xml",encoding='utf-8',xml_declaration=True)
        

                #sample
                data_int=open('data_interaction.txt','w')
                initiation_data=str(creationTime)+',MTC_HAAS,'+str(instanceID)+',1.3,'+str(buffer_size)+','+str(nextSequence)+','+str(firstSequence)+','+str(sequence)
                data_int.write(initiation_data)
                data_int.write('\n')
                for x in data:
                    for y in x:
                        y=str(y)
                        data_int.write(y)
                        data_int.write(',')
                    data_int.write('\n')
                data_int.close()
                #probe update
                probe = ET.parse('probe.xml')
                rootp = probe.getroot()
                rootp.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
                rootp[0].attrib['instanceId']=str(instanceID)
                rootp[0].attrib['creationTime']=str(creationTime)
                rootp[0].attrib['bufferSize']=str(buffer_size)
                probe=ET.ElementTree(rootp)
                probe.write('probe.xml',encoding='utf-8',xml_declaration=True)
                #asset update
                asset = ET.parse('asset.xml')
                roota = probe.getroot()
                roota.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
                roota[0].attrib['instanceId']=str(instanceID)
                roota[0].attrib['creationTime']=str(creationTime)
                roota[0].attrib['bufferSize']=str(buffer_size)
                asset=ET.ElementTree(roota)
                asset.write('asset.xml',encoding='utf-8',xml_declaration=True)

                
        if False:
                "Nothing"

if False:
    print "ERROR: RESTART!"
