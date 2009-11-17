class GoogleAnalyticsClientError(Exception):
    """
    General Google Analytics error (error accessing GA)
    """

    def __init__(self, reason):
        self.reason = reason

    def __repr__(self):
        return 'GAError: %s' % self.reason

    def __str__(self):
        return 'GAError: %s' % self.reason
