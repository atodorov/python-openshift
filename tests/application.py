"""
 Copyright (c) 2011, Open Technologies Bulgaria, Ltd. <http://otb.bg>
 Author: Alexander Todorov <atodorov@nospam.otb.bg>

 Tests for application control functionality.
"""

import os
import sys
import pprint
import unittest

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, ".."))


from openshift import *

class TestApplicationControl(unittest.TestCase):
    """
        Test OpenShiftExpress application control methods
    """

    def test_control_application(self):
        """
            All testing goes in one method with multiple asserts.
        """
        self.app_name = 'python0penshift7est'

        self.assertTrue(os.environ.has_key('OPENSHIFT_USER'), 'Provide OpenShift username!')
        self.assertTrue(os.environ.has_key('OPENSHIFT_PASSWORD'), 'Provide OpenShift password!')
        oshift = OpenShiftExpress(rhlogin=os.environ['OPENSHIFT_USER'], password=os.environ['OPENSHIFT_PASSWORD'])

        # test what happens with dummy actions
        try:
            print "TEST: Testing dummy actions ..."
            oshift.control_application(app_name='dummy', action='dummy')
        except OpenShiftException as e:
            print e

        # test what happens with dummy actions for embedded cartridge
        try:
            print "TEST: Testing dummy actions ..."
            oshift.control_application(app_name='dummy', action='dummy', embedded=True)
        except OpenShiftException as e:
            print e

        # test create application but no cartridge
        result = None
        try:
            print "TEST: Create without cartridge type ..."
            result = oshift.control_application(app_name=self.app_name, action='create')
        except OpenShiftException as e:
            print e
            self.assertTrue(result is None)

        # create test application
        print "TEST: Creating ..."
        result = oshift.control_application(app_name=self.app_name, action='create', cartridge='wsgi-3.2')
        print result
        self.assertTrue(result.startswith('Successfully created application'))
        info = oshift.get_user_info()
        pprint.pprint(info)
        self.assertTrue(info['app_info'].has_key(self.app_name))


        # stop the application
        print "TEST: Stopping ..."
        oshift.control_application(app_name=self.app_name, action='stop')
        status = oshift.control_application(app_name=self.app_name, action='status')
        print(status)
        self.assertTrue(status.find('stopped') > -1)

        # start the application
        print "TEST: Starting ..."
        oshift.control_application(app_name=self.app_name, action='start')
        status = oshift.control_application(app_name=self.app_name, action='status')
        print status
        self.assertTrue(status.startswith('Total Accesses'))

        # restart the application
        print "TEST: Restarting ..."
        oshift.control_application(app_name=self.app_name, action='restart')
        status = oshift.control_application(app_name=self.app_name, action='status')
        print status
        self.assertTrue(status.startswith('Total Accesses'))

        # force-stop the application
        print "TEST: Force-stopping ..."
        oshift.control_application(app_name=self.app_name, action='force-stop')
        status = oshift.control_application(app_name=self.app_name, action='status')
        print(status)
        self.assertTrue(status.find('stopped') > -1)

        # reload the application
# todo: after reload status gives: Application 'python0penshift7est' is either stopped or inaccessible
#        print "TEST: Reloading ..."
#        oshift.control_application(app_name=self.app_name, action='reload')
#        status = oshift.control_application(app_name=self.app_name, action='status')
#        print status
#        self.assertTrue(status.startswith('Total Accesses'))

        # add CNAME
        print "TEST: Adding CNAME alias ..."
        alias = '%s.example.com' % self.app_name
        oshift.control_application(app_name=self.app_name, action='add-alias', server_alias=alias)
        info = oshift.get_user_info()
        pprint.pprint(info)
        self.assertTrue(alias in info['app_info'][self.app_name]['aliases'])

        # remove CNAME
        print "TEST: Removing CNAME alias ..."
        alias = '%s.example.com' % self.app_name
        oshift.control_application(app_name=self.app_name, action='remove-alias', server_alias=alias)
        info = oshift.get_user_info()
        pprint.pprint(info)
        aliases = info['app_info'][self.app_name]['aliases']
        self.assertTrue((aliases is None) or (len(aliases) == 0))

        # add embedded cartridge for this app
        try:
            print "TEST: Add embedded with no cartridge specified ..."
            oshift.control_application(app_name=self.app_name, action='add', embedded=True)
        except OpenShiftException as e:
            print e

        print "TEST: Adding embedded ..."
        embed_type='mysql-5.1'
        oshift.control_application(app_name=self.app_name, action='add', cartridge=embed_type, embedded=True)
        info = oshift.get_user_info()
        pprint.pprint(info)
        self.assertTrue(embed_type in info['app_info'][self.app_name]['embedded'])


        # stop the embedded cartridge
        print "TEST: Stopping embedded..."
        oshift.control_application(app_name=self.app_name, action='stop', cartridge=embed_type, embedded=True)
        status = oshift.control_application(app_name=self.app_name, action='status', cartridge=embed_type, embedded=True)
        print(status)
        self.assertTrue(status.find('stopped') > -1)

        # start the embedded cartridge
        print "TEST: Starting embedded ..."
        oshift.control_application(app_name=self.app_name, action='start', cartridge=embed_type, embedded=True)
        status = oshift.control_application(app_name=self.app_name, action='status', cartridge=embed_type, embedded=True)
        print status
        self.assertTrue(status.find('running') > -1)

        # restart the embedded cartridge
        print "TEST: Restarting embedded ..."
        oshift.control_application(app_name=self.app_name, action='restart', cartridge=embed_type, embedded=True)
        status = oshift.control_application(app_name=self.app_name, action='status', cartridge=embed_type, embedded=True)
        print status
        self.assertTrue(status.find('running') > -1)

        # reload the embedded cartridge
#todo: after reload we get RESULT: Mysql is stopped
#        print "TEST: Reloading embedded ..."
#        oshift.control_application(app_name=self.app_name, action='reload', cartridge=embed_type, embedded=True)
#        status = oshift.control_application(app_name=self.app_name, action='status', cartridge=embed_type, embedded=True)
#        print status
#        self.assertTrue(status.startswith('Total Accesses'))

        print "TEST: Removing embedded ..."
        oshift.control_application(app_name=self.app_name, action='remove', cartridge=embed_type, embedded=True)
        info = oshift.get_user_info()
        pprint.pprint(info)
        embedded = info['app_info'][self.app_name]['embedded']
        self.assertTrue((embedded is None) or (len(embedded) == 0))

        # destroy the test application
        print "TEST: Destroying ..."
        result = oshift.control_application(app_name=self.app_name, action='destroy')
        print result
        self.assertTrue(result.startswith('Successfully destroyed application'))
        info = oshift.get_user_info()
        pprint.pprint(info)
        self.assertFalse(info['app_info'].has_key(self.app_name))


if __name__ == '__main__':
    unittest.main()
