"""
 Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

 Tests for the cartridges list functionality.
"""

import os
import sys
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, ".."))


from openshift import OpenShiftExpress

class TestCartList(unittest.TestCase):
    '''
        Test the OpenShiftExpress.get_cartridges_list() method
    '''

    def test_get_cart_list(self):
        '''If the list is not empty then PASS'''
        oshift = OpenShiftExpress(rhlogin=None, password=None)
        carts = oshift.get_cartridges_list()
        self.assertTrue(len(carts) > 0)


if __name__ == '__main__':
    unittest.main()
