
import xml.etree.cElementTree as ET
import serial, re, time,string, sys, datetime
"""
a='/sample?count=45'
b=a.split('?')
if len(b)==2:
    if b[0]=="/sample" and bool(re.match('count=[0-9]+',b[1])):
        DATA_COUNT=int(b[1].split('=')[1])
"""

if True:
    
    #constants
    count_path=0
    count_acc=0
    count_exec=0
    count_pgm=0
    count_pc=0
    count_con=0
    count_rot=0
    count_pow=0
    
    data_dict=open('data_interaction.txt','r')
    data_interaction=data_dict.readlines()

    header_elements=data_interaction[0].split(',')
    
    root=ET.Element("MTConnectStreams")
    root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
    #Header Element
    Header=ET.SubElement(root,"Header")
    creationTime=datetime.datetime.now()
    creationTime=creationTime.isoformat()+'Z'
    Header.attrib['creationTime']=header_elements[0]
    Header.attrib['sender']=header_elements[1]
    Header.attrib['bufferSize']=header_elements[4]
    Header.attrib['firstSequence']=header_elements[6]
    Header.attrib['lastSequence']=header_elements[7]
    Header.attrib['nextSequence']=header_elements[5]
    Header.attrib['instanceID']=header_elements[2]
    Header.attrib['version']=header_elements[3]
    

    #stream element
    Streams=ET.SubElement(root,"Streams")
    #DeviceStream element
    DeviceStream=ET.SubElement(Streams,"DeviceStream")
    DeviceStream.attrib['uuid']='VF2-1103225'
    DeviceStream.attrib['name']='HAAS-VF2'

    
    for x in data_interaction[1+FROM_COUNT:DATA_COUNT+1]:
        if len(x)<20:
            break

        y=x.split(',')
        

        if count_path==0 and (y[0]=="AccumulatedTime" or y[0]=="Execution" or y[0]=="PartCount" or y[0]=="Program"):
            #Component Stream for path
            ComponentStream_path=ET.SubElement(DeviceStream,"ComponentStream")
            ComponentStream_path.attrib['component']='Path'
            ComponentStream_path.attrib['name']='path'
            ComponentStream_path.attrib['componentId']='path1'
            count_path=1

        if  count_acc==0 and y[0]=="AccumulatedTime":
            #Sample for path
            Samples_path=ET.SubElement(ComponentStream_path,"Samples")
            count_acc=1
        
        if y[0]=="AccumulatedTime":
            AccumulatedTime=ET.SubElement(Samples_path,"AccumulatedTime")
            AccumulatedTime.attrib['dataItemId']=y[1]
            AccumulatedTime.text=y[6]
            AccumulatedTime.attrib['timestamp']=y[2]
            AccumulatedTime.attrib['sequence']=y[4]
            AccumulatedTime.attrib['name']=y[3]
            AccumulatedTime.attrib['subType']=y[5]            
            

        if (y[0]=="Execution" or y[0]=="PartCount" or y[0]=="Program") and count_exec==0:
            #Event for path
            Events_path=ET.SubElement(ComponentStream_path,"Events")
            count_exec=1

            
        if y[0]=="Execution":
            Execution=ET.SubElement(Events_path,"Execution")
            Execution.text=y[6]
            Execution.attrib['dataItemId']=y[1]
            Execution.attrib['timestamp']=y[2]
            Execution.attrib['sequence']=y[4]
            Execution.attrib['name']=y[3]
            

        if y[0]=="PartCount":
            PartCount=ET.SubElement(Events_path,"PartCount")
            PartCount.text=y[6]
            PartCount.attrib['dataItemId']=y[1]
            PartCount.attrib['timestamp']=y[2]
            PartCount.attrib['sequence']=y[4]
            PartCount.attrib['name']=y[3]

        if y[0]=="Program":
            Program=ET.SubElement(Events_path,"Program")
            Program.text=y[6]
            Program.attrib['dataItemId']=y[1]
            Program.attrib['timestamp']=y[2]
            Program.attrib['sequence']=y[4]
            Program.attrib['name']=y[3]

        if count_pow==0 and y[0]=="PowerState":
            #Component Stream for power
            ComponentStream_pow=ET.SubElement(DeviceStream,"ComponentStream")
            ComponentStream_pow.attrib['component']='Electric'
            ComponentStream_pow.attrib['name']='electric'
            ComponentStream_pow.attrib['componentId']='elec'
            #Sample for power
            Samples_pow=ET.SubElement(ComponentStream_pow,"Samples")
            count_pow=1

        if y[0]=="PowerState":
            PowerState=ET.SubElement(Samples_pow,"PowerState")
            PowerState.text=y[6]
            PowerState.attrib['dataItemId']=y[1]
            PowerState.attrib['timestamp']=y[2]
            PowerState.attrib['sequence']=y[4]
            PowerState.attrib['name']=y[3]

        if count_con==0 and y[0]=="EmergencyStop":
            #Component Stream for controller
            ComponentStream_con=ET.SubElement(DeviceStream,"ComponentStream")
            ComponentStream_con.attrib['component']='Controller'
            ComponentStream_con.attrib['name']='controller'
            ComponentStream_con.attrib['componentId']='cont'
            #Sample for controller
            Events_con=ET.SubElement(ComponentStream_con,"Events")
            count_con=1

        if y[0]=="EmergencyStop":
            EmergencyStop=ET.SubElement(Events_con,"EmergencyStop")
            EmergencyStop.attrib['dataItemId']=y[1]
            EmergencyStop.attrib['timestamp']=y[2]
            EmergencyStop.attrib['sequence']=y[4]
            EmergencyStop.attrib['name']=y[3]
            EmergencyStop.text=y[6]

        if count_rot==0 and y[0]=="RotaryVelocity":
            #Component Stream for rotary
            ComponentStream_rot=ET.SubElement(DeviceStream,"ComponentStream")
            ComponentStream_rot.attrib['component']='Rotary'
            ComponentStream_rot.attrib['name']='C'
            ComponentStream_rot.attrib['componentId']='c1'
            #sample for rotary
            Samples_rot=ET.SubElement(ComponentStream_rot,"Samples")
            count_rot=1
        
        if y[0]=="RotaryVelocity":
            RotaryVelocity=ET.SubElement(Samples_rot,"RotaryVelocity")
            RotaryVelocity.text=y[6]
            RotaryVelocity.attrib['dataItemId']=y[1]
            RotaryVelocity.attrib['timestamp']=y[2]
            RotaryVelocity.attrib['sequence']=y[4]
            RotaryVelocity.attrib['name']=y[3]
            RotaryVelocity.attrib['subType']=y[5]
         
    tree = ET.ElementTree(root)
    
    tree.write("sample2.xml",encoding='utf-8',xml_declaration=True)
