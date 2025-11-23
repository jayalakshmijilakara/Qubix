import frappe


def after_install():
    create_roles()
    create_users()
    set_permissions()

def create_roles():
    roles = ["ASM", "RSM", "HO"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert(ignore_permissions=True)


def create_users():
    users = [
        ("asm@demo.com", "Demo ASM", "ASM"),
        ("rsm@demo.com", "Demo RSM", "RSM"),
        ("ho@demo.com",  "Demo HO",  "HO"),
    ]

    for email, name, role in users:
        if not frappe.db.exists("User", email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": name,
                "enabled": 1,
                "new_password": "Test@123",
                "send_welcome_email": 0
            })
            user.insert(ignore_permissions=True)
            user.append("roles", {"role": role})
            user.save(ignore_permissions=True)


def set_permissions():
    roles = ["ASM", "RSM", "HO"]

    doctypes = [
        "Customer",
        "Item",
        "Sales Person",
        "Territory",
        "Special Price Approval Item",
        "Special Price Approval"
    ]

    for dt in doctypes:
        if not frappe.db.exists("DocType", dt):
            continue

        frappe.db.delete("DocPerm", {
            "parent": dt,
            "role": ["in", roles]
        })

        for role in roles:
            perm = frappe.get_doc({
                "doctype": "DocPerm",
                "parent": dt,
                "parenttype": "DocType",
                "parentfield": "permissions",
                "role": role,
                "permlevel": 0,
                "read": 1,
                "write": 1,
                "create": 1,
                "submit": 1 if dt == "Special Price Approval" else 0,
                "cancel": 1 if role == "HO" and dt == "Special Price Approval" else 0,
            })
            perm.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.clear_cache()
