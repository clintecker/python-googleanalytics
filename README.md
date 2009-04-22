A Python client for accessing Google Analytics data
===================================================

Not much info here but I'm working off the documentation [here](http://code.google.com/apis/analytics/docs/gdata/gdataDeveloperGuide.html)

### Credentials ###

You should put your Google Credentials in a file in your home directory called `.pythongoogleanalytics`. This is a ini style config file and should look like this:

<pre>
[Credentials]
google_account_email = youraccount@gmail.com
google_account_password = yourpassword
</pre>

If you want to take full advantage of the test suite, you'll need to add another section with a few valid profile IDs from the account you're testing.  Add these as follows:

<pre>
[Accounts]
test_profile_ids = 28192 1928329 1029
</pre>

If you don't add these, we can't really test any future data pulling, and some of the account stuff.  In the future perhaps we can build a list of accounts from get_all_accounts and proceed that way.

### Installation ###

Theoretically you should be able to type the following after checking out the source:

`sudo python setup.py install`

### Development ###

I'm trying to use Buildout, so you can start helping out with development by checking out the source and typing the following:

`python bootstrap.py && ./bin/buildout`

Run tests as follows:

`./bin/test`

Most of the action is in `googleanalytics.connection` for the moment.

### Usage ###

Check out the `tests.py` file for details on how to use the library.  There's not much here at the moment.

If it's not obvious I've modeled a lot of of what I've done so far off the [Boto Amazon Web Services client](http://code.google.com/p/boto/).