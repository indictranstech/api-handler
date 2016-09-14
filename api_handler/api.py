# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import json
import frappe
from frappe import _
import handler
from response import build_response,report_error
from .api_handler.doctype.api_log.api_log import log_request, log_response

def handle():
	"""
	Handler for `/api_name` methods
	**api_name = configured in api_hander hooks 
	### Examples:

	`/api_name/version/{methodname}` will call a whitelisted method
	
	"""
	parts = frappe.request.path[1:].split("/",4)
	method_name = version = api_name = method = response = None
	req_method = frappe.local.request.method

	# log_id = log_request(frappe.local.request, frappe.local.form_dict)

	if len(parts) <= 2:
		# if parts[1] == 'login':
		frappe.local.form_dict.cmd = '.'.join(map(str,[parts[0],parts[1]]))
		frappe.local.form_dict.op = parts[1]
		response = handler.handle()

	else:
		api_name = parts[0]
		version = parts[2].replace(".", "_")
		# frappe.local.form_dict.req_log_id = log_id
		if parts[3] == "method":
			method_name = parts[4]
			method = '.'.join(map(str,[api_name,"api.versions",version,method_name]))
			frappe.local.form_dict.cmd = method
			response = handler.handle()
		elif parts[3] == "resource":
			resource = dict(zip(["doctype", "docname"], parts[4].split("/")[:]))
			method = '.'.join(map(str,[api_name,"api.resources.handle"]))

			frappe.local.form_dict.cmd = method
			frappe.local.form_dict.version = version
			frappe.local.form_dict.resource = resource
			frappe.local.form_dict.req_method = req_method

			response = handler.handle()
		else:
			response = report_error(417,"Invalid URL")

	# # log response
	# data = json.loads(response.data)
	# data.update({ "log_id":log_id })
	# response.data = json.dumps(data)
	# log_response(log_id, response.data)
	
	return response