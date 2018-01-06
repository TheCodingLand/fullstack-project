import xml.etree.ElementTree as ET
from ot_ws.ot.ot_field import *
import re

testxml = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <GetObjectListResponse
            xmlns="http://www.omninet.de/OtWebSvc/v1">
            <GetObjectListResult success="true" errorMsg="" totalNumberResults="1">
                <Object id="1279330">
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
</soap:Envelope>"""


class Result(object):
    def __init__(self):
        self.id = 0
        self.res = {}
        self.metadata = {}


class serialize(object):

    def __init__(self, xml):

        self.res = {}
        self.metadata = {}
        self.id = 0
        self.results = []
        self.parse(xml)

    def getFields(self, xml):
        result = Result()
        #self.res.update({ 'id' : id})
        result.id = xml.attrib['id']
        print(result.id)

        for field in xml:
            k = globals()[field.tag]
            name = field.attrib['name']
            f = k(name)

            result.metadata.update({'%s' % name: field.tag})
            result.res.update({'%s' % name: f.getValueFromXML(field)})
        self.results.append(result)
        print(self.results)

    def parse(self, xml):
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        tree = ET.fromstring(xml)
        print(xml)
        root = tree \
            .find('*//GetObjectListResult')
        if root.attrib['success'] == "true":
            nbresults = 1
            try:
                nbresults = int(root.attrib['totalNumberResults'])

            except:
                nbresults = 1
            if nbresults == 1:
                result = True
                self.getFields(root[0])

            elif nbresults > 1:
                for item in root:
                    self.getFields(item)

            else:
                self.res = False

        print("RESULTS %s" % nbresults)


def test():
    data = testxml
    builder = serialize(testxml)
    return(builder.res)
