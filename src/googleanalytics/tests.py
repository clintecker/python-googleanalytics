import datetime
import unittest

import googleanalytics
from googleanalytics.exception import GoogleAnalyticsClientError
from googleanalytics import config

class GoogleAnalyticsTest(unittest.TestCase):
    def setUp(self):
        self.connection = googleanalytics.Connection()
        self.valid_profile_ids = config.get_valid_profiles()
        self.end_date = datetime.date.today()
        self.start_date = self.end_date - datetime.timedelta(30)

    def test_goodconnection(self):
        assert self.connection.auth_token is not None

    def test_badconnection(self):
        Connection = googleanalytics.Connection
        try:
            connection = Connection('clintecker@gmail.com', 'fakefake')
        except GoogleAnalyticsClientError, e:
            assert str(e.reason) == "HTTP Error 403: Forbidden"

    def test_accountlist(self):
        for c in range(1, len(self.valid_profile_ids)):
            accounts = self.connection.get_accounts(max_results=c)
            assert len(accounts) == c

    def test_bad_date_order(self):
        start_date = datetime.date(2009, 02, 21)
        end_date = datetime.date(2009, 02, 20)
        account = self.connection.get_account(self.valid_profile_ids[0])
        try:
            data = account.get_data(start_date=start_date, end_date=end_date, metrics=['pageviews'])
        except GoogleAnalyticsClientError, e:
            assert str(e.reason) == "Date orders are reversed"

    def test_dimensions_basic_get_data(self):
        for profile_id in self.valid_profile_ids:
            account = self.connection.get_account(profile_id)
            data = account.get_data(self.start_date, self.end_date, metrics=['pageviews'], dimensions=['browser'])
            assert len(data) > 0
            data = account.get_data(self.start_date, self.end_date, metrics=['pageviews'], dimensions=['pagePath'])
            assert len(data) > 0

    def test_dimensions_basic_get_data_output(self):
        for profile_id in self.valid_profile_ids:
            account = self.connection.get_account(profile_id)
            data = account.get_data(self.start_date, self.end_date, metrics=['pageviews'], dimensions=['browser'], sort=['-pageviews'])
            assert len(data) > 0
            assert isinstance(data.list, list)
            assert isinstance(data.list[0], list)
            assert isinstance(data.tuple, tuple)
            assert isinstance(data.tuple[0], tuple)

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

    def test_paging(self):
        for profile_id in self.valid_profile_ids:
            account = self.connection.get_account(profile_id)
            data = account.get_data(self.start_date, self.end_date, metrics=['pageviews'], dimensions=['pageTitle', 'pagePath'], sort=['-pageviews'])
            max_results = len(data) / 2
            if not max_results:
                print("profileId: %s does not have enough results for `test_paging`" % profile_id)
            data1 = account.get_data(self.start_date, self.end_date, metrics=['pageviews'], dimensions=['pageTitle', 'pagePath'], sort=['-pageviews'], max_results=max_results)
            assert len(data1) == max_results
            data2 = account.get_data(self.start_date, self.end_date, metrics=['pageviews'], dimensions=['pageTitle', 'pagePath'], sort=['-pageviews'], max_results=max_results, start_index=max_results)
            assert len(data2) == max_results
            for value in data1.tuple:
                assert value not in data2

    def test_multiple_dimensions(self):
        for profile_id in self.valid_profile_ids:
            account = self.connection.get_account(profile_id)
            data = account.get_data(self.start_date, self.end_date, metrics=['pageviews', 'timeOnPage', 'entrances'], dimensions=['pageTitle', 'pagePath'], max_results=10)
            for t in data.tuple:
                assert len(t) == 2
                assert len(t[0]) == 2
                assert len(t[1]) == 3

    def test_data_attributes(self):
        for profile_id in self.valid_profile_ids:
            account = self.connection.get_account(profile_id)
            metrics = ['pageviews', 'timeOnPage', 'entrances']
            dimensions = ['pageTitle', 'pagePath']
            data = account.get_data(self.start_date, self.end_date, metrics=metrics, dimensions=dimensions, max_results=10)
            assert data.startDate == self.start_date
            assert data.endDate == self.end_date
            assert len(data.aggregates) == len(metrics)
            for dp in data:
                assert len(dp.metrics) == len(metrics)
                for metric in metrics:
                    assert hasattr(dp, metric)
                assert len(dp.dimensions) == len(dimensions)
                for dimension in dimensions:
                    assert hasattr(dp, dimension)


def test_suite():
    return unittest.makeSuite(GoogleAnalyticsTest)
