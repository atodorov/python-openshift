# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>
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

import os
import re
import sys
import json
import socket
import urllib
import httplib
import exceptions

class OpenShiftUnknownException(exceptions.BaseException):
    pass

class OpenShiftNotFoundException(exceptions.BaseException):
    pass

class OpenShiftMissingDomainException(exceptions.BaseException):
    pass

class OpenShiftLoginFailedException(exceptions.BaseException):
    pass

class OpenShift:
    DEFAULT_MAX_LENGTH = 16
    APP_NAME_MAX_LENGTH = 32
    MAX_RETRIES = 7
    DEFAULT_DELAY = 2
    API = "1.1.1"
    mytimeout = 10
    mydebug = False
    broker_version = "?.?.?"
    api_version = "?.?.?"
  
    DEBUG_INGORE_KEYS = {
	'result' : None,
	'debug' : None,
	'exit_code' : None,
	'messages' : None,
	'data' : None,
	'api' : None,
	'broker' : None
    }

    def __init__(self, rhlogin, password, server='openshift.redhat.com'):
#	self.delay_time = self.DEFAULT_DELAY
	self.server = server
	self.rhlogin = rhlogin
	self.password = password

    def generate_json(self, data):
	data['api'] = self.API
	return json.dumps(data)

    def http_post(self, path, json_data, skip_password=False):
	'''
	    POST the data to the requester path and return the response object
	'''
	if skip_password:
	    params = urllib.urlencode({'json_data' : json_data})
	else:
	    params = urllib.urlencode({'json_data' : json_data, 'password' : self.password})

	conn = httplib.HTTPSConnection(self.server, timeout=self.mytimeout)
	conn.request('POST', path, params)
	response = conn.getresponse()

	if (response.status == 404) and (response.content_type == 'text/html'):
	    raise OpenShiftNotFoundException("RHCloud server not found.")

	return response


    def get_user_info(self):
	'''
	    Return information about the user.
	    http://docs.redhat.com/docs/en-US/OpenShift_Express/1.0/html/API_Guide/sect-API_Guide-API_Commands-User_and_Application_Information.html
	'''
	data = {'rhlogin' : self.rhlogin}
	data['debug'] = self.mydebug

	self.print_post_data(data)
	json_data = self.generate_json(data)

	response = self.http_post('/broker/userinfo', json_data)

	if response.status != 200:
	    if response.status == 404:
		raise OpenShiftMissingDomainException("The user with login '%s' does not have a registered domain." % self.rhlogin)
	    elif response.status == 401:
		raise OpenShiftLoginFailedException("Invalid user credentials")
	    else:
#todo: fix this
		self.print_response_err(response)
		raise OpenShiftUnknownException

	json_resp = json.loads(response.read())
	self.print_response_success(json_resp)

	user_info = json.loads(json_resp['data'])
	return user_info

    def get_cartridges_list(self, cart_type="standalone"):
	""" Get a list of available cartridges """

	data = {'cart_type' : cart_type}
	data['debug'] = self.mydebug

	self.print_post_data(data)
	json_data = self.generate_json(data)

	response = self.http_post('/broker/cartlist', json_data, skip_password=True)

	if response.status != 200:
	    self.print_response_err(response)
	    return []
	else:
	    json_resp = json.loads(response.read())
	    self.print_response_success(json_resp)

	    carts = json.loads(json_resp['data'])['carts']
	    return carts


    def timeout(self, value):
	if value and (value > 0):
	    self.mytimeout = value
	else:
	    print 'Timeout must be specified as a number greater than 0'
	    sys.exit(1)

    def debug(self, value):
	self.mydebug = value

    def delay(self, time, adj=DEFAULT_DELAY):
	self.delay_time *= adj



    # Invalid chars (") ($) (^) (<) (>) (|) (%) (/) (;) (:) (,) (\) (*) (=) (~)
    def check_rhlogin(self, rhlogin):
#todo: fix regular expression
	if rhlogin:
	    if re.match('/["\$\^<>\|%\/;:,\\\*=~]/', rhlogin):
		print 'RHLogin may not contain any of these characters: (\") ($) (^) (<) (>) (|) (%) (/) (;) (:) (,) (\) (*) (=) (~)'
		return False
	else:
	    print "RHLogin is required"
	    return False

	return True

    def check_app(self, app):
	self.check_field(app, 'application', APP_NAME_MAX_LENGTH)

    def check_namespace(self, namespace):
	self.check_field(namespace, 'namespace', DEFAULT_MAX_LENGTH)

    def check_field(self, field, type, max=0):
	if field:
#todo: fix regexp
	    if re.match("/[^0-9a-zA-Z]/", field):
		print "%s contains non-alphanumeric characters!" % field
		return False
	    if (max != 0) and (field.length > max):
		print "maximum %s size is %d characters" % (type, max)
		return False
	else:
	    print "%s is required" % field
	    return False

	return True

    def print_post_data(self, h):
	if self.mydebug:
	    print 'Submitting form:'
	    print h


    def print_response_err(self, response):
	print "Problem reported from server. Response code was %d." % response.status
	exit_code = 1

	if response.content_type == 'application/json':
	    print "JSON response:"
	    json_resp = json.loads(response.read())
	    exit_code = self.print_json_body(json_resp)
	elif self.mydebug:
	    print "HTTP response from server is %s" % response.read()
	    end
	sys.exit(exit_code)

    def print_response_messages(self, json_resp):
	messages = json_resp['messages']
	if messages:
	    print ''
	    print 'MESSAGES:'
	    print messages
	    print ''

    def print_response_success(self, json_resp, print_result=False):
	if self.mydebug:
	    print "Response from server:"
	    self.print_json_body(json_resp, print_result)
	elif print_result:
	    self.print_json_body(json_resp)
	else:
	    self.print_response_messages(json_resp)

    def print_json_body(self, json_resp, print_result=True):
	self.print_response_messages(json_resp)
	exit_code = json_resp['exit_code']
	if self.mydebug:
	    if json_resp['debug']:
		print ''
		print 'DEBUG:'
		print json_resp['debug']
		print ''
		print "Exit Code: ", exit_code

		if (json_resp.length > 3):
		    print json_resp

	if json_resp['api']:
	    print "API version:", json_resp['api']

	if json_resp['broker']:
	    print "Broker version:", json_resp['broker']

	if print_result and json_resp['result']:
	    print ''
	    print 'RESULT:'
	    print json_resp['result']
	    print ''

	return exit_code

    def hostexist(self, host):
	"""Check if host exists"""
	resp = socket.gethostbyname(host) # todo: handle ipv6 too
	return resp is not None

