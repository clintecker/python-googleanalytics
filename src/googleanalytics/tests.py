import unittest
import googleanalytics
from googleanalytics.exception import GoogleAnalyticsClientError

class GoogleAnalyticsTest(unittest.TestCase):
    def test_goodconnection(self):
      Connection = googleanalytics.Connection
      connection = Connection()
      assert connection.auth_token is not None

    def test_badconnection(self):
      Connection = googleanalytics.Connection
      try:
        connection = Connection('clintecker@gmail.com', 'fakefake')
      except GoogleAnalyticsClientError, e:
        assert str(e.reason) == "HTTP Error 403: Forbidden"
          
    def test_accountlist(self):
      Connection = googleanalytics.Connection
      connection = Connection()
      account_list = connection.get_accounts()
        
def test_suite():
    return unittest.makeSuite(GoogleAnalyticsTest)
