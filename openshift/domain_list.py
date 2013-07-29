from .domain import Domain
from .ose_object import OSEObject

class DomainList(OSEObject):
    def __init__(self, ose):
        super(DomainList, self).__init__(ose)
        self.domain_list = []
        for d in self._json['data']:
            self.append(Domain(ose, id=d['id']))

    def _request_fresh(self):
        return self.ose._do_request('domains')

    def append(self, domain):
        return self.domain_list.append(domain)
