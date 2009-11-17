class DataSet(list):
    """docstring for DataSet"""

    def __init__(self):
        list.__init__(self)

    @property
    def list(self):
        return [[r.dimensions, r.metrics] for r in self]

    @property
    def tuple(self):
        return tuple(map(tuple, self.list))

    @property
    def dict(self):
        ds = {}
        for dp in self:
            ds[dp.dimension] = dp.metric
        return ds


class DataPoint:
    """docstring for DataPoint"""

    def __init__(self, account=None, connection=None, title=None, dimensions=None, metrics=None):
        self.account = account
        self.connection = connection
        self.title = title
        self.dimensions = dimensions
        self.metrics = metrics

        if len(self.dimensions) == 1:
            self.dimension = self.dimensions[0]

        if len(self.metrics) == 1:
            self.metric = self.metrics[0]

    def __repr__(self):
        return '<DataPoint: %s / %s>' % (self.account.table_id, self.title)
