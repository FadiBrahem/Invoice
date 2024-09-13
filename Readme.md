Invoice Application

A desktop invoice application built with Python and PyQt5, allowing users to create and manage invoices, select templates, and generate PDF invoices.
Table of Contents

    Features
    Prerequisites
    Installation
    Configuration
    Running the Application
    Usage
        Creating a New Invoice
        Managing Invoices
        Selecting a Template
    Templates
    Troubleshooting
    Contributing
    License

Features

    Create new invoices with customer name and amount.
    Manage existing invoices (view invoices in a table).
    Select different invoice templates.
    Generate invoices as PDF files.
    Simple and user-friendly GUI.

Prerequisites

Before running the application, ensure you have the following installed on your system:

    Python 3.x
    pip (Python package installer)
    wkhtmltopdf (for PDF generation)

Installation

    Clone the Repository or Download the Source Code

    

git clone https://github.com/FadiBrahem/invoice-application.git
cd invoice-application

Install Required Python Packages

Install the necessary Python packages using pip:

bash

    pip install PyQt5 jinja2 pdfkit

    Install wkhtmltopdf
        Download wkhtmltopdf from the official website and install it.
        Ensure that wkhtmltopdf is added to your system's PATH environment variable.

    Note for Windows Users:
        The default installation path is usually C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe.
        Make sure to note this path for configuration.

Configuration

Update the path to wkhtmltopdf in the main.py file:

python

# In main.py
import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')  # Update this path

    Replace the path with the actual path to your wkhtmltopdf executable.
    Use a raw string (r'') to avoid issues with backslashes in Windows paths.

Running the Application

Run the application using the following command:

bash

python main.py

The application window should appear, displaying the main interface.
Usage
Creating a New Invoice

    Go to the File menu and select New Invoice.
    Enter the Customer Name and Amount in the provided fields.
    Click the Create Invoice button.
    A confirmation message will appear upon successful creation.
    The invoice PDF will be saved in the invoices directory.

Managing Invoices

    Go to the File menu and select Manage Invoices.
    A table will display all existing invoices with their ID, customer name, and amount.
    Use this section to view invoice details.

Selecting a Template

    Go to the File menu and select Select Template.
    A file dialog will open, allowing you to choose an HTML template from the templates directory.
    Select a template and confirm.
    The selected template will be used for generating future invoices.

Templates

    Invoice templates are HTML files stored in the templates directory.

    The default template is template1.html.

    You can create custom templates using HTML and Jinja2 templating.

    Template variables available:
        {{ invoice_id }}
        {{ customer }}
        {{ amount }}

    Example Template (template1.html):

    html

    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Invoice {{ invoice_id }}</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .invoice-box { max-width: 800px; margin: auto; padding: 30px; }
            .header { text-align: center; }
            .details { margin-top: 20px; }
            .details th, .details td { padding: 5px; text-align: left; }
        </style>
    </head>
    <body>
        <div class="invoice-box">
            <h1 class="header">Invoice {{ invoice_id }}</h1>
            <table class="details">
                <tr>
                    <th>Customer Name:</th>
                    <td>{{ customer }}</td>
                </tr>
                <tr>
                    <th>Amount:</th>
                    <td>${{ amount }}</td>
                </tr>
            </table>
        </div>
    </body>
    </html>

Troubleshooting

    Application Doesn't Start
        Ensure all dependencies are installed.
        Check for any errors in the console and resolve them.

    PDF Not Generated
        Verify that wkhtmltopdf is correctly installed and the path is properly set.
        Check if the invoices directory exists or if the application has permission to create it.

    Template Not Found
        Make sure the selected template exists in the templates directory.
        Confirm that the template filename matches exactly (case-sensitive).

    Error Messages
        Read the error messages displayed in the application or console to identify the issue.
        Common issues include indentation errors or missing files.

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.

    Create a new branch:

    bash

git checkout -b feature/your-feature-name

Commit your changes:

bash

git commit -m 'Add your feature'

Push to the branch:

bash

    git push origin feature/your-feature-name

    Open a Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Note: This application is a basic implementation intended for educational purposes. For production use, consider adding more features, security measures, and validations.
