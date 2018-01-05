import xmltodict

xml="""<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsl="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body><GetObjectList xmlns="http://www.omninet.de/OtWebSvc/v1"><Get folderPath="01. ITSM - Service Operation\\01. Event Management" recursive="true"><Filter>EventUCID<StringVal name="UCID">1231244123</StringVal></Filter></Get></GetObjectList></soap:Body></soap:Envelope>"""

def data():
    return xmltodict.parse(xml)


