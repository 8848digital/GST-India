<div align="center">

<!-- TODO: add link to website once it is ready -->
<h1>GST INDIA</h1>

</div>



## Introduction

This project aims to integrate the ClearTax portal's APIs with the ERPNext solution. The user can directly generate e-invoices, IRNs, and E-way bills and cancel them from within ERPNext.

It works on top of [ERPNext](https://github.com/frappe/erpnext) and the [Frappe Framework](https://github.com/frappe/frappe) - incredible FOSS projects built and maintained by the incredible folks at Frappe. Go check these out if you haven't already!

## Key Features

- E-invoicing (Generation/Cancellation)
- E-Way Bills (Generation/Cancellation/Updation)
- GST Invoices (Generation)
- Credit/Debit Notes
- Export Invoices


## Prerequisites

- Cleartax Account ( Only for Enterprise Users)
- Erpnext(v13 & above)
- Frappe (v13 & above)

## Installation

Once you've [set up a Frappe site](https://frappeframework.com/docs/v14/user/en/installation/), installing India Compliance is simple:


1. Download the app using the Bench CLI

  ```bash
  bench get-app https://github.com/8848digital/GST-India.git
  ```

2. Install the app on your site

  ```bash
  bench --site [site name] install-app india_compliance
  ```

## Setup Instructions

1. Enterprise Users
    1. Go to Cleartax Settings
    
      ![3edc54eb-ebc2-4376-9f40-789be607ada2](https://user-images.githubusercontent.com/48561545/206153841-efcdbda0-33f1-4607-9e6c-bf4fcb44b35d.png)
      
    2. Check the Enterprise checkbox
    
      ![a3c5a656-4c6e-4351-a408-5a952066a621](https://user-images.githubusercontent.com/48561545/206154012-583a8108-a845-46ff-8c24-cd9cd9aa3ce9.png)
      
    3. Under Enterprise Details, enter the auth tokens, GSTINs and their corresponding tax entity IDs
    
      ![bf71efbc-f6cc-4986-88e7-fbb30db4936d](https://user-images.githubusercontent.com/48561545/206154488-77bdcd35-e214-4987-9aab-630fb4a7e4b0.png)
      
2. SMB Users

     1. Go to Cleartax Settings
    
      ![3edc54eb-ebc2-4376-9f40-789be607ada2](https://user-images.githubusercontent.com/48561545/206153841-efcdbda0-33f1-4607-9e6c-bf4fcb44b35d.png)
      
    2. Uncheck the Enterprise checkbox
    
      ![a3c5a656-4c6e-4351-a408-5a952066a621](https://user-images.githubusercontent.com/48561545/206154012-583a8108-a845-46ff-8c24-cd9cd9aa3ce9.png)
    
3. Common Setup Instructions
      
    1. Click the Enable checkbox to enable all features.
    
      ![a528497c-8f2a-4b30-befa-922d0d511104](https://user-images.githubusercontent.com/48561545/206154731-e82b4746-744b-4d0f-ad6d-88f30aa5c126.png)
      
    2. Check the Sandbox checkbox for testing and uncheck it for production mode.
    
      ![e4db45ad-73c2-4bf2-a610-9ff35c104328](https://user-images.githubusercontent.com/48561545/206154931-dc22a05e-3958-497c-9e20-793f926b5641.png)
      
    3. Check the Automate checkbox if you want automatic generation of IRNs and EWBs on submit of documents.
    
      ![890bac94-cae5-47b6-bf5f-b11d6d602d1d](https://user-images.githubusercontent.com/48561545/206155163-323c2387-cd2b-4f6a-aedf-92318ee81886.png)
      
    4. Select the companies that require E- Invoicing here
    
       ![download](https://user-images.githubusercontent.com/48561545/206155995-9673c24a-9c64-4612-887c-4bdcacfc4b49.png)
       
    5. Let the Host Site have the default value unless asked to change by the organization.

        
## Functionalities

### E-Invoicing

   1. You can generate IRNs for a Sales Invoice(submitted) by clicking Create -> IRN
   
      ![519b521a-a2e0-4430-97a0-54a63c2c7a97](https://user-images.githubusercontent.com/48561545/206352385-fb397afb-508f-4899-815c-12e18ebeb64f.png)

   2. You can see the IRN details in the E-Invoicing section in the More Info tab.
   
      ![263d0b80-caaf-487f-b96e-8287b55b49ed](https://user-images.githubusercontent.com/48561545/206352467-ff6be3b3-5ab6-4814-8ed0-b0da9d04544b.png)

      
   3. If there are issues with the document, a popup will display the errors.
   4. You can also check the errors from Cleartax Api Log List
   5. After generating IRN, now you can generate EWB by IRN.
   6. In order to generate EWB, 
      1. The Sales Invoice must be generated from a Delivery Note
      2.  (OR) A Delivery Note must be generated from the Sales Invoice
      3.  (OR) Transporter Details must be created from the Sales Invoice.
   7. To generate EWB, click Create -> EWB 
   8. EWB details will be in the Ewaybill section in the More Info tab
   9. You can cancel EWB and IRN from Cancel EWb and Cancel IRN Buttons at the top.
   10. You can also generate EWb from a Delivery Note. i.e. EWB Without IRN
   11. In Delivery Note, you can enter the vehicle details, and update with the cleartax Portal. 
   12. This can be done using the Update Part B Button.
   13. You can also generate IRN for a Credit Note(same as Sales Invoice)

### GST Invoice
  1. You Can Generate GST Invoice for the Following Documents
      1. Sales Invoice
      2. Purchase Invoice
      3. Credit Note
      4. Debit Note
  2. To Generate GST Invoice, the billing company must be removed from E-Invoicing list in cleartax Settings
  3. Click on Create -> GST Invoice
   
### Error Log
   1. Incase anything goes wrong when generating an IRN/EWB/GST Invoice, you can look into the error logs and resolve the data.
   2. To Check Error logs, go to Cleartax Api Log List.
   3. You can filter the log by Document ID and API TYPE(i.e. IRN,EWB etc)
   
### Bulk Generation
   1. You can generate IRN and EWB in bulk from Sales Invoice List and Delivery Note List.
   2. Select the documents, then click on Action -> IRN/EWB.

### Dashboards
   We have created 3 dashboards
   1. E-Invoicing
   2. EWB (IRN - Sales Invoice)
   3. EWB (Delivery Note)
   
   You can get the count of generated, pending, failed, cancelled and also a monthly chart in these dashboards.
  
    

  






