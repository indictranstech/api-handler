# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.sessions
from response import build_response,report_error
import api_handler


def handle():
	"""handle request"""
	cmd = frappe.local.form_dict.cmd
	op = frappe.local.form_dict.op

	if op == 'login':
		login_user()
	elif cmd != 'login':
		manage_user()
		execute_cmd(cmd)	

	return build_response("json")

def execute_cmd(cmd, async=False):
	"""execute a request as python module"""

	method = get_attr(cmd)
	
	try:
		#check if whitelisted
		if frappe.session['user'] == 'Guest':
			if (method not in frappe.guest_methods):
				return report_error(403,"Not Allowed")		
		else:
			if not method in frappe.whitelisted:
				return report_error(403,"Not Allowed")

		
		ret = frappe.call(method, **frappe.form_dict)
		ret["code"] = 200
		if ret:
			for key in ret:
				frappe.response[key] = ret[key] 	
	
	except Exception, e:
		http_status_code = getattr(e, "status_code", 500)
		message = getattr(e, "message", 500)
		report_error(http_status_code,message)

	else:
		pass
	
	finally:
		import time
		ts = int(time.time())
		frappe.response["timestamp"] = ts
	
	

def get_attr(cmd):
	"""get method object from cmd"""
	if '.' in cmd:
		method = frappe.get_attr(cmd)
	else:
		method = globals()[cmd]
	frappe.log("method:" + cmd)
	return method


def login_user():
	cmd = frappe.local.form_dict.cmd
	method = get_attr(cmd)
	ret = frappe.call(method, **frappe.form_dict)
	return ret

def manage_user():
	#pass
	print frappe.form_dict.data
	#add condition of user id 
	#check given user id correct or not if not return from here 
	#if user is valid set it to session resume