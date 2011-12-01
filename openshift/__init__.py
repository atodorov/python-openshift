# Copyright (c) 2011, Open Technologies Bulgaria, Ltd. <http://otb.bg>
# Author: Alexander Todorov <atodorov@nospam.otb.bg>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import pprint
import urllib
import httplib
import exceptions

class OpenShiftException(exceptions.BaseException):
    pass

class OpenShiftLoginException(OpenShiftException):
    pass

class OpenShiftExpress:
    """Represent the OpenShift Express API."""

    API = "1.1.1"
    connection_timeout = 10
    debug = False

    def __init__(self, rhlogin, password, server='openshift.redhat.com'):
        self.server = server
        self.rhlogin = rhlogin
        self.password = password
        self.last_response = None

    def _generate_json(self, data, skip_login=False):
        """Helper function to encode the json data. DO NOT use directly."""
        data['api'] = self.API
        data['debug'] = self.debug

        if not skip_login:
            data['rhlogin'] = self.rhlogin

        return json.dumps(data)

    def _http_post(self, path, json_data, skip_password=False):
        """
            Helper function to POST the data to the requester path and return the response object.
            DO NOT use directly.
        """
        if skip_password:
            params = urllib.urlencode({'json_data' : json_data})
        else:
            params = urllib.urlencode({'json_data' : json_data, 'password' : self.password})

        # print all params before sending over https
        if self.debug:
            print 'Submitting params:'
            print params

        conn = httplib.HTTPSConnection(self.server, timeout=self.connection_mytimeout)
        conn.request('POST', path, params)
        response = conn.getresponse()

        # store the last server response for error reporting
        self.last_response['status'] = response.status
        self.last_response['content_type'] = response.content_type
        self.last_response['body'] = response.read()

        if (response.status == 404) and (response.getheader('Content-type') == 'text/html'):
            raise OpenShiftException("RHCloud server not found.")

        # request probably successed. print the reponse
        if self.debug:
            json_resp = json.loads(self.last_response['body'])
            print "Response from server:"
            pprint.pprint(json_resp)

        return response


    def get_user_info(self):
        """
            Get information about the user and currently deployed applications.

            @return  - dict structure with user and applications info or exception

            http://docs.redhat.com/docs/en-US/OpenShift_Express/1.0/html/API_Guide/sect-API_Guide-API_Commands-User_and_Application_Information.html
        """
        json_data = self._generate_json({})

        response = self._http_post('/broker/userinfo', json_data)

        if response.status != 200:
            if response.status == 404:
                raise OpenShiftException("The user with login '%s' does not have a registered domain." % self.rhlogin)
            elif response.status == 401:
                raise OpenShiftLoginException("Invalid user credentials")
            else:
                raise OpenShiftException(self.response_error())

        json_resp = json.loads(response.read())
        user_info = json.loads(json_resp['data'])
        return user_info

    def get_cartridges_list(self, cart_type="standalone"):
        """
            Get a list of available cartridges.

            @cart_type - 'standalone' or 'embedded'

            @return - list of cartridge names or exception

            http://docs.redhat.com/docs/en-US/OpenShift_Express/1.0/html/API_Guide/sect-API_Guide-API_Commands-Cartridge_List.html
        """

        data = {'cart_type' : cart_type}
        json_data = self._generate_json(data, skip_login=True)

        response = self._http_post('/broker/cartlist', json_data, skip_password=True)

        if response.status != 200:
            raise OpenShiftException(self.response_error())
        else:
            json_resp = json.loads(response.read())
            return json.loads(json_resp['data'])['carts']

    def control_application(self, app_name, action, cartridge=None, embedded=False, server_alias=None):
        """
            Control the application, create, destroy, start, stop, add embedded cartridge, etc.

            @app_name - string - the name of the application
            @action - string - what to do. see rhc-ctl-app for a list of allowed actions
            @cartridge - string - if the action is related to a specific framework (like add/remove) specify which one
            @embedded - bool - is the action related to an embedded cartridge
            @server_alias - string - specify if adding/removing a CNAME

            @return - the result structure returned by the server or exception

            todo: force-stop and reload are not documented. what is the difference with stop/restart?

            http://docs.redhat.com/docs/en-US/OpenShift_Express/1.0/html/API_Guide/sect-API_Guide-API_Commands-Application_Control_Commands.html
            http://docs.redhat.com/docs/en-US/OpenShift_Express/1.0/html/API_Guide/sect-API_Guide-API_Commands-Embedded_Cartridges.html
        """

        allowed_actions = ['configure', 'deconfigure', 'start', 'stop', 'restart', 'reload', 'status']
        if not embedded:
            allowed_actions += ['force-stop', 'add-alias', 'remove-alias']


        # create|destroy are used from rhc for clarity
        if action in ['create', 'add']:
            action = 'configure'

        # add|remove are used for embedded cartridges
        if action in ['destroy', 'remove']:
            action = 'deconfigure'


        if action not in allowed_actions:
            raise OpenShiftException("%s not in %s" % (action, '|'.join(allowed_actions)))


        data = {'action' : action, 'app_name' : app_name}

        if cartridge:
            data['cartridge'] = cartridge


        if server_alias:
            data['server_alias'] = server_alias

        json_data = self._generate_json(data)

        if embedded:
            response = self._http_post('/broker/embed_cartridge', json_data)
        else:
            response = self._http_post('/broker/cartridge', json_data)

        json_resp = None
        if response.status == 200:
            json_resp = json.loads(response.read())
        else:
            raise OpenShiftException(self.response_error())

        return json_resp['result']

    def create_domain(self, namespace, ssh_key=None, alter=False):
        """
            Create new domain (aka namespace) in the cloud.

            @namespace - string - the name of the domain
            @ssh_key - string - the key portion of an rsa key excluding ssh-rsa and comment
            @alter - bool - an optional flag to alter namespace and/or ssh key after creation

            @return - dict - the data structure returned from the server or exception

            http://docs.redhat.com/docs/en-US/OpenShift_Express/1.0/html/API_Guide/sect-API_Guide-API_Commands-Domain_Creation_Commands.html
        """
        if (not alter) and (ssh_key is None):
            raise OpenShiftException("Specify SSH key when creating a domain")

        data = {'namespace' : namespace, 'alter' : alter}
        if ssh_key is not None:
            data['ssh'] = ssh_key

        json_data = self._generate_json(data)

        response = self._http_post('/broker/domain', json_data)

        if response.status != 200:
            raise OpenShiftException(self.response_error())
        else:
            json_resp = json.loads(response.read())
            return json.loads(json_resp['data'])


    def response_error(self):
        """
            Call this in case of exception or unexpected results.
            The last response values are stored in self.last_response

            @return - string or exception
        """
        if self.last_response['content_type'] == 'application/json':
            json_resp = json.loads(self.last_response['body'])
            return json_resp['messages']
        else:
            raise OpenShiftException('Response type was not application/json. Please run in debug mode!')
