# Copyright (c) 2025, jaya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SpecialPriceApproval(Document):

    def on_update_after_submit(self):
        self.create_sales_order_from_special_price_approval()

    def create_sales_order_from_special_price_approval(self):
        if self.status != "HO Approved":
            return

        if self.sales_order_reference:
            return

        so = frappe.new_doc("Sales Order")
        so.customer = self.customer
        so.territory = self.territory
        so.special_price_approval_ref = self.name

        for item in self.items:
            rate = item.approved_rate or item.requested_rate
            if not rate:
                frappe.throw(f"Rate is missing for item {item.item_code}")

            so.append("items", {
                "item_code": item.item_code,
                "qty": item.quantity,
                "rate": rate,
            })

        so.insert(ignore_permissions=True)
        so.submit()

        self.db_set("sales_order_reference", so.name, update_modified=False)
