Installation
============

Theoretically you should be able to type the following after checking out the source:

`sudo python setup.py install`

You can also just install using `easy_install` like so:

`sudo easy_install python-googleanalytics`

Alternatively you may choose to use python-googleanalytics in a large project (most likely).  You can pass "python-googleanalytics" to any dependency manager (pip, buildout) to pull it into your development, production, or virtual environment for whatever reason you like.

## Development ##

I'm trying to use Buildout, so you can start helping out with development by checking out the source and typing the following:

<pre>
git clone git://github.com/clintecker/python-googleanalytics.git
python bootstrap.py && ./bin/buildout
</pre>

Once you've done these steps, you should be able to run a Python interpreter that has access to our module with the following command:

`./bin/python`

It should work like so:

<pre>
(python-googleanalytics)[master][~/src/python-googleanalytics] ./bin/python

>>> import googleanalytics
>>> 
</pre>

The system Python interpreter would not be able to pick up the module unless installed systemwide:

<pre>
[~] python
Python 2.5.1 (r251:54863, Jul 23 2008, 11:00:16) 
[GCC 4.0.1 (Apple Inc. build 5465)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import googleanalytics
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named googleanalytics
>>>
</pre>

### Environments ###

I strongly suggest developing in a virtual environment using [virtualenv](http://pypi.python.org/pypi/virtualenv) with its own Python interpreter.  You don't have to, but you might find your python development experience is a little nicer.

If you plan on using virtualenv, I then highly reccomend you get Doug Hellmann's `virtualenvwrapper` running which simplified the process of creating and managing virtual environment like so:

*Switching to a new environment:*

<pre>
[~] workon python-googleanalytics
(python-googleanalytics)[~]
</pre>

*Listing environments:*

<pre>
(python-googleanalytics)[~] workon
ars-django-project
ars_shortner
google_traffic
python-googleanalytics
test
writer_tracker
(python-googleanalytics)[~]
</pre>

*Creating new environments:*

<pre>
(python-googleanalytics)[~] mkvirtualenv test2
New python executable in test2/bin/python
Installing setuptools............done.
(test2)[~]
</pre>

## Testing ##
You will need to create a `.pythongoogleanalytics` configuration file in your home directory with the following settings (replacing the values with a valid Google Analytics account and profile ids) in order for the tests to run:

<pre>
[Credentials]
google_account_email = youraccount@gmail.com
google_account_password = yourpassword

[Accounts]
test_profile_ids = 1234 5678
</pre>

Run tests as follows (once you've bootstrapped buildout or installed the module globally):

`./bin/test`