# BISMMS — Bookstore Inventory & Stock Maintenance Management System

A web-based inventory and stock management system built for a retail academic bookstore. Developed as part of a Professional Practice and Development (PPD) academic project.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 6.0 |
| Database | PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript |
| PDF Generation | ReportLab |
| Email | Gmail SMTP |
| IDE | PyCharm |
| Version Control | Git / GitHub |

---

## Features

- **Role-Based Access Control (RBAC)** — Admin, Manager, and Staff roles with module-level access restrictions
- **Book & Category Management** — Add, edit, delete, and search academic books by title, author, ISBN, subject, or publisher
- **Stock-In Management** — Record incoming books from publishers/distributors with automatic quantity updates
- **Stock-Out Management** — Record outgoing sales with stock deduction and negative-quantity prevention
- **Supplier Management** — Manage publisher and distributor records linked to stock transactions
- **Low-Stock Alerts** — Automatic dashboard alerts when stock falls below reorder level
- **Email Notifications** — Automated Gmail SMTP emails to all active Admin and Manager users on low-stock trigger
- **Reports** — Current Stock, Stock Movement (with date filter), and Low-Stock reports
- **PDF Export** — Export all 3 report types to PDF via ReportLab
- **Audit Logging** — Full action trail: login, logout, stock-in, stock-out, book and user management actions — Admin only
- **Session Timeout** — Automatic session expiry after 30 minutes of inactivity
- **Dashboard** — Live stats: total books, low-stock count, total inventory value, recent transactions

---

## Project Structure

```
BISMMS/
├── apps/
│   ├── accounts/       # Authentication, user management, RBAC
│   ├── inventory/      # Books and categories
│   ├── stock/          # Stock-in and stock-out transactions
│   ├── suppliers/      # Publisher and distributor records
│   ├── alerts/         # Low-stock detection and email notifications
│   ├── reports/        # Report generation and PDF export
│   ├── dashboard/      # Live stats and overview
│   └── audit/          # Audit logging (Admin only)
├── bismms_project/     # Django project settings and URLs
├── templates/          # Global base template and partials
├── static/             # CSS, JS, images
├── manage.py
├── requirements.txt
└── .env                # Environment variables (not tracked)
```

---

## Role Access Matrix

| Feature | Staff | Manager | Admin |
|---|---|---|---|
| Login / Logout | ✓ | ✓ | ✓ |
| Books & Categories | ✓ | ✓ | ✓ |
| Stock-In & Stock-Out | ✓ | ✓ | ✓ |
| Dashboard | ✓ | ✓ | ✓ |
| Suppliers | ✗ | ✓ | ✓ |
| Reports & PDF Export | ✗ | ✓ | ✓ |
| Alerts | ✗ | ✓ | ✓ |
| User Management | ✗ | ✗ | ✓ |
| Audit Log | ✗ | ✗ | ✓ |
| Django Admin Panel | ✗ | ✗ | ✓ |

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SUJALL-MOHAPATRA/Bookstore-Stock-and-Inventory-Management-System.git
cd Bookstore-Stock-and-Inventory-Management-System
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with the following:

```
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=bismms_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
```

> **Note:** For email, use a Gmail App Password (not your regular Gmail password). Enable 2-Step Verification on the Gmail account first, then generate an App Password under Google Account → Security → App Passwords.

### 5. Set up the database

Create a PostgreSQL database named `bismms_db` (or whatever you set in `.env`), then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Key URLs

| URL | Description |
|---|---|
| `/accounts/login/` | Login page |
| `/dashboard/` | Main dashboard |
| `/inventory/books/` | Book list |
| `/stock/in/` | Record stock-in |
| `/stock/out/` | Record stock-out |
| `/suppliers/` | Supplier management |
| `/reports/stock/` | Current stock report |
| `/reports/movement/` | Stock movement report |
| `/reports/lowstock/` | Low-stock report |
| `/alerts/` | Low-stock alert list |
| `/accounts/users/` | User management (Admin) |
| `/audit/` | Audit log (Admin) |
| `/admin/` | Django admin panel (Admin) |

---

## Academic Context

This project was developed as part of a **Professional Practice and Development (PPD)** course. It follows the Software Requirements Specification (SRS) based on IEEE Std 830-1998, covering functional requirements REQ-F-001 through REQ-F-029 and non-functional requirements REQ-NF-001 through REQ-NF-009.

---

## License

This project is academic in nature and is not licensed for commercial use.
