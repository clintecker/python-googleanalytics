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
      account_list = connection.get_accounts(max_results=1)
      assert len(account_list) == 1
      assert account_list[0].title != ''
      account_list = connection.get_accounts(max_results=2)
      assert len(account_list) == 2
      assert account_list[0].title != ''
        
def test_suite():
    return unittest.makeSuite(GoogleAnalyticsTest)
