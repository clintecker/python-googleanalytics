import datetime
import time
from xml.etree import ElementTree

data_converters = {
   'integer': int,
}

class DataSet(list):
    """docstring for DataSet"""

    def __init__(self, raw_xml):
        list.__init__(self)
        self.raw_xml = raw_xml
        xml_tree = ElementTree.fromstring(self.raw_xml)
        self.id = xml_tree.find('{http://www.w3.org/2005/Atom}id').text
        self.title = xml_tree.find('{http://www.w3.org/2005/Atom}title').text
        self.totalResults = int(xml_tree.find('{http://a9.com/-/spec/opensearchrss/1.0/}totalResults').text)
        self.startIndex = int(xml_tree.find('{http://a9.com/-/spec/opensearchrss/1.0/}startIndex').text)
        self.itemsPerPage = int(xml_tree.find('{http://a9.com/-/spec/opensearchrss/1.0/}itemsPerPage').text)

        endDate = xml_tree.find('{http://schemas.google.com/analytics/2009}endDate').text
        self.endDate = datetime.date.fromtimestamp(time.mktime(time.strptime(endDate, '%Y-%m-%d')))
        startDate = xml_tree.find('{http://schemas.google.com/analytics/2009}startDate').text
        self.startDate = datetime.date.fromtimestamp(time.mktime(time.strptime(startDate, '%Y-%m-%d')))

        aggregates = xml_tree.find('{http://schemas.google.com/analytics/2009}aggregates')
        aggregate_metrics = aggregates.findall('{http://schemas.google.com/analytics/2009}metric')
        self.aggregates = []
        for m in aggregate_metrics:
            metric = Metric(**m.attrib)
            setattr(self, metric.name, metric)
            self.aggregates.append(metric)

        dataSource = xml_tree.find('{http://schemas.google.com/analytics/2009}dataSource')
        self.tableId = dataSource.find('{http://schemas.google.com/analytics/2009}tableId').text
        self.tableName = dataSource.find('{http://schemas.google.com/analytics/2009}tableName').text
        properties = dataSource.findall('{http://schemas.google.com/analytics/2009}property')
        for property in properties:
            setattr(self, property.attrib['name'].replace('ga:', ''), property.attrib['value'])

        entries = xml_tree.getiterator('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            dp = DataPoint(entry)
            self.append(dp)

    @property
    def list(self):
        return [[[d.value for d in dp.dimensions], [m.value for m in dp.metrics]] for dp in self]

    @property
    def tuple(self):
        return tuple(map(tuple, self.list))


class DataPoint(object):
    """DataPoint takes an `entry` from the xml response and creates `Dimension` and `Metric`
    objects in the order they are returned. It has the the dimensions and metrics available 
    directly as object attributes as well as stored in the `metrics` and `dimensions` array attributes.
    """
    def __init__(self, entry):
        self.title = entry.find('{http://www.w3.org/2005/Atom}title').text
        metrics = entry.findall('{http://schemas.google.com/analytics/2009}metric')
        self.metrics = []
        for m in metrics:
            metric = Metric(**m.attrib)
            setattr(self, metric.name, metric.value)
            self.metrics.append(metric)

        dimensions = entry.findall('{http://schemas.google.com/analytics/2009}dimension')
        self.dimensions = []
        for d in dimensions:
            dimension = Dimension(**d.attrib)
            setattr(self, dimension.name, dimension.value)
            self.dimensions.append(dimension)


class Dimension(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, unicode(v.replace('ga:', '')))


class Metric(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, unicode(v.replace('ga:', '')))
        if self.type in data_converters:
            self.value = data_converters[self.type](self.value)

