from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import xml.etree.cElementTree as ET
import serial, re, time,string, psycopg2, psycopg2.extras, sys, datetime

PORT_NUMBER = 5000

#This class will handle any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
                        self.path="/probe.xml"
                        
                elif self.path=="/probe":
                        self.path="/probe.xml"

                elif self.path=="/current":
                        self.path="/current.xml"

                elif self.path=="/asset" or self.path=="/assets":
                        self.path="/asset.xml"

                elif self.path=="/sample":
                        execfile("sample_1.py")
                        self.path="/sample.xml"

                elif "count" in self.path and "from" in self.path:
                        a=self.path
                        b=a.split('?')
                        if len(b)==2:
                                if b[0]=="/sample" and bool(re.match('from=[0-9]+&count=[0-9]+',b[1])):
                                        b[1]=b[1].split('&')
                                        FROM_COUNT=int(b[1][0].split('=')[1])
                                        DATA_COUNT=int(b[1][1].split('=')[1])

                                        currente = ET.parse('current.xml')
                                        rootc = currente.getroot()
                                        FROM=int(rootc[0].attrib['firstSequence'])
                                        TO=int(rootc[0].attrib['lastSequence'])
                                        if (DATA_COUNT+FROM)<=TO and FROM_COUNT>=FROM and FROM_COUNT<=TO:
                                                execfile("sample_3.py")
                                                self.path="/sample2.xml"
                                        else:
                                                errore = ET.parse('error.xml')
                                                roote = errore.getroot()
                                                                                       
                                                roote.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
                                                roote[0].attrib['instanceId']=rootc[0].attrib['instanceId']
                                                roote[0].attrib['creationTime']=rootc[0].attrib['creationTime']
                                                roote[0].attrib['bufferSize']=rootc[0].attrib['bufferSize']
                                                roote[1][0].attrib['errorCode']="OUT_OF_RANGE"
                                                roote[1][0].text="'count' must be less than or equal to 1000. 'from' must be greater than or equal to "+str(FROM)+". 'from+count' must be less than or equal to "+str(TO)+"."
                                                error=ET.ElementTree(roote)
                                                error.write('error.xml',encoding='utf-8',xml_declaration=True)
                                                self.path="/error.xml"
                                        
                elif "count" in self.path:
                        a=self.path
                        b=a.split('?')
                        if len(b)==2:
                                if b[0]=="/sample" and bool(re.match('count=[0-9]+',b[1])):
                                        DATA_COUNT=int(b[1].split('=')[1])
                                        if DATA_COUNT<=1000:
                                                execfile("sample_2.py")
                                                self.path="/sample1.xml"
                                        else:
                                                errore = ET.parse('error.xml')
                                                roote = errore.getroot()

                                                currente = ET.parse('current.xml')
                                                rootc = currente.getroot()
                                                
                                                roote.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
                                                roote[0].attrib['instanceId']=rootc[0].attrib['instanceId']
                                                roote[0].attrib['creationTime']=rootc[0].attrib['creationTime']
                                                roote[0].attrib['bufferSize']=rootc[0].attrib['bufferSize']
                                                roote[1][0].attrib['errorCode']="OUT_OF_RANGE"
                                                roote[1][0].text="'count' must be less than or equal to 1000."
                                                error=ET.ElementTree(roote)
                                                error.write('error.xml',encoding='utf-8',xml_declaration=True)
                                                self.path="/error.xml"

                else:
                        errore = ET.parse('error.xml')
                        roote = errore.getroot()

                        currente = ET.parse('current.xml')
                        rootc = currente.getroot()
                                                
                        roote.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
                        roote[0].attrib['instanceID']=rootc[0].attrib['instanceID']
                        roote[0].attrib['creationTime']=rootc[0].attrib['creationTime']
                        roote[0].attrib['bufferSize']=rootc[0].attrib['bufferSize']
                        roote[1][0].attrib['errorCode']="UNSUPPORTED"
                        roote[1][0].text="The following path is invalid: "+str(self.path)+" ."
                        error=ET.ElementTree(roote)
                        error.write('error.xml',encoding='utf-8',xml_declaration=True)
                        self.path="/error.xml"
                                
                        
                try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
                                
			if self.path.endswith(".xml"):
				mimetype='xml'
				sendReply = True
			
			if sendReply == True:
				#Open the static file requested and send it
                                f = open(curdir + sep + self.path) 
                                self.send_response(200)
                                self.send_header('Content-type',mimetype)
                                self.end_headers()
                                self.wfile.write(f.read())
                                f.close()
			return


		except IOError:
                        self.send_error(404,'File Not Found')
                        

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
