from .ose_object import OSEObject

class User(OSEObject):
    def __init__(self, ose):
        super(User, self).__init__(ose)

    def _request_fresh(self):
        return self.ose._do_request('user')
