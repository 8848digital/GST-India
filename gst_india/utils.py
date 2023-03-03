import frappe
from frappe import *
import json

def get_dict(type,doc):
    if frappe.db.exists(type,doc):
        return frappe.get_doc(type,doc).as_dict()
    return None

    
def success_response(data=None):
    response = {'msg': 'success'}
    if data: 
        response['data'] = data
    return response 

def error_response(err_msg):
    return {
        'msg': 'error',
        'error': err_msg
    }

def response_error_handling(response):
    error = ""
    errors = []
    if type(response) ==list:
        response = response[0]
    if type(response) == str:
        return error_response(response)
    if type(response) == None:
        return error_message("No response received!")
    if response.get('govt_response'):
        if response.get('govt_response').get('ErrorDetails'):
            errors = response.get('govt_response').get('ErrorDetails')
    elif response.get('ErrorDetails'):
        errors = response.get('ErrorDetails')
    elif response.get('errorDetails'):
        errors.append(response.get('errorDetails'))
    elif response.get('errors') and response.get('errors').get('errors'):
            errors = response.get('errors').get('errors') 
    else:
        errors.append({'error_message':json.dumps(response)})
    c=1
    for i in errors:
        error += str(c) + ". " + i.get("error_message") + "\r\n"
        c+=1 
    return error_response(error)



        
def response_logger(payload,response,api,doc_type,doc_name,status="Failed"):
    try:
        response = json.dumps(response, indent=4, sort_keys=False, default=str)
        if frappe.db.exists('Cleartax Api Log',{'document_name':doc_name,'api':api}):
            doc = frappe.get_doc('Cleartax Api Log',{'document_name':doc_name,'api':api})
            doc.request_data = payload
            doc.response = response
            doc.status = status
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.new_doc('Cleartax Api Log')
            doc.document_type = doc_type
            doc.document_name = doc_name
            doc.api = api
            doc.request_data = payload
            doc.response = response
            doc.status = status
            doc.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.logger('response').exception(e)

def get_url():
    if frappe.db.get_single_value('Cleartax Settings','enable'):
        return frappe.db.get_single_value('Cleartax Settings','host_url')
    elif frappe.db.get_single_value('Masters India Settings','enable'):
        return frappe.db.get_single_value('Cleartax Settings','host_url')
    frappe.throw("Please Enable Cleartax or Masters India GSP!")

def set_headers():
    if frappe.db.get_single_value('Cleartax Settings','enable'):
        return cleartax_headers()
    elif frappe.db.get_single_value('Masters India Settings','enable'):
        return masters_india_headers()
    frappe.throw("Please Enable Cleartax or Masters India GSP!")
        

def cleartax_headers():
    doc = frappe.get_doc("Cleartax Settings")
    headers = {
        'sandbox': str(doc.sandbox),
        'Content-Type': 'application/json'
    }
    if not doc.enterprise:
        return headers
    if doc.sandbox and doc.sandbox_auth_token:
        headers['token'] = doc.get_password('sandbox_auth_token')
        return headers
    if doc.production_auth_token:
        headers['token'] = doc.get_password('production_auth_token')
    return headers


def masters_india_headers():
    doc = frappe.get_doc("Masters India Settings")
    headers = {
        'sandbox': str(doc.sandbox),
        'Content-Type': 'application/json'
    }
    if doc.access_token:
        headers['token'] = doc.access_token
    return headers

