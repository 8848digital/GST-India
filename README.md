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
    4. Click the Enable checkbox to enable all features.
      ![a528497c-8f2a-4b30-befa-922d0d511104](https://user-images.githubusercontent.com/48561545/206154731-e82b4746-744b-4d0f-ad6d-88f30aa5c126.png)
    5. Check the Sandbox checkbox for testing and uncheck it for production mode.
      ![e4db45ad-73c2-4bf2-a610-9ff35c104328](https://user-images.githubusercontent.com/48561545/206154931-dc22a05e-3958-497c-9e20-793f926b5641.png)
    6. Check the Automate checkbox if you want automatic generation of IRNs and EWBs on submit of documents.
      ![890bac94-cae5-47b6-bf5f-b11d6d602d1d](https://user-images.githubusercontent.com/48561545/206155163-323c2387-cd2b-4f6a-aedf-92318ee81886.png)

        
2. SMB Users






## License

[GNU General Public License (v3)](https://github.com/resilient-tech/india-compliance/blob/develop/license.txt)
