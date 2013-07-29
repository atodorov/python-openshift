from .ose_object import OSEObject

class Domain(OSEObject):
    def __init__(self, ose, id):
        self.id = id
        super(Domain, self).__init__(ose)

    def _request_fresh(self):
        return self.ose._do_request('domains/{id}/'.format(id=self.id))
