import urllib

class Account:
    def __init__(self, connection=None, title=None, link=None,
      account_id=None, account_name=None, profile_id=None,
      web_property_id=None, table_id=None, validated=False):
        self.connection = connection
        self.title = title
        self.link = link
        self.account_id = account_id
        self.account_name = account_name
        self.profile_id = profile_id
        self.web_property_id = web_property_id
        if table_id:
          self.table_id = table_id
        else:
          self.table_id = 'ga:' + self.profile_id
        self.validated = validated

    def __repr__(self):
      if self.title:
        return '<Account: %s>' % self.title
      elif self.table_id:
        return '<Account: %s>' % self.table_id
        
    def get_data(self, start_date, end_date, dimensions=None, metrics=None, sort=None, filters=None):
      """
      Pulls data in from an account and returns a processed data structure for
      easy post processing. This method requires the following inputs:
      
      ** Required Arguments **
      
      ``start_date``
        A ``datetime`` object for the lower bound of your query
        
      ``end_date``
        A ``datetime`` object for the upper bound of your query
      
      ** Optional Arguments **
      
      ``dimensions``
        A list of dimensions, for example: ['country','browser']
      
        See: http://code.google.com/apis/analytics/docs/gdata/gdataReferenceDimensionsMetrics.html
        See: http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#dimensionsAndMetrics

      ``metrics``
        A list of metrics, for example: ['pageviews', 'uniquePageviews']
      
        See: http://code.google.com/apis/analytics/docs/gdata/gdataReferenceDimensionsMetrics.html
        See: http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#dimensionsAndMetrics
        
      ``sort``
        A list of dimensions or metrics to sort the output by, should probably
        be one of the items you specified in ``dimensions`` or ``metrics``.
        For example: ['browser', 'pageviews']
      
        See: http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#sorting
        
      ``filters``
        A list of filters.  A filter expression has three parts:
        
          name —  The name of the dimension or metric to filter on. 
                  For example: ga:pageviews will filter on the pageviews metric.
          operator —  Defines the type of filter match to use. Operators are 
                      specific to either dimensions or metrics.
          expression —  States the values included or excluded from the results.
                        Expressions use regular expression syntax.

        Learn more about valid operators and expressions here:
        http://code.google.com/apis/analytics/docs/gdata/gdataReference.html#filtering
        
        The ``filters`` input accepts this data as a list of lists like so:
        
          [
            ['browser', '=~', 'Firefox'], # Regular expression match on 'Firefox'
            ['browser', '=~', 'Internet (Explorer|Exploder)'],
            ['city', '=@', 'York'], # All cities with York as a substring
            ['state', '!=', 'California'], # Everything but California
            ['timeOnPage', '<', '10'], # Reject results where timeonpage < 10sec
          ]
      
      """
      path = '/analytics/feeds/data'
      
      data = {
        'ids': self.table_id,
        'dimensions': ",".join(['ga:'+d for d in dimensions]),
        'metrics': ",".join(['ga:'+m for m in metrics]),
        'sort': ",".join(['ga:'+s for s in sort]),
        'start-date': start_date.strftime('%Y-%m-%d'),
        'end-date': end_date.strftime('%Y-%m-%d'),
      }
      
      data = urllib.urlencode(data)
      
      response = self.connection.make_request('GET', path=path, data=data)
      #print response.read()