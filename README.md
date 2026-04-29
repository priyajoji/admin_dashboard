🛒 E-Commerce Admin Dashboard
-------------------------------

A full-stack admin system for managing an e-commerce platform, built using Flask, Streamlit, and MySQL. It provides a simple but functional control panel for product management, customer tracking, and sales monitoring.

The goal of this project is to simulate a real-world admin backend used in online retail systems.


Overview
--------------------------------------------

This system is split into two main components:

-Flask REST API → Handles all database operations (CRUD)
-Streamlit Dashboard → Provides an interactive admin interface

The frontend communicates with the backend through HTTP requests, making the system modular and easy to extend.

Core Features
--------------

-Product Inventory Management
  -Add new products with category and supplier mapping
  -View complete product catalog in a structured table
  -Update product details dynamically
  -Delete products from inventory
  
-Customer Management
  -View all registered customers
  -Clean, tabular representation of customer data
  -Real-time customer count metrics
  
-Sales Analytics
  -Total revenue calculation
  -Order history tracking
  -Average order value computation
  -Sales trend visualization over time
  
Architecture
------------

-Frontend: Streamlit (Admin Dashboard UI)
-Backend: Flask (REST API layer)
-Database: MySQL (Relational data storage)
-Communication: RESTful API using JSON payloads

The design follows a lightweight client-server architecture, separating UI logic from business logic.


API Design
-------------------------------------

The backend exposes the following endpoints:

Products:
---------

GET /products → Fetch all products
POST /products → Create a new product
PUT /products/<id> → Update product details
DELETE /products/<id> → Remove product

Customers:
----------

GET /customers → Retrieve all customers

Sales:
------

GET /sales → Retrieve order and revenue data
Setup Instructions

To run this project locally:

-Clone the repository and navigate into the project directory.
-Set up a Python virtual environment and install dependencies:
  -Flask
  -mysql-connector-python
  -streamlit
  -pandas
  -requests
-Create a MySQL database named ecommerce_db_2 and execute the provided schema file to generate tables.
-Start the Flask backend server.
-Launch the Streamlit dashboard.

Once both services are running, the dashboard will connect to the API automatically.

Design Philosophy
-----------------

This project focuses on simplicity and usability rather than over-engineering. The UI is designed to resemble a lightweight SaaS admin panel, prioritizing:

-Fast data access
-Minimal user friction
-Clear separation of concerns
-Easy extensibility for future features

Future Improvements
-------------------

Planned enhancements include:

-Authentication system for admin access
-Product image upload support
-Advanced filtering and search in inventory
-Role-based access control
-Deployment to cloud platforms (Render / AWS / Streamlit Cloud)
-Real-time dashboard analytics
