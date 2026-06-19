# Maverick Certification Hub

## 1. Introduction

**Maverick Certification Hub** is an end-to-end automation platform built to manage MAP (Maverick Assessment Program) Certification Drives at Hexaware Technologies. It replaces fragmented, manual processes with a centralized, auditable, and streamlined system.

The platform covers the entire certification lifecycle:

- **Drive Creation** — Set up certification drives with budget, timelines, pass thresholds, and policies
- **Candidate Registration** — Single or bulk CSV registration with duplicate prevention
- **Eligibility Evaluation** — Configurable rules engine (tenure, training, attempt limits, budget) with approval workflows
- **Assessment Results** — Import scores (single or bulk), automatic pass/fail determination based on drive threshold
- **Voucher Management** — Secure voucher pool, one-click auto-allocation to passed candidates, revoke/reissue, redemption tracking
- **Reporting & Analytics** — Funnel visualization, pass/fail trends by track, voucher utilization charts, CSV export
- **Audit Trail** — Immutable, append-only log of every action with before/after JSON snapshots
- **Simulated Communications** — Event-triggered notifications (registration ack, eligibility decisions, result notifications, voucher issuance) logged for demo purposes


## 2. Functionality Overview

### Admin Persona
- Create, edit, close, and delete certification drives
- Register candidates (single form or bulk CSV import)
- Run eligibility evaluation (rules engine) — approve or reject candidates
- Import assessment results — automatic pass/fail scoring
- Manage voucher pool — add vouchers, auto-allocate, revoke, reissue, mark redeemed
- View reports with charts (funnel, pass/fail by track, voucher utilization pie)
- Full audit log with filters and expandable before/after diff

### User Persona
- View drives and their details
- View registrations (read-only)
- View eligibility decisions (read-only)
- View assessment results (read-only)
- View reports and analytics
- Cannot access: Voucher Management, Audit Log

---

## 3. Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Python + FastAPI | 3.10+ / 0.115 |
| Frontend | React + Vite | 18.3 / 5.4 |
| Styling | Tailwind CSS + Ant Design | 3.4 / 5.24 |
| Charts | Recharts | 2.15 |
| HTTP Client | Axios | 1.9 |
| Routing | React Router | 7.6 |
| Icons | React Icons (Remix) | 5.5 |

---

## 4. Project Structure

```
Maverick-Certification-Hub/
├── backend/
│   ├── app.py                    # FastAPI entry point (port 8016)
│   ├── seed_data.py              # Dummy data seeder script
│   ├── requirements.txt          # Python dependencies
│   ├── data/                     # JSON data files (auto-managed)
│   │   ├── users.json
│   │   ├── drives.json
│   │   ├── registrations.json
│   │   ├── eligibility.json
│   │   ├── results.json
│   │   ├── vouchers.json
│   │   ├── audit_logs.json
│   │   ├── communications.json
│   │   └── templates.json
│   ├── uploads/                  # Drive-specific file storage
│   └── modules/
│       ├── api_routes/           # Route handlers (9 files)
│       ├── api_modules/          # Business logic (7 files)
│       └── service_modules/      # FileManager, HelperFunctions
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx               # Route definitions
│       ├── main.jsx              # Entry point
│       ├── index.css             # Global styles + animations
│       ├── assets/               # Background.png
│       ├── pages/                # Login, DrivesDashboard, CreateDrive
│       ├── components/           # 7 feature components
│       ├── layout/               # Layout (TopBar + Sidebar + Outlet)
│       ├── utils/                # TopBar, Sidebar
│       └── config/api/           # ApiUrls, apiConfig (Axios)
│
├── requirements.txt              # Root-level Python deps
├── readme.md                     # This file
├── TASKS.md                      # Detailed task breakdown
└── .gitignore
```

---

## 5. Local Setup (Step-by-Step)

### Prerequisites

Make sure you have these installed on your machine:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Git** — [Download](https://git-scm.com/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/maverick-certification-hub.git
cd maverick-certification-hub
```

### Step 2: Set Up the Backend

```bash
# Navigate to backend
cd backend

# (Optional) Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Seed Dummy Data

```bash
# Still inside the backend/ folder
python seed_data.py
```

This populates all JSON data files with realistic dummy records:
- 3 certification drives
- 35 candidate registrations
- 28 eligibility evaluations
- 17 assessment results
- 18 vouchers (with allocations and redemptions)
- 16 audit log entries
- 92 communication records

### Step 4: Start the Backend Server

```bash
# Still inside the backend/ folder
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8016 --reload
```

The API will be running at: **http://localhost:8016**

Verify by opening: http://localhost:8016/api/health

You should see:
```json
{"status": "ok", "version": "1.0.0"}
```

### Step 5: Set Up the Frontend

Open a **new terminal** window:

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install
```

### Step 6: Start the Frontend Dev Server

```bash
# Still inside the frontend/ folder
npm run dev
```

The app will be running at: **http://localhost:5173**

### Step 7: Use the Application

1. Open http://localhost:5173 in your browser
2. Click **"Login as Admin"** for full access, or **"Login as User"** for read-only access
3. You'll see the Drives Dashboard with 3 pre-seeded certification drives
4. Click any drive to explore: Registrations → Eligibility → Results → Vouchers → Reports → Audit

---

## 6. Quick Commands Reference

| Action | Command |
|--------|---------|
| Start backend | `cd backend && python -m uvicorn app:app --port 8016 --reload` |
| Start frontend | `cd frontend && npm run dev` |
| Re-seed data | `cd backend && python seed_data.py` |
| Build frontend | `cd frontend && npm run build` |
| Install backend deps | `cd backend && pip install -r requirements.txt` |
| Install frontend deps | `cd frontend && npm install` |

---

## 7. Notes

- **No database required** — All data is stored as JSON files in `backend/data/`. Delete these files and re-run `seed_data.py` to reset.
- **No authentication** — Login buttons simply set the user context in localStorage. No JWT, cookies, or tokens.
- **No real emails** — Communication events are logged to `communications.json` as if they were sent.
- **Voucher codes are masked** — The backend never sends full voucher codes to the frontend (only `****-****-XXXX`).
- **Audit trail is immutable** — There is no API to delete or modify audit log entries.
- **File uploads** — Uploaded CSV files and evidence documents are saved to `backend/uploads/{drive_id}/`.

---

## 8. Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend port 8016 already in use | Kill the process: `taskkill /F /PID <pid>` or change port in `app.py` |
| Frontend can't connect to backend | Ensure backend is running on port 8016. Check CORS in `app.py` |
| Charts show "No data" | Run `python seed_data.py` to populate data, then refresh |
| npm install fails | Delete `node_modules` and `package-lock.json`, then run `npm install` again |
| Python module not found | Ensure you're running from the `backend/` directory |

---

## 9. Team

Built for the **Designathon 2026** — MAP Certification Drive Automation challenge.

