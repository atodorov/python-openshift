"""
 Copyright (c) 2011, Open Technologies Bulgaria, Ltd. <http://otb.bg>
 Author: Alexander Todorov <atodorov@nospam.otb.bg>

 Tests for the cartridges list functionality.
"""

import os
import sys
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, ".."))


from openshift import OpenShiftExpress, OpenShiftException

class TestCartList(unittest.TestCase):
    '''
        Test the OpenShiftExpress.get_cartridges_list() method
    '''

    def test_get_cart_list(self):
        '''If the list is not empty then PASS'''
        print "TEST: Getting list of standalone cartridges ..."
        oshift = OpenShiftExpress(rhlogin=None, password=None)
        carts = oshift.get_cartridges_list()
        self.assertTrue(len(carts) > 0)
        print carts

    def test_get_cart_list_embedded(self):
        '''If the list is not empty then PASS'''
        print "TEST: Getting list of embedded cartridges ..."
        oshift = OpenShiftExpress(rhlogin=None, password=None)
        carts = oshift.get_cartridges_list('embedded')
        self.assertTrue(len(carts) > 0)
        print carts

    def test_get_cart_list_unknown(self):
        '''If the list is not empty then PASS'''
        print "TEST: Getting list of unknown cartridges ..."
        oshift = OpenShiftExpress(rhlogin=None, password=None)
        try:
            carts = oshift.get_cartridges_list('unknown')
        except OpenShiftException as e:
            self.assertTrue(True)
            print e


if __name__ == '__main__':
    unittest.main()
