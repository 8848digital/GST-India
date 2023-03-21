

def before_save(doc,method=None):
    cr = doc.conversion_rate
    if cr:
        for item in doc.shipment_item:
            item.company_rate = item.rate * cr 
            item.amount = item.rate * item.qty 
            item.company_amount = item.amount * cr  
