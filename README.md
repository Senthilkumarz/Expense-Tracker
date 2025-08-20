**Expense Tracker API Documentation**

---

**1. Overview:**

* Expense Tracker API allows multiple users to record and view their expenses.
* Supports user registration, authentication, expense management, and monthly summaries.
* Backend: Django REST Framework
* Database: SQLite
* Authentication: JWT-based
* Frontend: HTML, CSS (Tailwind), JavaScript

---

**2. User Management:**

* **Register**

  * Endpoint: `POST /api/register/`
  * Payload: `{"username": "string", "email": "string", "password": "string"}`
  * Response: Created user object.
* **Login**

  * Endpoint: `POST /api/login/`
  * Payload: `{ "email": "string", "password": "string" }`
  * Response: `{ "access": "JWT", "refresh": "JWT" }`

---

**3. Expense Management:**

* **Add Expense**

  * Endpoint: `POST /api/expenses/`
  * Payload: `{ "amount": number, "category": "string", "description": "string", "date": "YYYY-MM-DD" }`
  * JWT Authorization required.
* **List Expenses**

  * Endpoint: `GET /api/expenses/`
  * Filters: `?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&category=string&sort=date|amount&page=1&size=10`
  * JWT Authorization required.
* **Update Expense**

  * Endpoint: `PUT /api/expenses/{id}/`
  * Payload same as Add Expense.
  * JWT Authorization required.
* **Delete Expense**

  * Endpoint: `DELETE /api/expenses/{id}/`
  * JWT Authorization required.

---

**4. Monthly Summary:**

* Endpoint: `GET /api/summary/monthly/`
* Returns total expenses per month per category for the logged-in user.
* JWT Authorization required.

---

**5. Data Validation:**

* All input fields are validated.
* Amount must be numeric and positive.
* Category must be one of the predefined categories.
* Date must be a valid date.
* Returns detailed field errors for invalid inputs.

---

**6. Pagination & Sorting:**

* `GET /api/expenses/` supports pagination with `page` and `size` query parameters.
* Sorting supported by `sort` query parameter (`date` or `amount`).

---

**7. Frontend Overview:**

* Login and store JWT in `localStorage`.
* Add expense form with validation.
* Fetch expenses with filters and sorting.
* Display expenses in a table.
* Display all registered users in a table (optional).
* Styling using Tailwind CSS.

---

**8. Unit Tests (Backend):**

* Test user login and JWT generation.
* Test expense creation with valid and invalid payloads.
* Test expense listing with filters and pagination.

---

**9. Database:**

* Users table (Django built-in)
* Expenses table:

  * `user` (ForeignKey)
  * `amount` (Decimal)
  * `category` (CharField)
  * `description` (TextField)
  * `date` (DateField)

---

**10. Notes:**

* Only logged-in users can manage their own expenses.
* JWT token required for all protected endpoints.
* Frontend communicates with backend using fetch API and authorization headers.
* Pagination and sorting improve usability for large datasets.
