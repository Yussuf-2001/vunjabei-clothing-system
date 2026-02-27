# SOFTWARE REQUIREMENT SPECIFICATION (SRS)
## VUNJABEI CLOTHING MANAGEMENT SYSTEM
### The State University of Zanzibar

**Version:** 1.0
**Status:** Final
**Date:** 27-02-2026

**Student Name:** ____________________________
**Student Registration Number:** ____________________________

---

### **Document Approval**

| Role | Name | Signature | Date |
|---|---|---|---|
| Project Supervisor | | | |
| Student | | | |

---

## **Table of Contents**

**CHAPTER ONE: INTRODUCTION**
1.1. Introduction
1.2. Project Background
1.3. Project Objectives

**CHAPTER TWO: SYSTEM ANALYSIS**
2.1. Project Scope
2.2. Current System Description
2.3. Proposed Solution

**CHAPTER THREE: SYSTEM DESIGN**
3.1. System Architecture
3.2. Process Flow
3.3. Use Case Overview
3.4. Data Model

**CHAPTER FOUR: SYSTEM REQUIREMENTS**
4.1. Functional Requirements
4.2. Non-Functional Requirements

**CHAPTER FIVE: IMPLEMENTATION AND DEPLOYMENT**
5.1. Deployment
5.2. Glossary of Terms
5.3. References
5.4. Conclusion

---

## **CHAPTER ONE: INTRODUCTION**

### **1.1. Introduction**

This document presents the Software Requirement Specification (SRS) for the Vunjabei Clothing Management System. The purpose of this document is to formally describe the system requirements, operational environment, and constraints in a structured and professional manner. It serves as a reference for development, testing, and deployment of the system.

The Vunjabei Clothing Management System is a web-based application designed to automate clothing retail operations. The system provides a centralized digital platform for managing products, inventory, and customer orders. It replaces manual record-keeping methods with a secure, database-driven solution that ensures accuracy, reliability, and efficiency.

The system supports two primary user roles: Administrator and Customer. Each role interacts with the system through authenticated access with clearly defined privileges.

### **1.2. Project Background**

The current operational model at Vunjabei clothing business is fully manual. Sales transactions are recorded in notebooks, stock levels are determined through physical inspection, and customers must visit the shop or communicate by phone to confirm availability.

This manual approach introduces several operational challenges. Records can be lost or damaged, stock discrepancies occur frequently due to lack of real-time updates, and order tracking is not structured. Additionally, retrieving historical sales data is difficult and time-consuming.

To address these limitations, there is a need for a centralized web-based information system that ensures structured data storage, accurate stock tracking, and improved communication between customers and administrators.

### **1.3. Project Objectives**

The general objective of this project is to develop a reliable and secure web-based clothing management system that digitizes retail operations without changing the core business workflow.

Specifically, the system aims to:
*   Enable customers to register, browse products, and place orders remotely.
*   Allow administrators to manage products, monitor stock levels, and update order statuses efficiently.
*   Ensure that inventory updates occur automatically whenever an order is placed, thereby maintaining accurate stock records.

---

## **CHAPTER TWO: SYSTEM ANALYSIS**

### **2.1. Project Scope**

The system covers two main operational areas based on user roles.

**The Administrator module** allows authorized staff to:
*   Log in securely.
*   Manage products and categories.
*   Update stock quantities.
*   View customer orders.
*   Update order statuses such as Pending, Processing, Shipped, or Delivered.

**The Customer module** allows users to:
*   Register and log in.
*   Browse available products.
*   Place orders.
*   View their order history and current order status.

The system is web-based and accessible via internet-enabled devices. It does not include online payment processing or multi-branch management in its current version.

### **2.2. Current System Description**

The existing system is manual and paper-based. When a customer wants to purchase an item, staff manually check availability and record the sale in a notebook. There is no centralized storage of data, and stock updates depend entirely on manual counting.

This system lacks automation, is prone to human error, and does not provide customers with independent order tracking. The absence of digital reporting makes business performance analysis difficult.

### **2.3. Proposed Solution**

The proposed solution is a database-driven web application that centralizes product, user, and order data. The system ensures that all transactions are recorded electronically and stored securely in a relational database.

*   **Automation:** When a customer places an order, the system automatically deducts the ordered quantity from the available stock.
*   **Real-time Updates:** Administrators can immediately view incoming orders and update their statuses. Customers can log in at any time to check their order progress.
*   **Security:** The system enforces authentication and role-based access control to protect sensitive information and restrict unauthorized access.

---

## **CHAPTER THREE: SYSTEM DESIGN**

### **3.1. System Architecture**

The system follows a three-tier architecture consisting of presentation layer (frontend), application layer (backend), and data layer (database). Communication between the frontend and backend is performed through RESTful APIs using standard HTTP methods. The design ensures separation of concerns, maintainability, and scalability.

### **3.2. Process Flow**
1.  Customer registers an account.
2.  Customer logs into the system.
3.  Customer views available products.
4.  Customer places an order.
5.  Order is stored in the database and stock is updated automatically.
6.  Administrator logs in to view new orders.
7.  Administrator updates order status.
8.  Customer views updated order status.

### **3.3. Use Case Overview**

| Use Case ID | Use Case Name | Actor |
|---|---|---|
| **Administrator Use Cases** | | |
| UC-01 | Login | Administrator |
| UC-02 | Add/Update Product | Administrator |
| UC-03 | View All Orders | Administrator |
| UC-04 | Update Order Status | Administrator |
| **Customer Use Cases** | | |
| UC-05 | Register Account | Customer |
| UC-06 | Login | Customer |
| UC-07 | View Products | Customer |
| UC-08 | Place Order | Customer |
| UC-09 | View Order History | Customer |

### **3.4. Data Model**

The system database consists of four primary entities: User, Product, Order, and Category.

#### **3.4.1. User Entity**
| Attribute | Type | Description |
|---|---|---|
| id | Integer | Primary Key |
| username | Varchar | Unique user identifier for login |
| password | Varchar | Hashed password for security |
| email | Varchar | User's email address |
| is_staff | Boolean | Flag to identify administrator roles |

#### **3.4.2. Category Entity**
| Attribute | Type | Description |
|---|---|---|
| id | Integer | Primary Key |
| name | Varchar | Name of the product category (e.g., "T-Shirts") |

#### **3.4.3. Product Entity**
| Attribute | Type | Description |
|---|---|---|
| id | Integer | Primary Key |
| name | Varchar | Name of the product |
| category | ForeignKey | Links to the Category entity |
| price | Decimal | Unit price of the product |
| quantity | Integer | Available stock quantity |
| image | Varchar | URL path to the product image |

#### **3.4.4. Order Entity**
| Attribute | Type | Description |
|---|---|---|
| id | Integer | Primary Key |
| user | ForeignKey | Links to the User who placed the order |
| product | ForeignKey | Links to the ordered Product |
| quantity | Integer | Number of items ordered |
| total_price | Decimal | Calculated total price for the order |
| status | Varchar | Current status (e.g., Pending, Shipped) |
| date_ordered | DateTime | Timestamp when the order was placed |

Primary and foreign key relationships are used to maintain referential integrity. A single user can place multiple orders, and each product belongs to one category.

---

## **CHAPTER FOUR: SYSTEM REQUIREMENTS**

### **4.1. Functional Requirements**

*   The system shall allow customer registration and login.
*   The system shall allow administrator login with restricted access privileges.
*   The system shall allow administrators to add, edit, and update products.
*   The system shall update stock automatically after order placement.
*   The system shall allow administrators to update order status.
*   The system shall allow customers to place orders and view their order status.
*   All transactions shall be stored in the database.

### **4.2. Non-Functional Requirements**

*   **Security:** The system shall ensure security through authentication and controlled access. Passwords shall be stored securely using encryption mechanisms.
*   **Performance:** The system shall provide acceptable performance with response time within a few seconds under normal usage conditions.
*   **Reliability:** The system shall ensure reliability by maintaining data consistency and preventing data loss.
*   **Usability:** The system shall be user-friendly, with a simple and clear interface design.
*   **Availability:** The system shall be available continuously, subject to hosting service availability.

---

## **CHAPTER FIVE: IMPLEMENTATION AND DEPLOYMENT**

### **5.1. Deployment**

The backend application will be deployed on Render as a web service. The backend is developed using Django REST Framework to expose RESTful APIs.

The frontend interface is developed using React with Vite for build optimization. The system uses PostgreSQL for relational data storage.

During deployment, production settings will be configured, environment variables secured, database migrations executed, and HTTPS enabled to ensure secure communication between users and the server.

### **5.2. Glossary of Terms**

| Term | Definition |
|---|---|
| **SRS** | Software Requirement Specification: A formal document describing what a software system will do. |
| **API** | Application Programming Interface: A set of rules allowing different software applications to communicate with each other. |
| **RESTful** | Representational State Transfer: An architectural style for designing networked applications. |
| **CRUD** | Create, Read, Update, Delete: The four basic functions of persistent storage. |
| **UI** | User Interface: The visual part of an application through which a user interacts. |
| **Backend** | The server-side of an application that handles logic, database interactions, and APIs. |
| **Frontend** | The client-side of an application that the user directly interacts with. |

### **5.3. References**

*This section would include references to any standards, books, or other documents used in preparing the SRS.*

### **5.4. Conclusion**

The Vunjabei Clothing Management System provides a structured and centralized solution for managing clothing retail operations digitally. By automating inventory tracking and order management, the system eliminates inefficiencies associated with manual processes.

The technical design ensures security, scalability, and maintainability while preserving the original retail workflow. Upon implementation, the system will improve operational accuracy, enhance customer experience, and support future business growth.
