# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import json
import frappe
from frappe import _
import handler

def handle():
	"""
	Handler for `/api_name` methods
	**api_name = configured in api_hander hooks 
	### Examples:

	`/api_name/version/{methodname}` will call a whitelisted method
	
	"""
	parts = frappe.request.path[1:].split("/",3)
	method_name = version = api_name = method = None

	if len(parts) <= 2:
		if parts[1] == 'login':
			frappe.local.form_dict.cmd = '.'.join(map(str,[parts[0],parts[1]]))
			frappe.local.form_dict.op = "login"
			return handler.handle()

	elif len(parts) == 3:
		api_name = parts[0]
		version = parts[1]
		method_name = parts[2]
		method = '.'.join(map(str,[api_name,"versions",version,method_name]))
		frappe.local.form_dict.cmd = method
		return handler.handle()

	else:
		#invalid url
		pass	

	#return build_response("json")


