# Software Requirements Specification (SRS)

## 1. Introduction
### 1.1 Purpose
Define requirements for the Vunjabei Clothing Management System, a web-based system for product, order, and user management.

### 1.2 Scope
The system supports two user roles:
- Admin: manage products, monitor dashboard stats, and update order status.
- Customer: browse products, place orders, and track own orders.

### 1.3 Intended Users
- Shop administrators
- Customers

## 2. Overall Description
### 2.1 Product Perspective
A full-stack application with:
- Django REST API backend
- React frontend client
- PostgreSQL relational database

### 2.2 System Environment
- Backend runtime: Python 3.13+
- Frontend runtime: Node.js 18+
- DBMS: PostgreSQL 14+
- Browser support: modern Chrome/Firefox/Edge

## 3. Functional Requirements
### FR-1 Authentication
- Users can register and login.
- Admin registration creates staff account.
- Login returns user role for route protection.

### FR-2 Product Management (Admin)
- Admin can create, update, and delete products.
- Product has name, category, price, quantity, and optional image.

### FR-3 Product Browsing (Customer)
- Customer can view product list and details.
- Customer can view stock and price before ordering.

### FR-4 Order Placement
- Authenticated customer can place order with quantity, phone, and address.
- System validates stock and prevents negative stock.

### FR-5 My Orders
- Customer can view own orders and current status.

### FR-6 Order Management (Admin)
- Admin can view all orders.
- Admin can update order status (Pending, Processing, Shipped, Delivered, Cancelled).

### FR-7 Dashboard Stats
- Admin dashboard can show products count, customers count, sales totals, and low stock items.

## 4. Non-Functional Requirements
### NFR-1 Performance
- Dashboard and list endpoints should respond within acceptable time under class-demo load.

### NFR-2 Security
- Session-based authentication.
- Role checks for admin-only endpoints.
- Environment variables for secrets and database credentials.

### NFR-3 Reliability
- Database transactions used in order placement to protect stock consistency.

### NFR-4 Maintainability
- Clear separation of backend API and frontend client.
- Clean project structure and assignment documentation.

## 5. Data Requirements
Main entities:
- Category
- Product
- Customer
- Sale
- SaleItem
- Order

## 6. Constraints
- Must use Django + React + REST API.
- Must use PostgreSQL (no embedded database).
- Must be deployed to public cloud URL for submission.

## 7. Acceptance Criteria
- Application runs locally with frontend and backend.
- Admin and customer flows are demonstrable.
- Repository includes README, .gitignore, SRS, and deployment report.
- Live deployment URL is accessible publicly.
