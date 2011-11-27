# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

import os
import sys
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, "..", "src"))


from openshift import *

class TestUserInfo(unittest.TestCase):
    '''
	Test the OpenShift.get_user_info() method
    '''

    def test_missing_user(self):
	oshift = OpenShift(rhlogin='nosuchlogin', password='123456')
	try:
	    info = oshift.get_user_info()
	except OpenShiftLoginFailedException:
	    self.assertTrue(True)
	    return

	self.assertTrue(False)

    def test_wrong_password(self):
	self.assertTrue(os.environ.has_key('OPENSHIFT_USER'), 'Provide OpenShift username!')
	oshift = OpenShift(rhlogin=os.environ['OPENSHIFT_USER'], password='123456')
	try:
	    info = oshift.get_user_info()
	except OpenShiftLoginFailedException:
	    self.assertTrue(True)
	    return

	self.assertTrue(False)

    def test_user_info(self):
	self.assertTrue(os.environ.has_key('OPENSHIFT_USER'), 'Provide OpenShift username!')
	self.assertTrue(os.environ.has_key('OPENSHIFT_PASSWORD'), 'Provide OpenShift password!')
	oshift = OpenShift(rhlogin=os.environ['OPENSHIFT_USER'], password=os.environ['OPENSHIFT_PASSWORD'])
	info = oshift.get_user_info()
	self.assertTrue(info.has_key('user_info'))
	self.assertTrue(info.has_key('app_info'))


if __name__ == '__main__':
    unittest.main()
