class DataPoint:
  """docstring for DataPoint"""
  
  def __init__(self, account=None, connection=None, title=None, dimensions=[], metrics=[]):
    self.account = account
    self.connection = connection
    self.title = title
    self.dimensions = dimensions
    self.metrics = metrics
  
  def __repr__(self):
    return '<DataPoint: %s / %s>' % (self.account.title, self.title)