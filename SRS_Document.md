# Software Requirements Specification (SRS)

## The State University of Zanzibar
## Vunjabei Clothing Management System

Student Name: ____________________  
Student Registration Number: ____________________  
Course: Cloud Application Development and Deployment Using GitHub  
Submission Date: ____________________

## Table of Contents
1. Software Development Standards  
2. Introduction  
3. Project Background  
4. Project Objective  
5. Project Scope  
6. Current System Description  
7. Proposed System  
8. System Design  
9. Process Diagrams  
10. Use Cases  
11. Data Models  
12. Functional Requirements  
13. Non-Functional Requirements  
14. Deployment  
15. Conclusion

## 1. Software Development Standards
This project follows practical software development standards required by the assignment:
- Full-stack architecture: Django REST API backend + React frontend.
- Version control: Git and GitHub with meaningful commit messages.
- Documentation: README, SRS, deployment report, and assignment checklist.
- Environment-based configuration using `.env` values.
- Database standard: PostgreSQL (no embedded SQLite as primary project database).
- API-first communication between frontend and backend.
- Role-based access behavior for admin and customer features.

## 2. Introduction
The Vunjabei Clothing Management System is a web application that manages clothing products, customer orders, and order tracking. The system is designed for two user groups:
- Admin users who manage products and orders.
- Customer users who browse products and place orders.

The system was developed to demonstrate cloud application development, GitHub workflow, and deployment skills.

## 3. Project Background
Small and medium clothing businesses often face challenges in controlling stock, managing customer orders, and tracking order status. Manual methods lead to delays, missing records, and poor visibility.

This project solves those problems by providing a centralized, web-based platform where business operations are digitized and easy to monitor.

## 4. Project Objective
### 4.1 General Objective
To develop and deploy a functional cloud-ready clothing management system using GitHub-based workflow.

### 4.2 Specific Objectives
- To build a responsive frontend using React.
- To create backend API services using Django REST Framework.
- To connect the application to PostgreSQL database.
- To implement role-based features for admin and customer.
- To deploy the application using cloud platforms integrated with GitHub.
- To produce complete project documentation for presentation and submission.

## 5. Project Scope
### 5.1 In Scope
- User registration and login.
- Admin dashboard with key statistics.
- Product management (create, read, update, delete).
- Product browsing for customers.
- Place order functionality.
- Customer order history and status tracking.
- Admin order status updates (Pending, Processing, Shipped, Delivered, Cancelled).
- GitHub repository management and cloud deployment documentation.

### 5.2 Out of Scope
- Online payment gateway integration.
- SMS/Email notification service.
- Multi-vendor marketplace support.
- Advanced analytics and AI recommendations.

## 6. Current System Description
Before this solution, clothing business operations are typically handled manually:
- Product records are stored in notebooks or scattered files.
- Orders are tracked through calls/chats without status history.
- Stock updates are inconsistent after sales.
- Reporting is slow and error-prone.

Limitations of current/manual approach:
- High risk of data loss and duplicate entries.
- No centralized access for monitoring.
- Poor customer experience due to unclear order status.

## 7. Proposed System
The proposed system is a centralized web application with clear separation of responsibilities:
- React frontend provides user interfaces for admin and customers.
- Django REST API handles business logic and validation.
- PostgreSQL stores persistent data reliably.

Expected improvements:
- Faster and accurate order processing.
- Better stock visibility and management.
- Better customer trust through order status tracking.
- Easier maintenance and deployment through GitHub workflow.

## 8. System Design
### 8.1 Architecture Overview
- Presentation Layer: React (Vite + Bootstrap)
- Application Layer: Django + Django REST Framework APIs
- Data Layer: PostgreSQL

### 8.2 User Roles
- Admin:
- Manage products.
- View all orders.
- Update order statuses.
- View dashboard stats.

- Customer:
- Register and login.
- Browse products.
- Place orders.
- View personal order history.

### 8.3 Main Modules
- Authentication module
- Product management module
- Order management module
- Dashboard/statistics module
- Deployment/configuration module

## 9. Process Diagrams
### 9.1 Customer Order Process (Text Flow)
1. Customer logs in.
2. Customer views product list/details.
3. Customer selects quantity and submits order.
4. Backend validates stock and user.
5. Order is created and product stock is reduced.
6. Customer views order under "My Orders" with current status.

### 9.2 Admin Order Status Process (Text Flow)
1. Admin logs in.
2. Admin opens Order Management page.
3. System displays all orders.
4. Admin changes status to Processing/Shipped/Delivered/Cancelled.
5. Backend validates admin permission and updates status.
6. Updated status is visible to customer.

### 9.3 Process Diagram (Text)
```text
Customer Login
    |
    v
Browse Products -> Select Product & Quantity -> Submit Order
                                                |
                                                v
                                        [Stock Available?]
                                          /            \
                                        No              Yes
                                        |                |
                                        v                v
                                Show Error Message   Create Order
                                                          |
                                                          v
                                                    Reduce Stock
                                                          |
                                                          v
                                                    Show My Orders

Admin Login -> Open Order Management -> View Orders -> Update Status -> Saved
```

## 10. Use Cases
### UC-01: Register User
- Actor: Customer/Admin
- Precondition: User is not logged in.
- Main Flow: Enter credentials and submit registration form.
- Postcondition: User account is created.

### UC-02: Login
- Actor: Customer/Admin
- Precondition: User account exists.
- Main Flow: Enter username/password, system authenticates.
- Postcondition: User enters role-based dashboard.

### UC-03: Manage Products
- Actor: Admin
- Precondition: Admin is authenticated.
- Main Flow: Create/edit/delete products and upload image.
- Postcondition: Product catalog is updated.

### UC-04: Place Order
- Actor: Customer
- Precondition: Customer is authenticated and product has stock.
- Main Flow: Select product, quantity, address/phone, submit order.
- Postcondition: Order is saved and stock is reduced.

### UC-05: Update Order Status
- Actor: Admin
- Precondition: Admin is authenticated and order exists.
- Main Flow: Select order and change status.
- Postcondition: Order status is updated.

### UC-06: View My Orders
- Actor: Customer
- Precondition: Customer is authenticated.
- Main Flow: Open My Orders page.
- Postcondition: Customer sees own order history and statuses.

### 10.1 Use Case Diagram (Text)
```text
Actors:
  - Customer
  - Admin

Customer Use Cases:
  - Register
  - Login
  - Browse Products
  - Place Order
  - View My Orders

Admin Use Cases:
  - Login
  - Manage Products
  - View All Orders
  - Update Order Status
  - View Dashboard Stats
```

## 11. Data Models
### 11.1 Main Entities
- User (Django auth user)
- Customer
- Category
- Product
- Order
- Sale
- SaleItem

### 11.2 Key Relationships
- One Category has many Products.
- One User can place many Orders.
- One Product can appear in many Orders.
- One Sale can contain many SaleItems.
- One Customer can be linked to many Sales.

### 11.3 Important Attributes (Examples)
- Product: `name`, `category`, `price`, `quantity`, `image`
- Order: `user`, `product`, `quantity`, `total_price`, `status`, `phone`, `address`, `date_ordered`

### 11.4 ERD Diagram (Text)
```text
CATEGORY (1) --------< (M) PRODUCT (1) --------< (M) ORDER >-------- (1) USER
                                           \
                                            \--------< (M) SALE_ITEM >-------- (1) SALE

CUSTOMER (1) --------< (M) SALE >-------- (1) USER

Main Entities:
- USER(id, username, is_staff)
- CATEGORY(id, name)
- PRODUCT(id, name, price, quantity, category_id)
- ORDER(id, user_id, product_id, quantity, total_price, status, phone, address, date_ordered)
- CUSTOMER(id, name, phone, email, address)
- SALE(id, user_id, customer_id, total_amount, date)
- SALE_ITEM(id, sale_id, product_id, quantity, price)
```

## 12. Functional Requirements
- FR-01: System shall allow customer registration.
- FR-02: System shall allow user login and role detection (admin/customer).
- FR-03: System shall allow admin to add, update, and delete products.
- FR-04: System shall display products with category, price, quantity, and image.
- FR-05: System shall allow customer to place order with quantity, phone, and address.
- FR-06: System shall validate stock and update inventory after successful order.
- FR-07: System shall allow customer to view personal order history.
- FR-08: System shall allow admin to view all orders, update order status, and view dashboard statistics.

## 13. Non-Functional Requirements
- NFR-01 (Usability): Interfaces shall be simple and responsive on modern browsers.
- NFR-02 (Performance): Common API requests should return within acceptable response time under classroom demo load.
- NFR-03 (Security): Authentication and role checks shall protect admin operations.
- NFR-04 (Data Integrity): Order creation shall use transaction-safe updates to avoid stock inconsistency.
- NFR-05 (Maintainability): Codebase shall maintain clear folder structure for backend and frontend.
- NFR-06 (Portability): System shall run in local and cloud environments using environment variables.

## 14. Deployment
### 14.1 Deployment Strategy
- Source code hosted on GitHub (public repository).
- Backend deployment target: Render.
- Frontend deployment target: Vercel or Netlify.
- Optional CI/CD through GitHub Actions.

### 14.2 Required Environment Variables
- Backend: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`
- Frontend: `VITE_API_BASE_URL`

### 14.3 Deployment Deliverables for Assignment
- GitHub repository link
- Public live deployment URL
- Screenshots of commit history
- Screenshots of running application
- One-page deployment explanation

## 15. Conclusion
The Vunjabei Clothing Management System satisfies the core assignment requirements by combining:
- Functional full-stack implementation,
- Proper GitHub workflow,
- PostgreSQL-based data management,
- Cloud deployment readiness,
- Complete supporting documentation.

This SRS provides a clear blueprint for development, testing, deployment, and presentation of the project.
