from googleanalytics.exception import GoogleAnalyticsClientError
from googleanalytics.data import DataPoint, DataSet

import urllib

filter_operators = ['==', '!=', '>', '<', '>=', '<=', '=~', '!~', '=@', '!@']
data_converters = {
   'integer': int,
}

class Account:
    def __init__(self, connection=None, title=None, id=None,
        account_id=None, account_name=None, profile_id=None,
        currency=None, time_zone=None, web_property_id=None,
        table_id=None, updated=None):
        self.connection = connection
        self.title = title
        self.id = id
        self.account_id = account_id
        self.account_name = account_name
        self.profile_id = profile_id
        self.currency = currency
        self.time_zone = time_zone
        self.updated = updated
        self.web_property_id = web_property_id

    def __repr__(self):
        return '<Account: %s>' % self.title

    def get_data(self, start_date, end_date, metrics, dimensions=[], sort=[], filters=[], start_index=0, max_results=0):
        """
        Pulls data in from an account and returns a processed data structure for
        easy post processing. This method requires the following inputs:
        
        ** Required Arguments **
        
        ``start_date``
          A ``datetime`` object for the lower bound of your query
          
        ``end_date``
          A ``datetime`` object for the upper bound of your query
    
        ``metrics``
          A list of metrics, for example: ['pageviews', 'uniquePageviews']
        
          See: http://code.google.com/apis/analytics/docs/gdata/gdataReferenceDimensionsMetrics.html
          See: http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#dimensionsAndMetrics
    
        ** Optional Arguments **
        
        ``dimensions``
          A list of dimensions, for example: ['country','browser']
        
          See: http://code.google.com/apis/analytics/docs/gdata/gdataReferenceDimensionsMetrics.html
          See: http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#dimensionsAndMetrics
    
        ``sort``
          A list of dimensions or metrics to sort the output by, should probably
          be one of the items you specified in ``dimensions`` or ``metrics``.
          For example: ['browser', 'pageviews']
        
          See: http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#sorting
          
        ``filters``
          A list of filters.  A filter expression has three parts:
          
            name - The name of the dimension or metric to filter on. 
                    For example: ga:pageviews will filter on the pageviews metric.
            operator - Defines the type of filter match to use. Operators are 
                        specific to either dimensions or metrics.
            expression - States the values included or excluded from the results.
                          Expressions use regular expression syntax.
    
          Learn more about valid operators and expressions here:
          http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#filtering
          
          The ``filters`` input accepts this data as a list of lists like so. Please
          note that order matters, especially when using boolean operators (see
          below). 
          
            [
              ['browser', '=~', 'Firefox', 'AND'], # Regular expression match on 'Firefox'
              ['browser', '=~', 'Internet (Explorer|Exploder)', 'OR'],
              ['city', '=@', 'York', 'OR'], # All cities with York as a substring
              ['state', '!=', 'California', 'AND'], # Everything but California
              ['timeOnPage', '<', '10'], # Reject results where timeonpage < 10sec
            ]
            
          Filters can be combined with AND boolean logic as well as with OR 
          boolean logic. When using both operators, the OR operator has higher 
          precendence. When you are using more than one filter, please specify
          a fourth item in your list 'AND' or 'OR' to explicitly spell out the
          filters' relationships:
          
          For example, this filter selects data from the United States from the
          browser Firefox.
          
          [
            ['country', '==', 'United States', 'OR'],
            ['browser', '=@', 'FireFox'],
          ]
          
          This filter selects data from either the United States or Canada.
          
          [
            ['country', '==', 'United States', 'AND'],
            ['country', '==', 'Canada'],
          ]
          
          The first filter limits results to cities starting with 'L' and ending 
          with 'S'. The second limits results to browsers starting with 'Fire' 
          and the cities starting with 'L':
          
          [
            ['city', '=~', '^L.*S$']
          ]
          
          [
            ['city', '=~', '^L', 'AND'],
            ['browser', '=~', '^Fire']
          ]
    
        ``start_index``
          The first row to return, starts at 1. This is useful for paging in combination with
          max_results, and also to get results past row 1000 (Google Data does not return
          more than 1000 results at once)
          
        ``max_results``
          Number of results to return.
          
        """
        path = '/analytics/feeds/data'

        if start_date > end_date:
            raise GoogleAnalyticsClientError('Date orders are reversed')

        data = {
            'ids': self.table_id,
            'start-date': start_date.strftime('%Y-%m-%d'),
            'end-date': end_date.strftime('%Y-%m-%d'),
        }

        if start_index > 0:
            data['start-index'] = str(start_index)

        if max_results > 0:
            data['max-results'] = str(max_results)

        if dimensions:
            data['dimensions'] = ",".join(['ga:' + d for d in dimensions])
        data['metrics'] = ",".join(['ga:' + m for m in metrics])
        if sort:
            _sort = []
            for s in sort:
                pre = 'ga:'
                if s[0] == '-':
                    pre = '-ga:'
                    s = s[1:]
                _sort.append(pre + s)
            data['sort'] = ",".join(_sort)
        if filters:
            filter_string = self.process_filters(filters)
            data['filters'] = filter_string

        processed_data = DataSet()
        data = urllib.urlencode(data)

        response = self.connection.make_request('GET', path=path, data=data)
        raw_xml = response.read()
        xml_tree = self.connection.parse_response(raw_xml)
        data_rows = xml_tree.getiterator('{http://www.w3.org/2005/Atom}entry')
        for row in data_rows:
            values = {}
            ms = row.findall('{http://schemas.google.com/analytics/2009}metric')
            ds = row.findall('{http://schemas.google.com/analytics/2009}dimension')
            title = row.find('{http://www.w3.org/2005/Atom}title').text
            if len(ms) == 0:
                continue
            # detect datatype and convert if possible
            for m in ms:
                if m.attrib['type'] in data_converters.keys():
                    m.attrib['value'] = data_converters[m.attrib['type']](m.attrib['value'])
            dp = DataPoint(
                account=self,
                connection=self.connection,
                title=title,
                metrics=[m.attrib['value'] for m in ms],
                dimensions=[d.attrib['value'] for d in ds]
            )
            processed_data.append(dp)
        return processed_data

    def process_filters(self, filters):
        processed_filters = []
        multiple_filters = False
        if len(filters) > 1:
            multiple_filters = True
        for filt in filters:
            if len(filt) < 3:
                continue
            if len(filt) == 3:
                name, operator, expression = filt
                if multiple_filters:
                    comb = 'AND'
                else:
                    comb = ''
            elif len(filt) == 4:
                name, operator, expression, comb = filt
                if comb != 'AND' and comb != 'OR':
                    comb == 'AND'

            # Reject any filters with invalid operators
            if operator not in filter_operators:
                continue

            name = 'ga:' + name

            # Mapping to GA's boolean operators
            if comb == 'AND': comb = ';'
            if comb == 'OR': comb = ','

            # These three characters are special and must be escaped
            if '\\' in expression:
                expression = expression.replace('\\', '\\\\')
            if ',' in expression:
                expression = expression.replace(',', '\,')
            if ';' in expression:
                expression = expression.replace(';', '\;')

            processed_filters.append("".join([name, operator, expression, comb]))
        filter_string = "".join(processed_filters)

        # Strip any trailing boolean symbols
        if filter_string:
            if filter_string[-1] == ';' or filter_string[-1] == ',':
                filter_string = filter_string[:-1]
        return filter_string
