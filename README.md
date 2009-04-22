A Python client for accessing Google Analytics data
===================================================

Not much info here but I'm working off the documentation here:

http://code.google.com/apis/analytics/docs/gdata/gdataDeveloperGuide.html

You should put your Google Credentials in a file in your home directory called `.pythongoogleanalytics`. This is a ini style config file and should look like this:

`
[Credentials]
google_account_email = clintecker@gmail.com
google_account_password = sn00pd4w6
`

Check out the `tests.py` file for details on how to use the library.  There's not much here at the moment.

If it's not obvious I've modeled a lot of of what I've done so far off the [Boto Amazon Web Services client](http://code.google.com/p/boto/).