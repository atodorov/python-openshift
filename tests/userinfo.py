"""
 Copyright (c) 2011, Open Technologies Bulgaria, Ltd. <http://otb.bg>
 Author: Alexander Todorov <atodorov@nospam.otb.bg>

 Test userinfo function.
"""

import os
import sys
import pprint
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, ".."))


from openshift import *

class TestUserInfo(unittest.TestCase):
    '''
        Test the OpenShiftExpress.get_user_info() method
    '''

    def test_missing_user(self):
        print "TEST: Getting info for missing user ..."
        oshift = OpenShiftExpress(rhlogin='nosuchlogin', password='123456')
        try:
            info = oshift.get_user_info()
        except OpenShiftLoginException as e:
            self.assertTrue(True)
            print e
            return

        self.assertTrue(False)

    def test_wrong_password(self):
        print "TEST: Getting info with wrong password ..."
        self.assertTrue(os.environ.has_key('OPENSHIFT_USER'), 'Provide OpenShift username!')
        oshift = OpenShiftExpress(rhlogin=os.environ['OPENSHIFT_USER'], password='123456')
        try:
            info = oshift.get_user_info()
        except OpenShiftLoginException as e:
            self.assertTrue(True)
            print e
            return

        self.assertTrue(False)

    def test_user_info(self):
        print "TEST: Getting info for user ..."
        self.assertTrue(os.environ.has_key('OPENSHIFT_USER'), 'Provide OpenShift username!')
        self.assertTrue(os.environ.has_key('OPENSHIFT_PASSWORD'), 'Provide OpenShift password!')
        oshift = OpenShiftExpress(rhlogin=os.environ['OPENSHIFT_USER'], password=os.environ['OPENSHIFT_PASSWORD'])
        info = oshift.get_user_info()
        pprint.pprint(info)

        self.assertTrue(info.has_key('user_info'))
        self.assertTrue(info.has_key('app_info'))


if __name__ == '__main__':
    unittest.main()
