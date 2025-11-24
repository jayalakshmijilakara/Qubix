import frappe
from datetime import date


@frappe.whitelist()
def get_customers_for_sales_person(doctype, txt, searchfield, start, page_len, filters):
    if isinstance(filters, str):
        filters = frappe.parse_json(filters) if filters else {}
    filters = filters or {}

    sales_person = filters.get("sales_person")
    if not sales_person:
        return []

    return frappe.db.sql(
        """
        SELECT DISTINCT
            c.name,
            c.customer_name
        FROM
            `tabCustomer` c
            INNER JOIN `tabSales Team` st
                ON st.parent = c.name
                AND st.sales_person = %(sales_person)s
        WHERE
            c.docstatus < 2
            AND (c.name LIKE %(txt)s
                 OR c.customer_name LIKE %(txt)s)
        ORDER BY c.name
        LIMIT %(start)s, %(page_len)s
        """,
        {
            "sales_person": sales_person,
            "txt": f"%{txt}%",
            "start": start,
            "page_len": page_len,
        },
    )



@frappe.whitelist()
def make_sales_order(custom_special_price_approval_ref):
    doc = frappe.get_doc('Special Price Approval',custom_special_price_approval_ref)
    if doc.sales_order_reference:
        return doc.sales_order_reference
    

    so = frappe.new_doc("Sales Order")
    so.customer = doc.customer
    so.territory = doc.territory
    so.custom_special_price_approval_ref = doc.name
    so.delivery_date = date.today()


    for item in doc.items :
        rate = item.approved_rate or item.requested_rate
        if not rate :
            frappe.throw(f"Rate is missing for item {item.item_code}")
        so.append("items", {
                "item_code": item.item_code,
                "qty": item.quantity,
                "rate": rate,
            })
        
    so.insert(ignore_permissions=True)
    doc.db_set("sales_order_reference",so.name,update_modified=False)
    return so.name
