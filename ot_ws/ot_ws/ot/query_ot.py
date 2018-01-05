import requests
import os
import platform
url= os.getenv('OT_WS_URL')

url="http://otrcsl01.rcsl.lu/otws/v1.asmx"
import xml.etree.ElementTree as ET
if platform.system() == "Windows":
    Encoding = "cp437"
else:
    Encoding = "utf-8"

class query_ot():
    
    def __init__(self):
        self.body=""
        self.command =""
        self.headers = ""
        self.xml = ""
        self.xml_result = ""
        self.result = ""
        self.id= ""
        
    def get(self, id):
        self.id = id
        """Takes ID returns a formatted object"""
        self.body = r'<Get folderPath="" recursive="true"><ObjectIDs objectIDs="%s"/></Get>' % (id)
        self.command="GetObjectList"
        self.send()
    

    def add(self, model, fields):
        self.command = "AddObject"
        fieldxml = ""
        for field in fields:
            #print("looking for field xml string : of field %s, with value %s, class %s"%(field.name, field.value, field.fieldtype))
            #print (field.fieldXMLString())
            fieldxml = "%s%s" % (fieldxml, field.fieldXMLString())
        self.body = r'%s<Object folderPath="%s">' % (self.body, model.folder) + \
            r'%s' % fieldxml
        self.body = '%s</Object>' % self.body
        #print(self.body)
        self.send()
        tree = ET.fromstring(self.xml_result)
        root = tree \
            .find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')
        if root.attrib['success'] == "true":
            id = root.attrib['objectId']

            #print("couldn't add item in %s with fields %s" % (model.folder, fields))
            #print("request : %s" % self.xml)
            #print("response : %s" % self.xml_result)
        return id

    def getField(self, id, field):
        """Takes ID and a specific ot_field to query"""
        self.body = r'<Get folderPath="" recursive="true"><ObjectIDs objectIDs="%s"/><RequiredFields>%s</RequiredFields></Get>' % (id, field.name)
        self.command="GetObjectList"
        
    #def update(self, id, fields):

    def send(self):
        self.initQuery()
        data = self.xml.replace(r'\r\n', r'&#x000d;&#x000a;').encode("ascii", "xmlcharrefreplace")
        #print(self.headers)
        #print(data)
        #print(url)
        result = requests.post(url, data=data, headers=self.headers)
        ##print(self.body)
        
        #print(result.content)
        self.xml_result = result.content
        
                    
    def initQuery(self):
        """puts together hearders qnd command definition for the query"""
        self.headers = {'Content-Type': 'text/xml', 'charset': 'iso-8859-1',
                        'SOAPAction': '"http://www.omninet.de/OtWebSvc/v1/%s"'
                        % (self.command)}
        self.query = self.build()
        
        
        
        
    def build(self):
        """puts together hearders and command definition for the query"""
        self.xml = r'<?xml version="1.0" encoding="utf-8"?><soap:Envelope ' + \
            r'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
                   r'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' + \
                   r'xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
                   r'<%s xmlns="http://www.omninet.de/OtWebSvc/v1">' % (self.command) + \
                   r'%s</%s></soap:Body></soap:Envelope>' \
                   % (self.body, self.command)
                   
                   
    def GetEventByUCID(self, UCID):
        """hardcoded UCID query filter, temporary to avoid clashing with old api version"""
        self.body = ""
        
        self.command = "GetObjectList"
        self.body = r'%s<Get folderPath="01. ITSM - Service Operation\01. Event Management" recursive="true">' \
        % (self.body)

        
        self.body = r'%s<Filter>%s' % (self.body, 'EventUCID')

        filterVars =  r'<%s name="%s">%s</%s>' % ('StringVal', 'UCID', UCID, 'StringVal')
        self.body = r'%s%s</Filter></Get>' % (self.body, filterVars)
        self.send()