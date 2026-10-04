# K12 Hunar Scholarship Management CRM

A simple Scholarship Management CRM built as part of the **K12 Hunar Frontend Developer Assessment**. It allows employees to view, filter, create, edit, update, and preview state scholarship records across Bihar, Haryana, and Jharkhand through a server-rendered Flask interface.

---

## Live Demo & Repository

- **Live Demo**: [Add deployed URL]
- **Source Code**: https://github.com/24f2008062/k12-scholarship-crm-frontend

---

## Features

- **Dashboard Summary Cards**: Displays real-time counts for Total Programs, Published, Draft, and Expired scholarships calculated dynamically from the SQLite database.
- **State Filtering**: Filter scholarship programs by state (Bihar, Haryana, Jharkhand, or All States).
- **Status Filtering**: Filter by lifecycle status (Published, Draft, Expired, or All Statuses), with support for combined state and status queries.
- **Scholarship Table Listing**: High-density table displaying scholarship titles, provider departments, target classes, deadlines, and current status badges.
- **Inline Status Updates**: Change a scholarship's status directly from the dashboard row using a compact form without needing to enter the full edit page.
- **Add Scholarship**: Form to register new scholarship programs with server-side validation for required fields, state/status allowlists, and valid URL formats.
- **Edit Scholarship**: Unified form pre-populated with existing scholarship data.
- **Student-Facing Preview**: Dedicated preview screen simulating how a scholarship appears to students, highlighting target class, application deadlines, financial benefits, eligibility criteria, and a direct application link.
- **Responsive Layout**: Mobile-friendly layout using Bootstrap 5, including collapsible cards and horizontally scrollable tables.
- **User Feedback & Error Handling**: Clear flash alerts for CRUD actions, friendly validation error messages, and a custom 404 page for missing records.

---

## Tech Stack

- **Language**: Python 3
- **Web Framework**: Flask
- **ORM & Database**: Flask-SQLAlchemy (SQLite)
- **Templating Engine**: Jinja2
- **Frontend / Styling**: HTML5, CSS3, Bootstrap 5 (via CDN)

---

## Project Structure

```text
k12-scholarship-crm/
│
├── app.py                     # Flask routes, form validation, and startup init
├── models.py                  # SQLAlchemy Scholarship model and constants
├── seed.py                    # 9 assessment scholarship records and seed script
├── tests.py                   # Automated unit and integration tests
├── requirements.txt           # Python package dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules for Python & SQLite
│
├── instance/
│   └── scholarships.db        # SQLite database file (created automatically)
│
├── templates/
│   ├── base.html              # Base layout with navbar, alerts, and footer
│   ├── dashboard.html         # Main dashboard with stats, filters, and table
│   ├── scholarship_form.html  # Unified Add and Edit form template
│   ├── preview.html           # Student-facing scholarship preview
│   └── 404.html               # Custom 404 error page
│
└── static/
    └── css/
        └── style.css          # Custom CRM styling and responsive layout tweaks
```

---

## Getting Started

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone the Repository
```bash
git clone <repository-url>
cd k12-scholarship-crm
```

### 2. Set Up a Virtual Environment
- **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

> **Note**: Database tables and the initial 9 assessment scholarship records are created and seeded automatically on first run.

---

## Running Tests

An automated test suite is included to verify initial data seeding, filtering, CRUD operations, inline status updates, preview rendering, and 404 handling:

```bash
python3 -m unittest -v tests.py
```

---

## Assessment Seed Data

The database initializes with the 9 sample scholarship programs specified in the assessment:

1. **Bihar** — Post-Matric Scholarship BC EBC (Class 11-12, Deadline: 30 Sep 2026, Status: Published)
2. **Bihar** — Post-Matric Scholarship SC ST (Class 11-12, Deadline: 30 Sep 2026, Status: Draft)
3. **Bihar** — Mukhyamantri Balak Balika Protsahan Yojana (Class 9-10, Deadline: Not stated, Status: Expired)
4. **Haryana** — Pre-Matric Scholarship for SC Students (Class 9-10, Deadline: 31 Dec 2026, Status: Published)
5. **Haryana** — Pre-Matric Scholarship for BC Students (Class 9-10, Deadline: 31 Dec 2026, Status: Draft)
6. **Haryana** — Post-Matric Scholarship for SC Students (Class 11-12, Deadline: 31 Dec 2026, Status: Expired)
7. **Jharkhand** — Pre-Matric Scholarship for SC Students (Class 1-10, Deadline: 20 Nov 2026, Status: Published)
8. **Jharkhand** — Pre-Matric Scholarship for ST Students (Class 1-10, Deadline: 20 Nov 2026, Status: Draft)
9. **Jharkhand** — Pre-Matric Scholarship for BC OBC Students (Class 1-10, Deadline: 20 Nov 2026, Status: Expired)

---

## Key Design Decisions

- **Server-Rendered Architecture**: Using Flask and Jinja2 keeps the application straightforward, avoids client-side state synchronization issues, and allows clean Post/Redirect/Get workflows.
- **SQLite Database**: SQLite requires zero external database installation, making it simple for evaluators to clone and run the project locally.
- **Query Parameter Filtering**: Filter state is managed via standard URL query parameters (`?state=Bihar&status=Published`), keeping filter views bookmarkable and persistent across page reloads without frontend state management.
- **Focused Scope**: User authentication, role permissions, and complex API layers were intentionally omitted to keep the codebase clean, stable, and focused on the core assessment goals.

---

## AI Tools & References Used

AI tools were used for brainstorming UI layouts, implementation assistance, and test case generation. All submitted code has been reviewed, tested, and understood.
