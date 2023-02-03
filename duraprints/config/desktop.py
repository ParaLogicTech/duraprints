# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _

def get_data():
	return [
		# Modules
		{
			"module_name": "Duraprints",
			"category": "Modules",
			"label": _("Duraprints"),
			"color": "#3498db",
			"icon": "octicon octicon-repo",
			"type": "module",
			"description": "Complex & Compound Production tool.",
			"onboard_present": 1
		}
	]
