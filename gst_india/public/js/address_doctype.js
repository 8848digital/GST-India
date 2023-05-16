frappe.ui.form.on("Address","check_details", function(frm) {
            console.log(frm.selected_doc.gstin)
            frappe.call({
                method: "gst_india.cleartax_integration.API.gst.gstin_info",
                args: {
                    gstin: frm.selected_doc.gstin
                },
                callback: function (r) {
                    let data = r.message
                    let line1 = ""
                    if(data.floorNumber){
                        line1 = line1 + data.floorNumber
                    }
                    if(data.buildingNumber){
                        line1 = line1 + ","+ buildingNumber 
                    }
                    if(data.buildingName){
                        line1 = line1 + ","+ buildingName
                    }
                    frm.set_value('address_line1',line1);
                }
            });
        });

