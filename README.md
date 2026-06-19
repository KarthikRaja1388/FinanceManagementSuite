# Personal Project: Finance Management Suite

Welcome to the **Finance Management Suite**! This project was built as a dedicated learning endeavor designed to master the fundamentals of full-stack web development using **Python** and **Django**. 

Rather than deploying a public-facing product, the core objective of this project was to tackle real-world software engineering challenges: managing relational databases, designing a modular backend architecture, and implementing secure user authentication.

---

## 🧠 Key Learning Objectives & Achievements

Building this suite allowed me to shift from theoretical coding to structuring a production-ready application. Key skills showcased in this codebase include:

*   **Modular Django Architecture:** Instead of building a monolithic app, I split the ecosystem into dedicated, decoupled Django apps (`identity`, `account`, `budget`, `category`, `transaction`, `shopping`). This taught me how to keep code maintainable, scalable, and organized.
*   **Relational Database Design:** Designed a robust data schema utilizing Django’s ORM. I implemented **Foreign Keys** and relational links to cleanly map users to accounts, accounts to categories, and transactions to specific budgets.
*   **State Management & Logic Flow:** Gained a deep understanding of handling financial mathematical logic in the backend—ensuring balances accurately update when a transaction is added, modified, or deleted.
*   **Authentication & Security:** Implemented secure user onboarding pipelines within the `identity` app, handling session management, registration, and user-scoped data protection.

---

## 🛠️ Project Blueprint & Breakdown

The project repository is broken down into specific operational modules, showcasing clean separation of concerns:

| App Module | Learning Focus | Purpose & Functionality |
| :--- | :--- | :--- |
| **`fms/`** | Core Configuration | Houses global settings, WSGI/ASGI servers, and primary routing structures. |
| **`identity/`** | Security & Auth | Custom user registration, secure login/logout workflows, and user scoping. |
| **`account/`** | Resource Management | Tracks user-created financial hubs (e.g., Bank Accounts, Cash, Credit). |
| **`category/`** | Data Classification | Implements categorical sorting (Groceries, Salary, Utilities) for granular metrics. |
| **`transaction/`** | Ledger Mechanics | Handles incoming/outgoing flow logs, validating balances against structural constraints. |
| **`budget/`** | Analytical Logic | Allows configuration of spending ceilings, tracking threshold crossings. |
| **`shopping/`** | Wishlist Aggregation | Sandbox feature to practice prioritizing future target purchases against current asset pools. |

---

## 💻 Technical Stack

- **Language:** Python 3.x
- **Framework:** Django (MVC/MVT Architecture)
- **Database:** SQLite (Used to master migrations, schema evolution, and ORM queries)
- **Frontend:** Responsive HTML5 / CSS3 via Django Template Language

---
