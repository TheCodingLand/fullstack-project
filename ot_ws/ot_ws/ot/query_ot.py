import requests
import os
import platform
import random
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
from ot_ws.ot.ot_models import *
ENABLED = False
if os.getenv("OMNITRACKER_API_ENABLED") == "TRUE":
    ENABLED = True
if os.getenv("OMNITRACKER_API_URL"):
    url = os.getenv("OMNITRACKER_API_URL")

import xml.etree.ElementTree as ET
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

    def getWithFields(self, id, requiredFields):
        self.id = id
        """Takes ID returns an object with specific fields formatted object"""
        self.body = r'<Get folderPath="" recursive="false"><ObjectIDs objectIDs="%s"/>' % (
            id)
        if requiredFields != []:
            required = ""
            for f in requiredFields:
                required = r'%s<RequiredField>%s</RequiredField>' % (required,f)

        self.body = "%s%s</Get>" % (self.body, required)

        self.command = "GetObjectList"
        self.send()
        #logging.error(self.xml)
        #logging.error(self.xml_result)

    def get(self, id):
        self.id = id
        """Takes ID returns a formatted object"""
        self.body = r'<Get folderPath="" recursive="false"><ObjectIDs objectIDs="%s"/></Get>' % (
            id)

        self.command = "GetObjectList"
        self.send()

    def remove(self, id):
        self.id = id
        """Takes ID, deletes object"""
        self.body = r'<RemoveObject><ObjectID>%s</ObjectID><IgnoreReferences>true</IgnoreReferences></RemoveObject >' % (
            id)

        self.command = "GetObjectList"
        self.send()

    def modifyObjet(self, id, fields):
        self.id = id
        self.command = "ModifyObject"
        fieldxml = ""
        # logging.error(fields)
        for field in fields:
            fieldxml = "%s%s" % (fieldxml, field.fieldXMLString())

        self.body = r'<Object objectId="%s">' % (
            self.id) + r'%s' % fieldxml
        self.body = '%s</Object>' % self.body
        # logging.error(self.body)
        self.send()
        if ENABLED == True:

            tree = ET.fromstring(self.xml_result)
            root = tree \
                .find('*//{http://www.omninet.de/OtWebSvc/v1}ModifyObjectResult')

            if root.attrib['success'] == "true":
                return True
            else:
                return False

        else:
            log.error("API disabled %s" % self.xml)
            return False

    def add(self, model, fields):
        #log.error("sending object event")
        self.command = "AddObject"
        fieldxml = ""
        # logging.info(fields)
        for field in fields:
            fieldxml = "%s%s" % (fieldxml, field.fieldXMLString())
        # logging.info(fieldxml)
        self.body = r'%s<Object folderPath="%s">' % (self.body, model.folder) + \
            r'%s' % fieldxml
        self.body = '%s</Object>' % self.body

        self.send()
        if ENABLED == True:

            tree = ET.fromstring(self.xml_result)
            root = tree \
                .find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')

            if root.attrib['success'] == "true":
                id = root.attrib['objectId']
            else:
                log.error("could not complete request %s" % self.xml)
                log.error("server response : %s" % logging.error(
                    "could not complete request %s" % self.xml_result))
                id = 0
            return id
        else:
            log.error("API disabled %s" % self.xml)
            id = 0
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

        if ENABLED == True:
            result = requests.post(url, data=data, headers=self.headers)
        # logging.error(result.text)
            self.xml_result = result.content

        # logging.info(self.xml)
        # logging.info(self.xml_result)

    def initQuery(self):
        """puts together hearders qnd command definition for the query"""
        self.headers = {'Content-Type': 'text/xml', 'charset': 'utf-8',
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

    def getObjectList(self, objectClassName, filter, variables, requiredFields):
        """requests info from the api based on defined a filter and an arraw of variables [[variable1,Value1],[variable2,Value2]]"""

        self.body = ""
        if objectClassName in globals():
            constructor = globals()[objectClassName]
            item = constructor()
        else:
            logging.error("error, impossible to create an instance of %s, check your input / class definitions" % (
                objectClassName))

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

        if requiredFields != []:
            required = ""
            for f in requiredFields:
                required = '<RequiredField>%s</RequiredField>' % (f)
            self.body = '%s%s' % (self.body, required)

        self.body = r'%s</Get>' % (self.body)

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
