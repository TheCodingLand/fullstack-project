import requests
import os
import platform
import random
import logging

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')

from ot_ws.ot.ot_models import *
ENABLED = False
if os.getenv("OMNITRACKER_API_ENABLED") == "True":
    ENABLED = True
if os.getenv("OMNITRACKER_API_URL"):
    url = os.getenv("OMNITRACKER_API_URL")
else:
    url = "http://otrcsl01.rcsl.lu/otws/v1.asmx"

import xml.etree.ElementTree as ET
if platform.system() == "Windows":
    Encoding = "cp437"
else:
    Encoding = "utf-8"


class query_ot():

    def __init__(self):
        self.body = ""
        self.command = ""
        self.headers = ""
        self.xml = ""
        self.xml_result = ""
        self.result = ""
        self.id = ""

    def get(self, id):
        self.id = id
        """Takes ID returns a formatted object"""
        self.body = r'<Get folderPath="" recursive="true"><ObjectIDs objectIDs="%s"/></Get>' % (
            id)
        self.command = "GetObjectList"
        if ENABLED:
            self.send()
        else:
            self.xml_result = self.dummydata()

    def add(self, model, fields):
        self.command = "AddObject"
        fieldxml = ""

        for field in fields:
            #print("looking for field xml string : of field %s, with value %s, class %s"%(field.name, field.value, field.fieldtype))
            #print (field.fieldXMLString())

            fieldxml = "%s%s" % (fieldxml, field.fieldXMLString())
        logging.warning(fieldxml)
        self.body = r'%s<Object folderPath="%s">' % (self.body, model.folder) + \
            r'%s' % fieldxml
        self.body = '%s</Object>' % self.body
        # print(self.body)
        self.send()
        tree = ET.fromstring(self.xml_result)
        root = tree \
            .find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')

        if root.attrib['success'] == "true":
            id = root.attrib['objectId']
        else:
            logging.ERROR(self)
            logging.ERROR(self.xml_result)
            #print("couldn't add item in %s with fields %s" % (model.folder, fields))
            #print("request : %s" % self.xml)
            #print("response : %s" % self.xml_result)

        return id

    def getField(self, id, field):
        """Takes ID and a specific ot_field to query"""
        self.body = r'<Get folderPath="" recursive="true"><ObjectIDs objectIDs="%s"/><RequiredFields>%s</RequiredFields></Get>' % (
            id, field.name)
        self.command = "GetObjectList"

    # def update(self, id, fields):

    def send(self):
        self.initQuery()
        data = self.xml.replace(r'\r\n', r'&#x000d;&#x000a;').encode(
            "ascii", "xmlcharrefreplace")
        # print(self.headers)
        # print(data)
        # print(url)
        result = requests.post(url, data=data, headers=self.headers)
        # print(self.body)

        # print(result.content)
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

        filterVars = r'<%s name="%s">%s</%s>' % (
            'StringVal', 'UCID', UCID, 'StringVal')
        self.body = r'%s%s</Filter></Get>' % (self.body, filterVars)
        self.send()

    def getObjectList(self, objectClassName, filter, variables):
        """requests info from the api based on defined a filter and an arraw of variables [[variable1,Value1],[variable2,Value2]]"""

        self.body = ""
        if objectClassName in globals():
            id = "1234asdf"
            constructor = globals()[objectClassName]
            item = constructor()
        else:
            raise "error, impossible to create an instance of %s, check your input / class definitions" % (
                objectClassName)

        self.command = "GetObjectList"
        self.body = r'%s<Get folderPath="%s" recursive="true">' \
            % (self.body, item.folder)
        if filter != "":

            self.body = '%s<Filter>%s' % (self.body, filter)
            filterVars = ''
            for variable in variables:
                filterVars = '%s<%s name="%s">%s</%s>' % (
                    filterVars, 'StringVal', variable.get('name'), variable.get('value'), 'StringVal')
            self.body = '%s%s</Filter>' % (self.body, filterVars)
        self.body = r'%s</Get>' % (self.body)
        self.send()

    def GetUserByExt(self, UCID):
        """hardcoded UCID query filter, temporary to avoid clashing with old api version"""
        self.body = ""

        self.command = "GetObjectList"
        self.body = r'%s<Get folderPath="01. ITSM - Service Operation\01. Event Management" recursive="true">' \
            % (self.body)

        self.body = r'%s<Filter>%s' % (self.body, 'EventUCID')

        filterVars = r'<%s name="%s">%s</%s>' % (
            'StringVal', 'UCID', UCID, 'StringVal')
        self.body = r'%s%s</Filter></Get>' % (self.body, filterVars)
        self.send()

    def dummydata(self):
        id = random.randint(1000000, 5000000)

        data = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope
                xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <soap:Body>
                    <GetObjectListResponse
                        xmlns="http://www.omninet.de/OtWebSvc/v1">
                        <GetObjectListResult success="true" errorMsg="" totalNumberResults="1">
                            <Object id="%s">
                                <ReferenceToUserVal name="Applicant" type="userdisplayname" Value="Superuser" />
                                <NullVal name="AssociatedCategory" />
                                <NullVal name="AssociatedClosureCategory" />
                                <ReferenceListVal name="RelatedEmails" objectIds="" />
                                <ReferenceListVal name="AssociatedExternalPersons" objectIds="" />
                                <ReferenceListVal name="AssociatedBmsJobExecs" objectIds="" />
                                <NullVal name="AssociatedCI" />
                                <AttachmentsVal name="Attachments" />
                                <NullVal name="Call Status" />
                                <NullVal name="Call Finished Date" />
                                <NullVal name="CINumber" />
                                <StringVal name="Class">(not specified)</StringVal>
                                <TimeStampedMemoVal name="Answers" />
                                <LongIntVal name="CountEventMails">0</LongIntVal>
                                <DateTimeVal name="CreationDate">2017-12-19T15:56:00</DateTimeVal>
                                <NullVal name="Description" />
                                <NullVal name="EventID" />
                                <NullVal name="Eventaction" />
                                <StringVal name="Eventsystem">n.n.</StringVal>
                                <ReferenceVal name="Eventtype" objectId="560566" />
                                <ReferenceListVal name="ExternalTickets" objectIds="" />
                                <StringVal name="Impact">(not specified)</StringVal>
                                <NullVal name="InitialAssociatedCategory" />
                                <DateTimeVal name="LastChange">2017-12-19T15:56:01</DateTimeVal>
                                <BoolVal name="ManualSLAChange">false</BoolVal>
                                <LongIntVal name="Number">193696</LongIntVal>
                                <LongIntVal name="CountCorrelatedEvents">0</LongIntVal>
                                <NullVal name="Phone Number" />
                                <NullVal name="PickUpDateTime" />
                                <StringVal name="PreferredContactType">NotSpecified</StringVal>
                                <StringVal name="Priority">(not specified)</StringVal>
                                <NullVal name="UCOnSiteBreachReason" />
                                <NullVal name="UCResolutionBreachReason" />
                                <NullVal name="UCResponseBreachReason" />
                                <NullVal name="RelatedChange" />
                                <ReferenceListVal name="CorrelatedEvents" objectIds="" />
                                <NullVal name="RelatedIncident" />
                                <NullVal name="RelatedProblem" />
                                <BoolVal name="Reopened">false</BoolVal>
                                <NullVal name="ReportingCompany" />
                                <ReferenceToUserVal name="Responsible" type="groupname" Value="Event-Staff" />
                                <StringVal name="Source">Call</StringVal>
                                <StringVal name="State">new</StringVal>
                                <StringVal name="Subclass">(not specified)</StringVal>
                                <NullVal name="TIGGroup" />
                                <NullVal name="Title" />
                                <NullVal name="TransferHistory" />
                                <StringVal name="UCID">1231424142313</StringVal>
                                <StringVal name="Urgency">(not specified)</StringVal>
                            </Object>
                        </GetObjectListResult>
                    </GetObjectListResponse>
                </soap:Body>
            </soap:Envelope>""" % (id)
        return data.encode()
