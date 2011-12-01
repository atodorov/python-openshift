"""
 Copyright (c) 2011, Open Technologies Bulgaria, Ltd. <http://otb.bg>
 Author: Alexander Todorov <atodorov@nospam.otb.bg>

 Tests for application control functionality.
"""

import os
import sys
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, ".."))


from openshift import OpenShiftExpress

class TestApplicationControl(unittest.TestCase):
    '''
        Test OpenShiftExpress application control methods
    '''

    def test_start_app(self):
        self.assertTrue(os.environ.has_key('OPENSHIFT_USER'), 'Provide OpenShift username!')
        self.assertTrue(os.environ.has_key('OPENSHIFT_PASSWORD'), 'Provide OpenShift password!')
        oshift = OpenShiftExpress(rhlogin=os.environ['OPENSHIFT_USER'], password=os.environ['OPENSHIFT_PASSWORD'])

#	oshift.start_application(self.app_name)
        self.assertTrue(False) # not implemented. FAIL


if __name__ == '__main__':
    unittest.main()
