from googleanalytics.exception import *
from googleanalytics import handler
import xml.sax
import pprint
import re
import urllib
import urllib2


class GAConnection():
  default_host = 'https://www.google.com'
  user_agent = 'python-gapi-1.0'
  query_string = {
    'accountType': 'GOOGLE',
    'Email': None,
    'Passwd': None,
    'service': 'analytics',
    'source': user_agent,
  }
  auth_token = None

  def __init__(self, google_email, google_password):
    self.query_string['Email'] = google_email
    self.query_string['Passwd'] = google_password

    authtoken_pat = re.compile(r"Auth=(.*)")
    path = '/accounts/ClientLogin'

    response = self.make_request(path=path, data=self.query_string)
    auth_token = authtoken_pat.search(response.read())
    self.auth_token = auth_token.groups(0)[0]
    
  def make_request(self, path, headers=None, data=''):
    if headers == None:
      headers = {
        'User-Agent': self.user_agent,
        'Authorization': 'GoogleLogin auth=%s' % self.auth_token 
      }
    else:
      headers = headers.copy()
    
    if data != '':
      data = urllib.urlencode(data)
    if not headers.has_key('Content-Length'):
      headers['Content-Length'] = str(len(data))
    request = urllib2.Request(self.default_host + path, data)
    try:
      response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
      raise GoogleAnalyticsClientError(e)
    return response