
frappe.ui.form.on("Special Price Approval", {
    before_workflow_action: async (frm) => {
        const user = frappe.session.user;
        const action = frm.selected_workflow_action;

        if (action === "Submit" && !frm.doc.asm_approved_by) {
            const ok = await new Promise((resolve, reject) => {
                frappe.msgprint({
                    title: "ASM Approval",
                    message: "Proceed with ASM approval?",
                    primary_action: {
                        label: "Proceed",
                        action() { cur_dialog.hide(); resolve(true); }
                    },
                    secondary_action: {
                        label: "Cancel",
                        action() { cur_dialog.hide(); reject(); }
                    }
                });
            }).catch(() => frappe.throw("Approval cancelled."));

            await frm.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: frm.doctype,
                    name: frm.doc.name,
                    fieldname: "asm_approved_by",
                    value: user
                }
            });
        }
    },

    after_workflow_action: async (frm) => {
        const user = frappe.session.user;

        if (frm.doc.workflow_state === "RSM Approved" && !frm.doc.rsm_approved_by) {
            await frm.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: frm.doctype,
                    name: frm.doc.name,
                    fieldname: "rsm_approved_by",
                    value: user
                }
            });
        }

        if (frm.doc.workflow_state === "HO Approved" && !frm.doc.ho_approved_by) {
            await frm.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: frm.doctype,
                    name: frm.doc.name,
                    fieldname: "ho_approved_by",
                    value: user
                }
            });
        }

        frm.reload_doc();
    }
});

frappe.ui.form.on("Special Price Approval", {
    refresh(frm) {
        frm.set_query("sales_person", function() {
            return {
                filters: {
                    enabled: 1
                }
            };
        });



      if (frm.doc.status === "HO Approved" && !frm.is_new()) {
            frm.add_custom_button(__("Print Approval"), function () {
                const doctype = frm.doc.doctype;
                const docname = frm.doc.name;
                const print_format = "Special Price Approval Format"; 
                const no_letterhead = 0;

                const url = `/api/method/frappe.utils.print_format.download_pdf`
                    + `?doctype=${encodeURIComponent(doctype)}`
                    + `&name=${encodeURIComponent(docname)}`
                    + `&format=${encodeURIComponent(print_format)}`
                    + `&no_letterhead=${no_letterhead}`;

                window.open(url);
            }, __("Actions"));
        }
    },

    sales_person(frm) {
        if (frm.doc.sales_person) {
            frm.set_query("customer", function() {
                return {
                    query: "qubix.api.get_customers_for_sales_person",
                    filters: {
                        sales_person: frm.doc.sales_person
                    }
                };
            });
        }
    }
});



frappe.ui.form.on("Special Price Approval", {
     refresh(frm) {
         if (frm.doc.status === 'HO Approved' && !frm.doc.sales_order_reference) {
             frm.add_custom_button(__("Make Sales Order"), function () {
                frappe.call({
                    method:"qubix.api.make_sales_order",
                    args:{
                        custom_special_price_approval_ref : frm.doc.name,

                    },
                    callback: function(r){
                        if(!r.exc && r.message){
                            frappe.set_route("Form","Sales Order",r.message);
                        }
                    }
                
                })
            

             })

         }
     }
})