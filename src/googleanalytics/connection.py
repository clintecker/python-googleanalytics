from googleanalytics.exception import *
from googleanalytics import handler, config
import xml.sax
import pprint
import re
import urllib
import urllib2

DEBUG = False

class GAConnection():
  default_host = 'https://www.google.com'
  user_agent = 'python-gapi-1.0'
  auth_token = None

  def __init__(self, google_email=None, google_password=None):  
    authtoken_pat = re.compile(r"Auth=(.*)")
    path = '/accounts/ClientLogin'
    
    if google_email == None or google_password == None:
      google_email, google_password = config.get_google_credentials()
      
    data = "accountType=GOOGLE&Email=%s&Passwd=%s&service=analytics&source=%s"
    data = data % (google_email, google_password, self.user_agent)

    response = self.make_request('POST', path=path, data=data)
    auth_token = authtoken_pat.search(response.read())
    self.auth_token = auth_token.groups(0)[0]
    
  def get_accounts(self, start_index=1, max_results=None):
    path = '/analytics/feeds/accounts/default'
    data = { 'start-index': start_index,}
    if max_results:
      data['max-results'] = max_results
    data = urllib.urlencode(data)
    response = self.make_request('GET', path, data=data)
    print response.read()
    
  def make_request(self, method, path, headers=None, data=''):
    if headers == None:
      headers = {
        'User-Agent': self.user_agent,
        'Authorization': 'GoogleLogin auth=%s' % self.auth_token 
      }
    else:
      headers = headers.copy() 
      
    if not headers.has_key('Content-Length'):
      headers['Content-Length'] = str(len(data))
     
    if DEBUG:
      print "** Headers: %s" % (headers,)
         
    if method == 'GET':
      path = '%s?%s' % (path, data)
      data = ''
    
    request = urllib2.Request(self.default_host + path, data)
    
    try:
      response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
      raise GoogleAnalyticsClientError(e)
    return response