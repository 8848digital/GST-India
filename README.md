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
        
2. SMB Users






## License

[GNU General Public License (v3)](https://github.com/resilient-tech/india-compliance/blob/develop/license.txt)
