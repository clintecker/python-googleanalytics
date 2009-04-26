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

In addition to dimensions and metrics you can specify sorting and filtering parameters, both optional.  *Definitely required* though are lower and upper bounds to the time frame you wish to gather data from.  These can be `datetime.datetime` or `datetime.date` objects.  Here's a really basic call:

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> account.get_data(start_date=start_date, end_date=end_date)
[]
</pre>

This will, of course, return no data (no dimensions or metrics specified), but is valid.

Here's one that would give you some good data, a list of browsers that accessed your site in your timeframe and how many page views each of those browsers generated.

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> account.get_data(start_date=start_date, end_date=end_date, dimensions=['browser',], metrics=['pageviews',])
[&lt;DataPoint: ga:6367750 / ga:browser=Chrome&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Firefox&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Internet Explorer&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Mozilla Compatible Agent&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Safari&gt;]
</pre>

You could get Google to sort that for you (note FireFox is first now):

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> account.get_data(start_date=start_date, end_date=end_date, dimensions=['browser',], metrics=['pageviews',], sort=['-pageviews',])
[&lt;DataPoint: ga:6367750 / ga:browser=Firefox&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Internet Explorer&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Safari&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Chrome&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Mozilla Compatible Agent&gt;]
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
>>> account.get_data(start_date=start_date, end_date=end_date, dimensions=['browser',], metrics=['pageviews',], sort=['-pageviews',], filters=filters)
[&lt;DataPoint: ga:6367750 / ga:browser=Firefox&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Internet Explorer&gt;, &lt;DataPoint: ga:6367750 / ga:browser=Safari&gt;]
</pre>

### Data ###

At this point you should be asking me how this data is returned to you.  In the above examples, the data is returned as a `googleanalytics.data.DataSet` object which is essentially a Python list with three "properties" (`list`/`tuple`/`dict`) added to it.  This list is populated with `googleanalytics.data.DataPoint` objects.  Each of these has an associated dimension and metric (i.e. "Firefox" and "30293") and a little more data.

So how do you get useful data?  You _could_ iterate over the `DataSet` and access each `DataPoint`'s metric and dimension properties directly, or you could output the whole dataset as a list of lists, tuple or tuples, or dictionary.  Example:

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> start_date = datetime.date(2009, 04, 10)
>>> end_date = datetime.date(2009, 04, 10)
>>> data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['browser',], metrics=['pageviews',], sort=['-pageviews',])
>>> data.list
[['Firefox', 21], ['Internet Explorer', 17], ['Safari', 17], ['Chrome', 6], ['Mozilla Compatible Agent', 5]]
>>> data.tuple
(('Firefox', 21), ('Internet Explorer', 17), ('Safari', 17), ('Chrome', 6), ('Mozilla Compatible Agent', 5))
>>> data.dict
{'Chrome': 6, 'Internet Explorer': 17, 'Firefox': 21, 'Safari': 17, 'Mozilla Compatible Agent': 5}
</pre>

If you're concerned with the sort-order, you shouldn't really use the `dict` output as order isn't guaranteed.  `list` and `tuple` will retain the sorting order that Google Analytics output the data in.

If you don't add these, we can't really test any future data pulling, and some of the account stuff.  In the future perhaps we can build a list of accounts from get_all_accounts and proceed that way.

#### Pulling multiple dimensions/metrics ####

Patrick Collison has graciously implemented pulling multiple metrics and data in a single request.  Instead of simple passing in a list with one metric or dimension, pass in as many as you like<sup>1</sup>

<pre>
>>> from googleanalytics import Connection
>>> import datetime
>>> connection = Connection('clintecker@gmail.com', 'fakefake')
>>> account = connection.get_account('1234')
>>> end_date = datetime.datetime.today()
>>> start_date = end_date-datetime.timedelta(days=2)
>>> data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['pageTitle', 'pagePath'], metrics=['pageviews','timeOnPage','entrances'], max_results=10)
>>> data
[<DataPoint: ga:7337113 / ga:pageTitle=How to find out more about Clint Ecker - Django Developer | ga:pagePath=/>]
>>> data.tuple
((['How to find out more about Clint Ecker - Django Developer', '/'], [5, '0.0', 5]),)
</pre>

1: The Google Analytics generally caps you out around 7 or 10 as a maximum, so don't go too crazy ;)

#### Pagination in data results ####

Robert Kosera has added `max_results` and `start_index` to `account.get_data` and they work just like you might expect.  There are examples in tests.py