import frappe


def after_install():
    create_special_roles()
    create_default_users()
    setup_special_price_approval_permissions()

def create_special_roles():
    roles = ["ASM", "RSM", "HO"]

    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert(ignore_permissions=True)
            frappe.logger().info(f"Created Role: {role}")


def create_default_users():
    default_users = [
        {
            "email": "asm@demo.com",
            "full_name": "Demo ASM",
            "role": "ASM"
        },
        {
            "email": "rsm@demo.com",
            "full_name": "Demo RSM",
            "role": "RSM"
        },
        {
            "email": "ho@demo.com",
            "full_name": "Demo HO",
            "role": "HO"
        },
    ]

    for user in default_users:
        if not frappe.db.exists("User", user["email"]):
            new_user = frappe.get_doc({
                "doctype": "User",
                "email": user["email"],
                "first_name": user["full_name"],
                "enabled": 1,
                "send_welcome_email": 0,  
                "new_password": "Test@123" 
            })
            new_user.insert(ignore_permissions=True)

            # Assign Role
            new_user.append("roles", {"role": user["role"]})
            new_user.save(ignore_permissions=True)

            frappe.logger().info(f"Created User: {user['email']} with role {user['role']}")



def setup_special_price_approval_permissions():
    doctype = "Special Price Approval"

    if not frappe.db.exists("DocType", doctype):
        frappe.logger().warning(f"{doctype} not found. Skipping permission setup.")
        return

    frappe.db.delete("DocPerm", {"parent": doctype})

    def add_perm(role, read=0, write=0, create=0, submit=0, cancel=0):
        frappe.get_doc({
            "doctype": "DocPerm",
            "parent": doctype,
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": role,
            "permlevel": 0,
            "read": read,
            "write": write,
            "create": create,
            "submit": submit,
            "cancel": cancel,
        }).insert(ignore_permissions=True)

    add_perm("ASM", read=1, write=1, create=1, submit=1)

    add_perm("RSM", read=1, write=1, submit=1)

    add_perm("HO", read=1, write=1, submit=1, cancel=1)

    frappe.clear_cache(doctype=doctype)
    frappe.logger().info("Permissions set for Special Price Approval.")
