class Account:
    def __init__(self, connection=None, title=None, link=None,
      account_id=None, account_name=None, profile_id=None,
      web_property_id=None):
        self.connection = connection
        self.title = title
        self.link = link
        self.account_id = account_id
        self.account_name = account_name
        self.profile_id = profile_id
        self.web_property_id = web_property_id
        self.table_id = 'ga:' + self.profile_id

    def __repr__(self):
      if self.title:
        return '<Account: %s>' % self.title
      elif self.table_id:
        return '<Account: %s>' % self.table_id