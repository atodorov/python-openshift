from .ose_object import OSEObject
from .domain_list import DomainList

class User(OSEObject):
    def __init__(self, ose):
        super(User, self).__init__(ose)

    def _request_fresh(self):
        return self.ose._do_request('user')

    def get_domains(self):
        """Return DomainList object containing domains associated with current user.
        """
        return DomainList(self.ose)
