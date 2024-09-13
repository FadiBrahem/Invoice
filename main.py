import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QLineEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt
import os
from database import Database
from jinja2 import Environment, FileSystemLoader
import pdfkit

# Update this path to point to your wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf=r'path to wkhtmltopdf.exe')

class InvoiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Invoice Application')
        self.setGeometry(100, 100, 800, 600)
        
        self.db = Database('invoices.db')
        self.template = 'template1.html'  # Default template
        
        self.initUI()
    
    def initUI(self):
        # Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        newInvoiceAction = QAction('New Invoice', self)
        newInvoiceAction.triggered.connect(self.new_invoice)
        fileMenu.addAction(newInvoiceAction)
        
        manageInvoicesAction = QAction('Manage Invoices', self)
        manageInvoicesAction.triggered.connect(self.manage_invoices)
        fileMenu.addAction(manageInvoicesAction)
        
        selectTemplateAction = QAction('Select Template', self)
        selectTemplateAction.triggered.connect(self.select_template)
        fileMenu.addAction(selectTemplateAction)
        
        # Central Widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        
        # Welcome Message
        self.welcome_label = QLabel('Welcome to the Invoice Application')
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)
    
    def new_invoice(self):
        # Clear the layout
        self.clear_layout()
        
        # Invoice Form
        self.invoice_form = InvoiceForm(self.template, self.db)
        self.layout.addWidget(self.invoice_form)
    
    def manage_invoices(self):
        # Clear the layout
        self.clear_layout()
        
        # Invoice Manager
        self.invoice_manager = InvoiceManager(self.db)
        self.layout.addWidget(self.invoice_manager)
    
    def select_template(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select Invoice Template", "templates/", 
            "HTML Files (*.html);;All Files (*)", options=options)
        if fileName:
            self.template = os.path.basename(fileName)
            QMessageBox.information(self, "Template Selected", f"Template {self.template} selected.")
    
    def clear_layout(self):
        # Remove all widgets from the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class InvoiceForm(QWidget):
    def __init__(self, template, db):
        super().__init__()
        self.template = template
        self.db = db
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.customer_label = QLabel('Customer Name:')
        self.customer_input = QLineEdit()
        
        self.amount_label = QLabel('Amount:')
        self.amount_input = QLineEdit()
        
        self.create_button = QPushButton('Create Invoice')
        self.create_button.clicked.connect(self.create_invoice)
        
        layout.addWidget(self.customer_label)
        layout.addWidget(self.customer_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.create_button)
        
        self.setLayout(layout)
    
    def create_invoice(self):
        customer = self.customer_input.text()
        amount = self.amount_input.text()
        
        if not customer or not amount:
            QMessageBox.warning(self, "Input Error", "Please enter customer name and amount.")
            return
        
        # Save to database
        invoice_id = self.db.insert_invoice(customer, amount)
        
        # Generate PDF
        self.generate_pdf(invoice_id, customer, amount)
        
        QMessageBox.information(self, "Invoice Created", f"Invoice {invoice_id} created successfully.")
        self.customer_input.clear()
        self.amount_input.clear()
    
    def generate_pdf(self, invoice_id, customer, amount):
        # Load template
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(self.template)

        html_content = template.render(
            invoice_id=invoice_id,
            customer=customer,
            amount=amount
        )

        # Ensure the invoices directory exists
        if not os.path.exists('invoices'):
            os.makedirs('invoices')

        # Generate PDF
        pdfkit.from_string(html_content, f'invoices/invoice_{invoice_id}.pdf', configuration=config)

class InvoiceManager(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Invoice ID', 'Customer', 'Amount'])
        
        self.load_invoices()
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_invoices(self):
        invoices = self.db.fetch_invoices()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(invoices):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InvoiceApp()
    window.show()
    sys.exit(app.exec_())
