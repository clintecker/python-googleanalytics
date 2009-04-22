import unittest
import googleanalytics
from googleanalytics.exception import GoogleAnalyticsClientError
from googleanalytics import config

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
      valid_profile_ids = config.get_valid_profiles()
      for c in range(1, len(valid_profile_ids)):
        accounts = connection.get_accounts(max_results=c)
        assert len(accounts) == c
    
    def test_account_retrieval_unvalidated(self):
      Connection = googleanalytics.Connection
      connection = Connection()
      valid_profile_ids = config.get_valid_profiles()
      for c in range(len(valid_profile_ids)):
        account = connection.get_account(valid_profile_ids[c])
    
    #def test_get_data(self):
    #  Connection = googleanalytics.Connection
    #  connection = Connection()
    #  valid_profile_ids = config.get_valid_profiles()
    #  for c in range(len(valid_profile_ids)):
    #    account = connection.get_account(valid_profile_ids[c])
    #    account.get_data()
    
    def test_basic_filter(self):
      filters = [
        ['country', '==', 'United States'],
      ]
      account = googleanalytics.account.Account()
      filter_string = account.process_filters(filters)
      assert filter_string == 'ga:country==United States'
    
    def test_filter_escaping(self):
      filters = [
        ['country', '==', 'United,States'],
      ]
      account = googleanalytics.account.Account()
      filter_string = account.process_filters(filters)
      assert filter_string == 'ga:country==United\,States'
      filters = [
        ['country', '==', 'United\States'],
      ]
      filter_string = account.process_filters(filters)
      assert filter_string == 'ga:country==United\\\\States'
      
      filters = [
        ['country', '==', 'Uni,tedSt,ates'],
      ]
      filter_string = account.process_filters(filters)
      assert filter_string == 'ga:country==Uni\,tedSt\,ates'
      
      filters = [
        ['country', '==', 'Uni,tedSt;at,es'],
      ]
      filter_string = account.process_filters(filters)
      assert filter_string == 'ga:country==Uni\,tedSt\;at\,es'
    
    def test_bad_operator_rejection(self):
      filters = [
        ['country', '@@', 'United,States'],
      ]
      account = googleanalytics.account.Account()
      filter_string = account.process_filters(filters)
      assert filter_string == ''
      
        
def test_suite():
    return unittest.makeSuite(GoogleAnalyticsTest)
