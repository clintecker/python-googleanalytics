from googleanalytics.exception import GoogleAnalyticsClientError
from googleanalytics import config
from googleanalytics.account import Account
from xml.etree import ElementTree

import re
import urllib
import urllib2

DEBUG = False
PRETTYPRINT = True
TIMEOUT = 10

class GAConnection:
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
        if DEBUG:
            print "Authenticating with %s / %s" % (google_email, google_password)
        response = self.make_request('POST', path=path, data=data)
        auth_token = authtoken_pat.search(response.read())
        self.auth_token = auth_token.groups(0)[0]

    def get_accounts(self, start_index=1, max_results=None):
        path = '/analytics/feeds/accounts/default'
        data = {'start-index': start_index, }
        if max_results:
            data['max-results'] = max_results
        data = urllib.urlencode(data)
        response = self.make_request('GET', path, data=data)
        raw_xml = response.read()
        xml_tree = ElementTree.fromstring(raw_xml)
        account_list = []
        accounts = xml_tree.getiterator('{http://www.w3.org/2005/Atom}entry')
        for account in accounts:
            account_data = {
                'title': account.find('{http://www.w3.org/2005/Atom}title').text,
                'id': account.find('{http://www.w3.org/2005/Atom}id').text,
                'updated': account.find('{http://www.w3.org/2005/Atom}updated').text,
                'table_id': account.find('{http://schemas.google.com/analytics/2009}tableId').text,
            }
            for f in account.getiterator('{http://schemas.google.com/analytics/2009}property'):
                account_data[f.attrib['name']] = f.attrib['value']
            a = Account(
                connection=self,
                title=account_data['title'],
                id=account_data['id'],
                updated=account_data['updated'],
                table_id=account_data['table_id'],
                account_id=account_data['ga:accountId'],
                account_name=account_data['ga:accountName'],
                currency=account_data['ga:currency'],
                time_zone=account_data['ga:timezone'],
                profile_id=account_data['ga:profileId'],
                web_property_id=account_data['ga:webPropertyId'],
            )
            account_list.append(a)
        return account_list

    def get_account(self, profile_id):
        for account in self.get_accounts():
            if account.profile_id == profile_id:
                return account

    def make_request(self, method, path, headers=None, data=''):
        if headers == None:
            headers = {
                'User-Agent': self.user_agent,
                'Authorization': 'GoogleLogin auth=%s' % self.auth_token
            }
        else:
            headers = headers.copy()

        if DEBUG:
            print "** Headers: %s" % (headers,)

        if method == 'GET':
            path = '%s?%s' % (path, data)

        if DEBUG:
            print "** Method: %s" % (method,)
            print "** Path: %s" % (path,)
            print "** Data: %s" % (data,)
            print "** URL: %s" % (self.default_host + path)

        if PRETTYPRINT:
            # Doesn't seem to work yet...
            data += "&prettyprint=true"

        if method == 'POST':
            request = urllib2.Request(self.default_host + path, data, headers)
        elif method == 'GET':
            request = urllib2.Request(self.default_host + path, headers=headers)

        try:
            response = urllib2.urlopen(request, timeout=TIMEOUT)
        except urllib2.HTTPError, e:
            raise GoogleAnalyticsClientError(e)
        return response
