# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

import os
import sys
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, "..", "src"))


from openshift import *

class TestCartList(unittest.TestCase):
    '''
	Test the OpenShift.get_cartridges_list() method
    '''

    def test_user_info(self):
	oshift = OpenShift(rhlogin=None, password=None)
	carts = oshift.get_cartridges_list()
	self.assertTrue(len(carts) > 0)


if __name__ == '__main__':
    unittest.main()
