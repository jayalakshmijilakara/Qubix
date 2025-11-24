# Copyright (c) 2025, jaya and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"label": "State", "fieldname": "state", "fieldtype": "Link", "options": "Territory", "width": 120},
        {"label": "Financial Year", "fieldname": "financial_year", "fieldtype": "Link", "options": "Fiscal Year", "width": 120},
        {"label": "ASM Name", "fieldname": "asm_name", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": "Period", "fieldname": "period", "fieldtype": "Data", "width": 100},
        {"label": "Total Budget", "fieldname": "total_budget", "fieldtype": "Currency", "width": 120},
        {"label": "Approved Amount", "fieldname": "approved_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Utilized Amount", "fieldname": "utilized_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Utilization %", "fieldname": "utilization_percent", "fieldtype": "Percent", "width": 120},
    ]

def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("state"):
        conditions.append("bu.state = %(state)s")
        values["state"] = filters["state"]

    if filters.get("financial_year"):
        conditions.append("bu.financial_year = %(financial_year)s")
        values["financial_year"] = filters["financial_year"]

    if filters.get("period"):
        conditions.append("bu.period = %(period)s")
        values["period"] = filters["period"]

    if filters.get("asm_name"):
        conditions.append("bu.asm_name = %(asm_name)s")
        values["asm_name"] = filters["asm_name"]

    condition_str = " AND ".join(conditions) if conditions else "1=1"
    return condition_str, values

def get_data(filters):
    conditions, values = get_conditions(filters)

    query = f"""
        SELECT
            bu.state,
            bu.financial_year,
            bu.asm_name,
            bu.period,
            SUM(IFNULL(ba.total_budget, 0)) AS total_budget,
            SUM(IFNULL(bu.approved_amount, 0)) AS approved_amount,
            SUM(IFNULL(bu.utilized_amount, 0)) AS utilized_amount,
            CASE
                WHEN SUM(IFNULL(ba.total_budget, 0)) = 0 THEN 0
                ELSE (SUM(IFNULL(bu.utilized_amount, 0)) / SUM(IFNULL(ba.total_budget, 0))) * 100
            END AS utilization_percent
        FROM `tabBudget Utilization` bu
        LEFT JOIN `tabBudget Allocation` ba
            ON ba.state = bu.state
           AND ba.financial_year = bu.financial_year
           AND ba.asm_name = bu.asm_name
           AND ba.period = bu.period
        WHERE {conditions}
        GROUP BY
            bu.state, bu.financial_year, bu.asm_name, bu.period
        ORDER BY
            bu.state, bu.financial_year, bu.asm_name, bu.period
    """

    return frappe.db.sql(query, values, as_dict=True)
