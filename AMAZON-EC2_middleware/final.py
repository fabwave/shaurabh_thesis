
import psycopg2, boto3, re, datetime,BeautifulSoup,urllib,time
import xml.etree.ElementTree as ET

const1='once' #const to check a process isnt repeated infinitely

if True:
    #connect to the AWS RDS postgres instance
    conn=psycopg2.connect("host='testrun.cnw4f0shy3qa.us-east-1.rds.amazonaws.com' port=5432 dbname='testrun' user='testuser' password='helloworld'")
    cur=conn.cursor()
    
    #connect to NCSU RedHat system's postgres instance
    conn2=psycopg2.connect("host='152.1.58.206' port=5432 dbname='postgres' user='postgres' password='ssr'")
    cur2=conn2.cursor()
    print time.clock()
    if True:
        conn.rollback()
        conn2.rollback()
        #check status for inputs from DOME platform
        cur.execute("SELECT * FROM dime_sks_log ORDER BY timestamp DESC;")
        status=cur.fetchall()
        conn.commit()
        print time.clock()
        if 'DOME' in status[0][1]:
            feedback=''
            #after verifying inputs start the comparisons
            html='https://s3.amazonaws.com/ncsudome/turning.html' #status[0][2]
            material=status[0][3]
            #first converting html to xml: this makes it easier to travel through the data
            f=urllib.urlopen(html)
            a=f.read()
            a=a.replace('&','NA')
            g=open('setupsheet.html','w')
            g.write(a)
            f.close()
            g.close()
            g=open('setupsheet.html')
            soup=BeautifulSoup.BeautifulSoup(g)
            g.close()
            h=open('setupsheet.xml','w')
            print >> h,soup.prettify()
            h.close()
            print time.clock()
            #collect data from this xml tree
            tree=ET.parse('setupsheet.xml')
            root=tree.getroot()
            part_dict={}
            DX=root[1][3][1][0][0][1][0][2].text
            #maximum x,y,z range of stock
            maxx=re.findall(r"[-+]?\d*\.\d+|\d+",DX)[0]
            maxy=re.findall(r"[-+]?\d*\.\d+|\d+",root[1][3][1][0][0][1][0][4].text)[0]
            maxz=re.findall(r"[-+]?\d*\.\d+|\d+",root[1][3][1][0][0][1][0][6].text)[0]
            if 'in' in DX:
                units=25.4
            elif 'mm' in DX:
                units=1
            else:
                units=1
                
            part_dict['stock']=[str(units*float(maxx)),str(units*float(maxy)),str(units*float(maxz))]
            #maximum rapid feed,spindlespeed and estimated cycletime
            maxfeed=re.findall(r"[-+]?\d*\.\d+|\d+",root[1][5][1][0][0][5][0][1].text)[0]
            maxsspeed=re.findall(r"[-+]?\d*\.\d+|\d+",root[1][5][1][0][0][6][0][1].text)[0]
            ctms=re.findall(r"[-+]?\d*\.\d+|\d+",root[1][5][1][0][0][9][0][1].text)
            cycletime=0

            for x in range(0,len(ctms)):
                cycletime+=(60**(len(ctms)-x-1))*float(ctms[x])

            part_dict['rapid feed']=str(units*float(maxfeed))
            part_dict['spindle speed']=str(maxsspeed)
            part_dict['cycle time']=str(cycletime)


            #process details includind type,diameter and tolerance
            cnt=1
            tool_dict={}
            process='unknown'
            aroot=root[1][7].findall('.//div')
            for ind,div in enumerate(aroot):
                if 'Tolerance' in div.text:
                    Tol= re.findall(r"[-+]?\d*\.\d+|\d+",aroot[ind+1].text)[0]
        
                if 'Type' in div.text:
                    Type= re.sub(' +',' ',aroot[ind+1].text)
                    Type= re.sub('\n','',Type)
                    Type=str(cnt)+Type
                    cnt+=1
                    if 'mill' in aroot[ind+1].text:
                        process='milling'
                    elif 'turn' in aroot[ind+1].text:
                        process='turning'
        
                if 'Diameter' in div.text:
                    Dia= re.findall(r"[-+]?\d*\.\d+|\d+",aroot[ind+1].text)[0]

                if 'Length' in div.text:
                    Len= re.findall(r"[-+]?\d*\.\d+|\d+",aroot[ind+1].text)[0]
                    tool_dict[Type]=[str(units*float(Tol)), str(units*float(Len)), str(units*float(Dia))]
            print time.clock()


            
            #listing all machines
            cur.execute("SELECT DISTINCT machine_name FROM machine_specs ORDER BY machine_name DESC;")
            machines=cur.fetchall()
            cur.execute("SELECT DISTINCT machine_name FROM machine_specs WHERE value like '%turn%' ORDER BY machine_name DESC")
            machines_turn=cur.fetchall()
            
            #process identified
            #mass-material
            mater=''
            cur.execute('SELECT DISTINCT machine_name FROM machine_specs order by machine_name desc;')
            mat=cur.fetchall()
            for x in mat:
                const2='Y'
                if 'BENCHMAN-4000' in x[0] and material!='plastic' and material!='aluminium':
                    const3='N'
                    mater+='N'
                if const2=='Y':
                    mater+='Y'
                    
            
            #checking wt w.r.t. each machine
            cur.execute("SELECT * FROM materials where name='stainless steel';")
            density=cur.fetchall()[0][1]
            mass=float(part_dict['stock'][0])*float(part_dict['stock'][1])*float(part_dict['stock'][2])*float(density)*(10**(-9))
            cur.execute("SELECT machine_name, value FROM machine_specs where machine_param='wt' order by machine_name desc;")             
            wt_table=cur.fetchall()
            wt=''
            for x in range(0,len(wt_table)):
                if float(wt_table[x][1])>mass:
                    wt+='Y'
                else:
                    wt+='N'
            #verifying volume fit
            if process=='milling':
                cur.execute("SELECT machine_name, machine_param, value FROM machine_specs where machine_param like 'travel%' order by machine_name desc, machine_param asc;")
                vol_table=cur.fetchall()
                vol=''
                for x in range(len(vol_table)/3):
                    if float(vol_table[x][2])>float(part_dict['stock'][0]) and (vol_table[x+1][2])>float(part_dict['stock'][1]) and (vol_table[x+2][2])>float(part_dict['stock'][2]):
                        vol+='Y'
                    else:
                        vol+='N'
            elif process=='turning':
                cur.execute("SELECT machine_name,machine_param,value FROM machine_specs where machine_param='turn_dia' or machine_param='turn_len' order by machine_name desc,machine_param asc;")
                volt_table=cur.fetchall()
                volt=''
                
                for x in range(len(volt_table)/2):
                    if float(volt_table[x][2])>float(part_dict['stock'][0]) and (volt_table[x][2])>float(part_dict['stock'][1]) and (volt_table[x+1][2])>float(part_dict['stock'][2]):
                        volt+='Y'
                    else:
                        volt+='N'
                               
            #verifying max sspeed
            if process=='milling':
                cur.execute("SELECT machine_name,value FROM machine_specs where machine_param='rtsspeed' order by machine_name desc;")
                sspeed_table=cur.fetchall()
                sspeed=''
                for x in range(len(sspeed_table)):
                    if float(sspeed_table[x][1])>float(part_dict['spindle speed']):
                        sspeed+='Y'
                    else:
                        sspeed+='N'
            elif process=='turning':
                cur.execute("SELECT machine_name, value FROM machine_specs where machine_param='turn_sspeed_1' order by machine_name desc;")
                turnss_table=cur.fetchall()
                turnss=''
                for x in range(len(turnss_table)):
                    if float(turnss_table[x][1])>float(part_dict['spindle speed']):
                        turnss+='Y'
                    else:
                        turnss+='N'

            #verifying maximum rapid feed
            cur.execute("SELECT machine_name,value FROM machine_specs where machine_param='feed' order by machine_name desc;")
            feed_table=cur.fetchall()
            feed=''
            for x in range(len(feed_table)):
                if float(feed_table[x][1])*1000>float(part_dict['rapid feed']):
                    feed+='Y'
                else:
                    feed+='N'

            #verifying max tool diameter
            cur.execute("SELECT machine_name,value FROM machine_specs where machine_param='tool_dia' order by machine_name desc;")
            toold_table=cur.fetchall()
            toold=''
            maxtoold=0
            for x in tool_dict:
                if maxtoold<float(tool_dict[x][2]):
                    maxtoold=float(tool_dict[x][2])
            for x in range(len(toold_table)):
                if float(toold_table[x][1])>maxtoold:
                    toold+='Y'
                else:
                    toold+='N'

            #Minimum tolerance
            mintol=100
            cur.execute("SELECT machine_name,value FROM machine_specs where machine_param='tolerance' order by machine_name desc;")
            tol_table=cur.fetchall()
            tol=''
            for x in tool_dict:
                if mintol>float(tool_dict[x][0]):
                    mintol=float(tool_dict[x][0])
            for x in range(len(tol_table)):
                if float(tol_table[x][1])<mintol:
                    tol+='Y'
                else:
                    tol+='N'
            
            #Feature to tolerance
            cur.execute("SELECT * FROM proc_cap order by process;")
            ftol=cur.fetchall()
            ftol_cmt='Feature tolerance/s for process/es '
            comment1='Feature tolerance/s for process/es '
            
            for x in tool_dict:
                if 'bor' in x and float(tool_dict[x][0])<float(ftol[0][1]):
                    ftol_cmt=ftol_cmt +str(x)+', '
                    
                if 'drill' in x and float(tool_dict[x][0])<float(ftol[1][1]):
                    ftol_cmt=ftol_cmt+str(x)+', '
                    
                if 'mill' in x and float(tool_dict[x][0])<float(ftol[2][1]):
                    ftol_cmt=ftol_cmt+str(x)+', '

                if 'ream' in x and float(tool_dict[x][0])<float(ftol[3][1]):
                    ftol_cmt=ftol_cmt+str(x)+', '

                if 'turn' in x and float(tool_dict[x][0])<float(ftol[4][1]):
                    ftol_cmt=ftol_cmt+str(x)+', '
            
            if ftol_cmt==comment1:
                ftol_cmt=''
            else:
                ftol_cmt=ftol_cmt+'can not be machined using the assigned tools. Kindly reconsider.'
                feedback=ftol_cmt

            #finding the right machine
                     
            if process=='milling':
                macfind=['Y' for x in range(len(machines))] 
                for i in range(len(machines)):
                    if macfind[i]=='Y' and mater[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and wt[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and vol[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and sspeed[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and feed[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and toold[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and tol[i]=='N':
                        macfind[i]='N'

            
            if process=='turning':
                macfind=['N' for x in range(len(machines))]

                index_turn=[]
                
                for i,x in enumerate(machines):
                    for y in machines_turn:
                        if x==y:
                            index_turn.append(i)

                for i in index_turn:
                    macfind[i]='Y'

                for i,x in enumerate(machines):
                    if macfind[i]=='Y' and mater[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and wt[i]=='N':
                        macfind[i]='N'

                    if x in machines_turn:
                        if macfind[i]=='Y' and volt[machines_turn.index(x)]=='N':
                            macfind[i]='N'
                    if x in machines_turn:  
                        if macfind[i]=='Y' and turnss[machines_turn.index(x)]=='N':
                            macfind[i]='N'

                    if macfind[i]=='Y' and feed[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and toold[i]=='N':
                        macfind[i]='N'
                    if macfind[i]=='Y' and tol[i]=='N':
                        macfind[i]='N'

                
            machine_ideal=[]
            for i,x in enumerate(macfind):
                if x=='Y':
                    machine_ideal.append(machines[i][0])

            print time.clock()

            #machine availability
            machine_ideal_avail=[]
            const3=[]
            availtime=''
            machine_feedback=''
            for i,x in enumerate(machine_ideal):
                cur.execute("SELECT * FROM machine_avail where machine_name=%s;",(machine_ideal[i],))
                const3=cur.fetchall()[0]
                day=str(datetime.datetime.today().weekday())
                cur.execute("SELECT time_begin,time_end from machine_sched where machine_name=%s and day=%s;",(machine_ideal[i],day))
                sched=cur.fetchall()
                if 'busy' in const3[2] and 'BUSY' in const3[3]:
                    for y in sched:
                        if datetime.datetime.now().isoformat()[10:]<x[1]:
                            availtime=x+' is available at ' + datetime.datetime.now().isoformat()[0:10]+x[1]+':00. '
                            machine_ideal_avail.append(availtime)
                            break

                if 'idle' in const3[2] and 'BUSY' in const3[3]:
                    for y in sched:
                        if datetime.datetime.now().isoformat()[10:]<x[1]:
                            availtime=x+' is scheduled to be idle but is busy. Kindly check back in a while. The next available slot starts at '+datetime.datetime.now().isoformat()[0:10]+x[1]+':00. '
                            machine_ideal_avail.append(availtime)
                            break
                if 'idle' in const3[2] and ('READY' in const3[3] or 'OFF' in const3[3]):
                    availtime=x + ' is available now.'
                    machine_ideal_avail.append(availtime)
                                    

                #machine_ideal_avail.append(cur.fetchall()[0])                
                
            
            if len(machine_ideal)==0 or len(ftol_cmt)!=0:
                if len(ftol_cmt)!=0 and len(machine_ideal)==0:
                    feedback="Job specifications can not be achieved on any machine. Also, " + ftol_cmt
                elif len(machine_ideal)==0:
                    feedback="Job specifications can not be achieved on any machine."
                elif len(ftol_cmt)!=0:
                    feedback=ftol_cmt
                
                    
                machine_feedback='There are no machines that can machine this job.'

                
            elif len(ftol_cmt)==0:
                for x in machine_ideal:
                    machine_feedback+= x+', '
                machine_feedback+='can machine the part.'

            print time.clock()
            
            
                

            
            cur.execute("SELECT * FROM machine_rank order by rank ASC;")
            machine_ranking=cur.fetchall()
            ht_rank='0'

            if len(machine_ideal)>1 and process=='milling' and len(ftol_cmt)==0:
                for x in machine_ranking:
                    for y in machine_ideal:
                        if y in x:
                            if ht_rank>x[1]:
                                ht_rank=x[1]
            
                
            for x in machine_ranking:
                if ht_rank in x:
                    feedback=x[0]+' will provide better finish in better time.'
                    break

            if 'BENCHMAN-4000' in machine_ideal and len(machine_ideal)>1 and (material=='aluminium' or material=='plastic') and len(ftol_cmt)==0:
                        feedback+="BENCHMAN-4000 should be preferred if looking for prototyping the part with reasonable finish."


            #sending all feedbacks to the database from where DOME would read it.
            AVAILABILITY=''
            if len(ftol_cmt)==0 and machine_ideal>=1:
                for x in machine_ideal_avail:
                    AVAILABILITY+=x
            cur.execute("INSERT INTO dime_sks_log (timestamp, status, machine, availability,feedback) VALUES (%s,'AWS',%s,%s,%s);",(datetime.datetime.now().isoformat(),machine_feedback,AVAILABILITY,feedback))
            conn.commit()
            
 
