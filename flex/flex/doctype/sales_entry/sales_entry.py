# Copyright (c) 2024, Bantoo and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class SalesEntry(Document):
	def validate(self):
		# if not self.sales_person:
		shop_settings = frappe.get_doc("Shop Settings", "Shop Settings")
		self.sales_person = frappe.session.user
		self.shop = self.get_sales_persons_shop(shop_settings, self.sales_person)
		
	def get_sales_persons_shop(self, shop_settings, sales_person):

		if self.shop and shop_settings.allow_supervisors_to_switch_shops == 1:
			return self.shop
		for shop in shop_settings.staff_allocation:
			if shop.sales_person and shop.shop:
				if shop.sales_person == sales_person:
					return shop.shop
				
		frappe.throw(_("Sales Person {0} is not assigned to any shop. You can ask the Sales Manager to assign you a shop {1}").format(frappe.bold(sales_person), frappe.bold("Shop Settings")))
					
	@frappe.whitelist()
	def update_fields(self):		
		self.update_line_amount()
		# self.update_sales_total()

	def update_line_amount(self):
		total = 0
		total_qty = 0
		for sales_line in self.sales_entries:
			if not sales_line.price or not sales_line.qty:
				continue
			sales_line.amount = sales_line.price * sales_line.qty
			total_qty = total_qty + sales_line.qty
			total = total + sales_line.amount
		self.total = total
		self.total_qty = total_qty
