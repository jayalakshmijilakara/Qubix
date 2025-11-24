// Copyright (c) 2025, jaya and contributors
// For license information, please see license.txt

frappe.query_reports["Budget Utilization (Script Report)"] = {
    "filters": [
        {
            "fieldname": "state",
            "label": __("State"),
            "fieldtype": "Link",
            "options": "Territory",    
            "reqd": 0
        },
        {
            "fieldname": "financial_year",
            "label": __("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",   
            "reqd": 0
        },
        {
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": [
                "Q1 (Apr–Jun)",
                "Q2 (Jul–Sep)",
                "Q3 (Oct–Dec)",
                "Q4 (Jan–Mar)"
            ].join("\n"),
            "reqd": 0
        },
        {
            "fieldname": "asm_name",
            "label": __("ASM Name"),
            "fieldtype": "Link",
            "options": "User",    
            "reqd": 0
        }
    ]
};
