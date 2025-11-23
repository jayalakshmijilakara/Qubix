import frappe


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
