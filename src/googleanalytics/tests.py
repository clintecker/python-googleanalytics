import datetime
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
  
  def test_bad_date_order(self):
    Connection = googleanalytics.Connection
    connection = Connection()
    valid_profile_ids = config.get_valid_profiles()
    
    start_date = datetime.date(2009, 02, 21)
    end_date = datetime.date(2009, 02, 20)
    account = connection.get_account(valid_profile_ids[0])
    try:
      data = account.get_data(start_date=start_date, end_date=end_date)
    except GoogleAnalyticsClientError, e:
      assert str(e.reason) == "Date orders are reversed"
      
  def test_basic_get_data_no_params(self):
    Connection = googleanalytics.Connection
    connection = Connection()
    valid_profile_ids = config.get_valid_profiles()
    
    start_date = datetime.date(2009, 04, 10)
    end_date = datetime.date(2009, 04, 10)
    
    for c in range(len(valid_profile_ids)):
      account = connection.get_account(valid_profile_ids[c])
      data = account.get_data(start_date=start_date, end_date=end_date)
      assert len(data) == 0
      
  def test_dimensions_basic_get_data(self):
    Connection = googleanalytics.Connection
    connection = Connection()
    valid_profile_ids = config.get_valid_profiles()
  
    start_date = datetime.date(2009, 04, 10)
    end_date = datetime.date(2009, 04, 10)
  
    for c in range(len(valid_profile_ids)):
      account = connection.get_account(valid_profile_ids[c])
      data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['browser',], metrics=['pageviews',])
      assert len(data) > 0
      data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['pagePath',], metrics=['pageviews',])
      assert len(data) > 0

  def test_dimensions_basic_get_data_output(self):
    Connection = googleanalytics.Connection
    connection = Connection()
    valid_profile_ids = config.get_valid_profiles()

    start_date = datetime.date(2009, 04, 10)
    end_date = datetime.date(2009, 04, 10)

    for c in range(len(valid_profile_ids)):
      account = connection.get_account(valid_profile_ids[c])
      data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['browser',], metrics=['pageviews',], sort=['-pageviews',])
      assert len(data) > 0
      assert isinstance(data.list, list)
      assert isinstance(data.list[0], list)
      assert isinstance(data.tuple, tuple)
      assert isinstance(data.tuple[0], tuple)
      assert isinstance(data.dict, dict)
      
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
    
  def test_multiple_filters(self):
    filters = [
      ['country', '==', 'United States', 'AND'],
      ['country', '==', 'Canada']
    ]
    account = googleanalytics.account.Account()
    filter_string = account.process_filters(filters)
    assert filter_string == 'ga:country==United States;ga:country==Canada'
    
    filters = [
      ['city', '=~', '^L', 'AND'],
      ['browser', '=~', '^Fire']
    ]
    filter_string = account.process_filters(filters)
    assert filter_string == 'ga:city=~^L;ga:browser=~^Fire'
    
    filters = [
      ['browser', '=~', '^Fire', 'OR'],
      ['browser', '=~', '^Internet', 'OR'],
      ['browser', '=~', '^Saf'],
    ]
    filter_string = account.process_filters(filters)
    assert filter_string == 'ga:browser=~^Fire,ga:browser=~^Internet,ga:browser=~^Saf'
    
  def test_multiple_filters_mix_ops(self):
    filters = [
      ['browser', '=~', 'Firefox', 'AND'],
      ['browser', '=~', 'Internet (Explorer|Exploder)', 'OR'],
      ['city', '=@', 'York', 'OR'],
      ['state', '!=', 'California', 'AND'],
      ['timeOnPage', '<', '10'],
    ]
    account = googleanalytics.account.Account()
    filter_string = account.process_filters(filters)
    assert filter_string == 'ga:browser=~Firefox;ga:browser=~Internet (Explorer|Exploder),ga:city=@York,ga:state!=California;ga:timeOnPage<10'

  # for this to work, the test account has to track at least 20 pages
  def test_paging(self):
    Connection = googleanalytics.Connection
    connection = Connection()
    valid_profile_ids = config.get_valid_profiles()

    end_date = datetime.datetime.today()
    start_date = end_date-datetime.timedelta(days=2)

    for c in range(len(valid_profile_ids)):
      account = connection.get_account(valid_profile_ids[c])
      data1 = account.get_data(start_date=start_date, end_date=end_date, dimensions=['pageTitle', 'pagePath'], metrics=['pageviews',], sort=['-pageviews',], max_results=10)
      assert len(data1) == 10
      data2 = account.get_data(start_date=start_date, end_date=end_date, dimensions=['pageTitle', 'pagePath'], metrics=['pageviews',], sort=['-pageviews',], max_results=10, start_index=11)
      #print data2.tuple
      assert len(data2) == 10
      for value in data1.tuple:
      	assert value not in data2

  def test_multiple_dimensions(self):
    Connection = googleanalytics.Connection
    connection = Connection()
    valid_profile_ids = config.get_valid_profiles()

    end_date = datetime.datetime.today()
    start_date = end_date-datetime.timedelta(days=2)

    for c in range(len(valid_profile_ids)):
      account = connection.get_account(valid_profile_ids[c])
      data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['pageTitle', 'pagePath'], metrics=['pageviews','timeOnPage','entrances'], max_results=10)
      for t in data.tuple:
        #print t
        assert len(t) == 2
        assert len(t[0]) == 2
        assert len(t[1]) == 3

def test_suite():
  return unittest.makeSuite(GoogleAnalyticsTest)
