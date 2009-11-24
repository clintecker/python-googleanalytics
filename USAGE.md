Usage
=====

### Getting started ###

You initiate the process by importing the `googleanalytics.Connection` class.  This object is used to authorize against GA and contains the machinery to make requests to GA, and maintains your authorization token.  Speaking of your Google Credentials, you can specify these in two ways.  The first, which I like, is to create a configuration file in your home directory named `.pythongoogleanalytics`.  Populate it like this:

<pre>
[Credentials]
google_account_email = youraccount@gmail.com
google_account_password = yourpassword
</pre>

The second method is to supply the credentials directly to the Connection object in your code like so:

<pre>
>>> from googleanalytics import Connection
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
</pre>

If you are using the former (~/.pythongoogleanalytics) method, you can just make naked `Connection()` calls to set up your connection object.

### Listing/getting accounts ###

You can retrieve a list of profiles associated with your account like so:

<pre>
>>> from googleanalytics import Connection
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> accounts = connection.get_accounts()
</pre>

This will return a list of account objects which you could use to retrieve data.  The `Connection.get_accounts` method also accepts pagination parameters:

`>>> accounts = connection.get_accounts(start_index=10, max_results=5)`

Both are optional. `start_index` defaults to 1 (the listing is 1-indexed), and `max_results` defaults to `None` which means a naked call just returns all your accounts.

*Alternatively*: If you know the profile ID you want to use, you can use the `Connection.get_account` method.  This currently does no validation, so if you provide an invalid profile ID you can expect things to break. It works like you might expect:

`>>> account = connection.get_account('1234')`

### Retrieving Data ###

Once you have an `Account` object you can start pulling data from it.  Reports are built by specifying a combinations of _dimensions_ and _metrics_.  Dimensions are things like Browsers, Platforms, PagePath. Metrics are generally numerical data like pageviews, visits, percentages, elapsed time, and so forth.  Google has a [long reference to these here](http://code.google.com/apis/analytics/docs/gdata/gdataReferenceDimensionsMetrics.html).

Google specifies all these with `ga:` prepended to each dimension or metric.  Right now I require you don't specify the `ga:` part.  What I mean is that when you want `ga:pagePath` you pass in `pagePath`.  Leave off the `ga:` for now.

`get_data()` has three required arguments. You must provide start and end dates as the first two positional arguments, respectively, and they can be either `datetime.datetime` or `datetime.date` objects.  These dates bound the time frame for the data you request.  If you only want data for a single day, the start and end dates should be identical (the end date is inclusive).  `metrics` is the only other required argument and can be passed as the third positional argument or as a keyword argument.  However, it must be a list containing at least one valid metric to form a proper request.

In addition to dimensions and metrics you can specify sorting and filtering parameters, both optional.  

Here's a really basic call:

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> data = account.get_data(start_date, end_date, metrics=['pageviews'])
>>> data.list
[[[], [4567]]]
</pre>

You can optionally retrieve metrics by various dimensions, such as a list of browsers that accessed your site in your timeframe and how many page views each of those browsers generated.

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> data = account.get_data(start_date, end_date, metrics=['pageviews'], dimensions=['browser',])
>>> data.list
[[['Chrome'], [43293]], [['Firefox'], [6367750]], [['Internet Explorer'], [5391084]], [['Mozilla Compatible Agent'],[238179]], [['Safari'], [567432]]]
</pre>

You could get Google to sort that for you (note FireFox is first now):

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> data = account.get_data(start_date, end_date, metrics=['pageviews',], dimensions=['browser',], sort=['pageviews',])
>>> data.list
[[['Firefox'], [6367750]], [['Internet Explorer'], [5391084]], [['Safari'], [567432]], [['Mozilla Compatible Agent'],[238179]], [['Chrome'], [43293]]]
</pre>

And you could do some fun filtering, get a list of browsers, sorted descending by page views, and filtered to only contain browser strings which match the three regexs below (starting with Fire OR Internet OR Saf):

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> filters = [
...   ['browser', '=~', '^Fire', 'OR'],
...   ['browser', '=~', '^Internet', 'OR'],
...   ['browser', '=~', '^Saf'],
... ]
>>> data = account.get_data(start_date, end_date, metrics=['pageviews',], dimensions=['browser',], sort=['-pageviews',], filters=filters)
>>> data.list
[[['Firefox'], [6367750]], [['Internet Explorer'], [5391084]], [['Safari'], [567432]]]
</pre>

### Data ###

At this point you should be asking me how this data is returned to you.  In the above examples, the data is returned as a `googleanalytics.data.DataSet` object which is essentially a Python list with two shortcut "properties" (`list`/`tuple`) added to it.  This list is populated with `googleanalytics.data.DataPoint` objects.  Each `DataPoint` has `dimensions` and `metrics` properties, which are just arrays of `googleanalytics.data.Dimension` and `googleanalytics.data.Metric` objects respectively.

So how do you get useful data?  The quickest path to the dimension and metric data is to output the whole dataset as a list of lists or a tuple of tuples.  Example:

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> data = account.get_data(start_date, end_date, metrics=['pageviews',], dimensions=['browser',], sort=['-pageviews',])
>>> data.list
[[['Firefox'], [21]], [['Internet Explorer'], [17]], [['Safari'], [17]], [['Chrome'], [6]], [['Mozilla Compatible Agent'], [5]]]
>>> data.tuple
((['Firefox'], [21]), (['Internet Explorer'], [17]), (['Safari'], [17]), (['Chrome'], [6]), (['Mozilla Compatible Agent'], [5]))
</pre>

`list` and `tuple` will retain the sorting order of the Google Analytics results.  Each item in `list` or `tuple` are an ordered pair of lists.  The first list is the dimensions (which will be an empty list if no dimensions were defined). The second list contains the metrics, in the order they were requested in the get_data call.


#### Pulling multiple dimensions/metrics ####

Patrick Collison has graciously implemented pulling multiple metrics and data in a single request.  Instead of simply passing in a list with one metric or dimension, pass in as many as you like<sup>1</sup>.  The metrics will be returned in the order they were requested in the get_data call.

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> end_date = datetime.datetime.today()
>>> start_date = end_date-datetime.timedelta(days=2)
>>> metrics = ['pageviews','timeOnPage','entrances']
>>> dimensions = ['pageTitle', 'pagePath']
>>> data = account.get_data(start_date, end_date, metrics=metrics, dimensions=dimensions, max_results=1)
>>> data.list
[[[u'How to find out more about Clint Ecker - Django Developer', u'/'], [5, '0.0', 5]]]
>>> for row in data.list:
...     print dict(zip(dimensions, row[0]))
...     print dict(zip(metrics, row[1]))
...     print '.'*50
...
{'pageTitle': u'How to find out more about Clint Ecker - Django Developer', 'pagePath': u'/'}
{'entrances': 5, 'pageviews': 5, 'timeOnPage': u'0.0'}
</pre>

1: The Google Analytics API allows a maximum of 10 metrics and 7 dimensions for a given query, although not every metric/dimension combination is valid. See [the official docs](http://code.google.com/intl/en-US/apis/analytics/docs/gdata/gdataReferenceValidCombos.html) for more details.

#### Working with `Dimension` and `Metric` objects ####

Google Analytics returns far more data than just the metrics and dimensions. As such, `DataSet` (and the `DataPoint` objects the `DataSet` contains) have many attributes which make this data available.  For more information on the exact data that is returned, [see the official docs](http://code.google.com/intl/en-US/apis/analytics/docs/gdata/gdataReferenceDataFeed.html#dataResponse).  In short, all of the top-level Data Feed attributes are direct attributes of the `DataSet` instance and all of the `entry` attributes of the Data Feed are direct attributes of the `DataPoint` instances.  These attributes are named identically to the names used in the returned Data Feed, with the leading xml namespace removed (e.g. 'dxp:startDate' becomes simply 'startDate').

Assume the following code as given in the following examples:

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> end_date = datetime.datetime.today()
>>> start_date = end_date-datetime.timedelta(days=2)
>>> metrics = ['pageviews','timeOnPage','entrances']
>>> dimensions = ['pageTitle', 'pagePath']
>>> dataset = account.get_data(start_date, end_date, metrics=metrics, dimensions=dimensions, max_results=1)
</pre>

One example of a `DataSet` level attribute is the property 'aggregates' which is an array of `Metric` objects. This property is aggregate metric data, irrespective of any dimensions for the given time span:
<pre>
>>> dataset.aggregates
[<googleanalytics.data.Metric object at 0x102094b10>, <googleanalytics.data.Metric object at 0x102094ed0>, <googleanalytics.data.Metric object at 0x102094f10>]
>>> for metric in dataset.aggregates:
...     print "%s => %s" % (metric.name, metric.value)
...
pageviews => 217870
timeOnPage => 1.2157589E7
entrances => 63873
</pre>

The aggregate metric values are also available as direct attributes of the `DataSet` object:

<pre>
>>> dataset.pageviews
217870
>>> dataset.timeOnPage
1.2157589E7
>>> dataset.entrances
63873
</pre>

`DataPoint` objects are comprised of `Metric` and `Dimension` objects (if applicable).  These metrics and dimensions are available directly through arrays:

<pre>
>>> dataset
[<googleanalytics.data.DataPoint object at 0x102094f50>]
>>> datapoint = dataset[0]
>>> datapoint.metrics
[<googleanalytics.data.Metric object at 0x102094b10>, <googleanalytics.data.Metric object at 0x102094ed0>, <googleanalytics.data.Metric object at 0x102094f10>]
>>> datapoint.dimensions
[<googleanalytics.data.Dimension object at 0x1020990d0>, <googleanalytics.data.Dimension object at 0x102099110>]
</pre>

As with the aggregates array attribute of `DataSet`, each of these metrics and dimensions are also direct attributes of the `DataPoint` object:

<pre>
>>> datapoint.pageviews
5
>>> datapoint.timeOnPage
u'0.0'
>>> datapoint.entrances
5
>>> datapoint.pageTitle
u'How to find out more about Clint Ecker - Django Developer'
>>> datapoint.pagePath
u'/'
</pre> 

If you really need the low level data for each metric, then you should iterate through the `metrics` array of the `DataPoint` instance:

<pre>
>>> metric = datapoint.metrics[0]
>>> metric.name
u'pageviews'
>>> metric.value
5
>>> metric.type
u'integer'
>>> metric.confidenceInterval
u'0.0'
</pre>

For now, all metric values are returned as strings except in the case of when `type` is `u'integer'`. The code will cast the metric value as an integer in this case.

#### Pagination in data results ####

Robert Kosera has added `max_results` and `start_index` to `account.get_data` and they work just like you might expect.  There are examples in tests.py