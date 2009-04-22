A Python client for accessing Google Analytics data
===================================================

Not much info here but I'm working off the documentation [here](http://code.google.com/apis/analytics/docs/gdata/gdataDeveloperGuide.html)

### Credentials ###

You should put your Google Credentials in a file in your home directory called `.pythongoogleanalytics`. This is a ini style config file and should look like this:

<pre>
[Credentials]
google_account_email = clintecker@gmail.com
google_account_password = sn00pd4w6
</pre>

### Installation ###

Theoretically you should be able to type the following after checking out the source:

`sudo python setup.py install`

### Development ###

I'm trying to use Buildout, so you can start helping out with development by checking out the source and typing the following:

`python bootstrap.py`
`./bin/buildout`

Run tests as follows:

`./bin/test`

Most of the action is in `googleanalytics.connection` for the moment.

### Usage ###

Check out the `tests.py` file for details on how to use the library.  There's not much here at the moment.

If it's not obvious I've modeled a lot of of what I've done so far off the [Boto Amazon Web Services client](http://code.google.com/p/boto/).