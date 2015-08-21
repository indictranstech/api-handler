# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.sessions


def handle():
	"""handle request"""
	cmd = frappe.local.form_dict.cmd
	execute_cmd(cmd)

	return build_response("json")

def execute_cmd(cmd, async=False):
	"""execute a request as python module"""
	import api_handler

	method = get_attr(cmd)
	
	# check if whitelisted
	# if frappe.session['user'] == 'Guest':
	# 	if (method not in frappe.guest_methods):
	# 		frappe.msgprint(_("Not permitted"))
	# 		raise frappe.PermissionError('Not Allowed, {0}'.format(method))
	# else:
	# 	if not method in frappe.whitelisted:
	# 		frappe.msgprint(_("Not permitted"))
	# 		raise frappe.PermissionError('Not Allowed, {0}'.format(method))
	try:
		ret = frappe.call(method, **frappe.form_dict)
		ret["code"] = 200	
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass
	
	

def get_attr(cmd):
	"""get method object from cmd"""
	if '.' in cmd:
		method = frappe.get_attr(cmd)
	else:
		method = globals()[cmd]
	frappe.log("method:" + cmd)
	return method
