import dateutil.parser
import json
import datetime
import arrow
from dateutil.parser import parse


def date_handler(obj): return (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)


class ot_field(object):
    def __init__(self, name):
        self.fieldtype = ""
        self.name = name
        self.value = ""

    def fieldXMLString(self):
        fieldquery = r'<%s name="%s">%s</%s>' \
            % (self.fieldtype, self.name, self.value, self.fieldtype)
        return fieldquery

    def getValueFromXML(self, xml):
        return xml.text

    def __unicode__(self):
        return self.value


class NullVal(ot_field):
    def __init(self, name):
        super(NullVal, self).__init__(name)
        self.fieldtype = "NullVal"

    def getValueFromXML(self, xml):
        self.value = ""
        return self.value

    def fieldXMLString(self):
        return false


class ObjectId(ot_field):
    def __init__(self, name):
        super(ObjectId, self).__init__(name)
        self.fieldtype = "ID"


class LongIntVal(ot_field):
    def __init__(self, name):
        super(LongIntVal, self).__init__(name)
        self.fieldtype = "LongIntVal"


class ShortIntVal(ot_field):
    def __init__(self, name):
        super(ShortIntVal, self).__init__(name)
        self.fieldtype = "LongIntVal"


class BoolVal(ot_field):
    def __init__(self, name):
        super(BoolVal, self).__init__(name)
        self.fieldtype = "BoolVal"


class StringVal(ot_field):
    def __init__(self, name):
        super(StringVal, self).__init__(name)
        self.fieldtype = "StringVal"


class DateTimeVal(ot_field):
    def __init__(self, name):
        super(DateTimeVal, self).__init__(name)
        self.fieldtype = "DateTimeVal"

    def getValueFromXML(self, xml):
        self.value = dateutil.parser.parse(xml.text)
        self.value = json.dumps(self.value, default=date_handler)[1:-1]
        return self.value

    def fieldXMLString(self):
        self.value = arrow.get(self.value).datetime
        self.value = self.value.astimezone().replace(tzinfo=None)
        fieldquery = r'<%s name="%s">%s</%s>' \
            % (self.fieldtype, self.name, self.value.isoformat()[:-7], self.fieldtype)
        return fieldquery


class Text(ot_field):
    def __init__(self, name):
        super(Text, self).__init__(name)
        self.fieldtype = "Text"


class ReferenceVal(ot_field):
    def __init__(self, name):
        super(ReferenceVal, self).__init__(name)
        self.fieldtype = "ReferenceVal"

    def fieldXMLString(self):
        fieldquery = r'<ReferenceVal name="%s" objectId="%s"/>' \
            % (self.name, self.value)
        return fieldquery

    def getValueFromXML(self, xml):
        try:
            self.value = xml.attrib['objectId']
        except:
            self.value = None
        return self.value


class ReferenceToUserVal(ot_field):
    def __init__(self, name):
        super(ReferenceToUserVal, self).__init__(name)
        self.fieldtype = "ReferenceToUserVal"
        self.reference = "userdisplayname"

    def fieldXMLString(self):
        fieldquery = r'<ReferenceToUserVal name = "%s" type = "%s" Value = "%s" />' \
            % (self.name, self.reference, self.value)
        return fieldquery

    def getValueFromXML(self, xml):
        return xml.attrib['Value']


class ReferenceListVal(ot_field):
    def __init__(self, name):
        super(ReferenceListVal, self).__init__(name)

    def getValueFromXml(self, xml):
        try:
            value = xml.attrib['objectIds']
            self.value = value.split(" ")
        except:
            self.value = None

        return self.value

    def fieldXMLString(self):
        if len(self.value) > 0:
            ids = ""
            for value in self.value:
                ids = "%s %s" % (ids, value)
                fieldquery = r'<ReferenceListVal name = "%s" objectIds="%s" />' \
                    % (self.name, ids[1:])
        return fieldquery

# NOT HANDLED YET


class TimeStampedMemoVal(ot_field):
    def __init(TimeStampedMemoVal, name):
        super(NullVal, self).__init__(name)
        self.fieldtype = "TimeStampedMemoVal"

    def getValueFromXML(self, xml):
        self.value = ""
        return self.value

    def fieldXMLString(self):
        return false


class AttachmentsVal(ot_field):
    def __init(self, name):
        super(AttachmentsVal, self).__init__(name)
        self.fieldtype = "AttachmentsVal"

    def getValueFromXML(self, xml):
        self.value = ""
        return self.value

    def fieldXMLString(self):
        return false
