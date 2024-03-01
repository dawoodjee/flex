import frappe
from frappe import _

def create_custom_field(field_name, doctype):
	update = False
	custom_fields = frappe.get_all("Custom Field", filters={"dt": doctype}, fields=["fieldname"], pluck="fieldname")

	try:
		if field_name.lower() in custom_fields:
			return		
		
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": doctype,
			"fieldname": field_name.lower(),
			"fieldtype": "Data",
			"label": field_name,
			"insert_after": 'username',
			"allow_on_submit": 1,
			"no_copy": 1,
			"hidden": 0
		}).insert()
		update = True
		if update:
			frappe.msgprint(_("{0} custom field has been added to {1}").format(frappe.bold(field_name), doctype))
	except Exception as e:
		count = 0
		while count < 1:
			# try again
			create_custom_field(field_name, doctype)
			count += 1 

		if count >= 1:
			frappe.msgprint(
				msg=_("Unable to create custom field(s). ") + e.message, 
				title=_('Failed to create custom field(s)'),
				raise_exception=1
			)
			count += 1