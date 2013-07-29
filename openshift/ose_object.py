class OSEObject(object):
    """Superclass to all OSE objects that hold data about remote API."""
    def __init__(self, ose):
        self.ose = ose
        self.refresh()

    def refresh(self):
        """Reloads all info about this object.

        Uses _request_fresh() method defined by subclasses to obtain
        fresh response.
        """
        self._response = self._request_fresh()
        self._json = self._response.json()

    def _request_fresh(self):
        raise NotImplementedError('Class {cls} doesn\'t implement _request_fresh method.'.\
                format(cls=type(self)))

    def __getattr__(self, attr):
        return self._response.json()['data'][attr]
