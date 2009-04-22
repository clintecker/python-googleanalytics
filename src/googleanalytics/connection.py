from googleanalytics.exception import *
import pprint
import re
import urllib
import urllib2

authtoken_pat = re.compile(r"Auth=(.*)")

class GAConnection():
    default_host = 'https://www.google.com/accounts/ClientLogin'
    query_string = {
      'accountType': 'GOOGLE',
      'Email': None,
      'Passwd': None,
      'service': 'analytics',
      'source': 'python-gapi-1.0',
    }

    def __init__(self, google_email, google_password):
      self.query_string['Email'] = google_email
      self.query_string['Passwd'] = google_password
      
      post_data = urllib.urlencode(self.query_string)
      request = urllib2.Request(self.default_host, post_data)

      try:
        response = urllib2.urlopen(request)
      except urllib2.HTTPError, e:
        raise GoogleAnalyticsClientError(e)
        
      auth_token = authtoken_pat.search(response.read())
      self.auth_token = auth_token.groups(0)