frappe.ui.form.on("Address","check_details", function(frm) {
            console.log(frm.selected_doc.gstin)
            frappe.call({
                method: "gst_india.cleartax_integration.API.gst.gstin_info",
                args: {
                    gstin: frm.selected_doc.gstin
                },
                callback: function (r) {
                    let line1 = ""
                    if(r.message.floorNumber){
                        line1 = line1 + r.message.floorNumber
                    }
                    if(r.message.buildingNumber){
                        line1 = line1 + ","+ r.message.buildingNumber 
                    }
                    if(r.message.buildingName){
                        line1 = line1 + ","+ r.message.buildingName
                    }
                    frm.set_value('address_line1',line1);
                    frm.set_value('address_line2',r.message.street);
                    frm.set_value('pincode',r.message.pincode);
                }
            });
        });

