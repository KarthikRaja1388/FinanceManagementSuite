# Finance Management Suite

Finance Management Suite is a comprehensive, modular web application built with Python and Django designed to help users track their personal finances, manage accounts, monitor budgets, categorize expenses, and organize shopping items. 

The project uses a structured, multi-app Django architecture to separate concerns, making it highly scalable and easily maintainable.

---

## 🚀 Features & Project Structure

The codebase is split into specific, dedicated Django applications:

- **`fms/`**: The core project configuration folder containing settings, primary routing (`urls.py`), and WSGI/ASGI configurations.
- **`identity/`**: Manages user authentication, including registration, login, logout, and profile controls.
- **`account/`**: Handles financial accounts (e.g., Bank Accounts, Credit Cards, Cash Wallets) and tracks current balances.
- **`budget/`**: Allows users to set monthly or category-specific spending limits and track progress against goals.
- **`category/`**: Manages expense and income categories (e.g., Groceries, Rent, Salary, Entertainment) to systematically organize transactions.
- **`transaction/`**: Records cash inflows and outflows, linking specific movements to accounts and categories.
- **`shopping/`**: Integrated shopping or wishlist management to help plan future purchases against current financial standings.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Django Framework
- **Frontend:** HTML5, CSS3, Django Template Engine
- **Database:** Postgres (for development)

---

