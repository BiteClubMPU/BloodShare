# 🌍 BloodShare – Urgent Donation Network API

[![API Status](https://img.shields.io/badge/API-In%20Development-orange)](#)
[![ESL Capstone](https://img.shields.io/badge/ESL-Capstone%20Project-blue)](#)

## 📝 Project Overview

Hospitals and blood banks lack real-time visibility into blood shortages, so patients wait while staff search for donors by phone. Hospital staff and registered donors experience this delay daily: hospitals cannot reach matching donors quickly, and donors rarely hear about urgent needs in their own city zone. BloodShare's RESTful API tracks inventory shortages in real time and sends instant alerts to registered donors who have the matching blood type and live in the same city zone.

---

## ⚙️ Tech Stack & Prerequisites
To run this application locally, ensure your machine meets the minimum version constraints outlined below:

*   **Language & Runtime:** Python 3.11.5
*   **Web Framework:** FastAPI v0.100.0
*   **Database:** PostgreSQL v15.3
*   **Production Dependencies:**
    *   `fastapi` (^0.100.0) - Handles HTTP routing and automatic API documentation.
    *   `uvicorn` (^0.23.0) - Runs the ASGI web server.
    *   `sqlalchemy` (^2.0.0) - Maps Python models to database tables.
    *   `psycopg2-binary` (^2.9.6) - Connects the application to the PostgreSQL database.
    *   `alembic` (^1.11.0) - Manages database schema migrations.
    *   `pydantic` (^2.0.0) - Validates request payloads (for example, blood types).
    *   `python-dotenv` (^1.0.0) - Loads environment variables from the `.env` file.

---

## 🚀 Installation & Setup

Follow these precise steps to provision your local development environment:

1. **Clone** the remote repository from GitHub:
   ```bash
   git clone https://github.com/BiteClubMPU/BloodShare.git
   cd bloodshare
   ```

2. **Create** and **activate** a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install** all required production and development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure** your environment variables by copying the template file:
   ```bash
   cp .env.example .env
   ```
   *(Open the newly created `.env` file and insert your local database credentials).*

5. **Initialize** the database schema migrations:
   ```bash
   alembic upgrade head
   ```

6. **Start** the local development server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Open** the interactive API documentation in your browser:
   ```
   http://127.0.0.1:8000/docs
   ```

---

## 📖 API Reference Guide
All request payloads and response bodies must strictly communicate via valid JSON.

| HTTP Method | URL Path | Required JSON Payload Keys | Expected Status | Description / Purpose |
| :--- | :--- | :--- | :---: | :--- |
| `GET` | `/inventory/shortages` | None (optional query: `blood_type`, `zone_id`, `urgency`) | `200 OK` | Retrieves a filtered list of current blood shortages. |
| `POST` | `/inventory/shortages` | `{"hospital_id": "number", "blood_type": "string", "units_needed": "number", "urgency": "string"}` | `201 Created` | Creates a new shortage request from a hospital. |
| `PUT` | `/inventory/{blood_bank_id}` | `{"blood_type": "string", "units_available": "number"}` | `200 OK` | Updates the stock level of a blood type in a blood bank. |
| `POST` | `/alerts/send` | `{"shortage_request_id": "number", "channel": "string"}` | `202 Accepted` | Triggers notifications to matching donors in the same city zone. |
| `GET` | `/alerts/{id}` | None | `200 OK` | Retrieves the status of a single alert. |
| `PATCH` | `/alerts/{id}` | `{"status": "string"}` | `200 OK` | Lets a donor accept or decline an alert. |
| `POST` | `/donors` | `{"full_name": "string", "email": "string", "blood_type": "string", "city_zone_id": "number"}` | `201 Created` | Registers a new donor. |
| `GET` | `/donors` | None (optional query: `blood_type`, `zone_id`, `available`) | `200 OK` | Searches registered donors by blood type and zone. |
| `PATCH` | `/donors/{id}` | `{"is_available": "boolean"}` | `200 OK` | Updates donor data or availability. |
| `GET` | `/zones` | None | `200 OK` | Lists all city zones. |

### 🛑 Standard Error Handling Response
When data validation fails or unexpected edge cases occur, the API guarantees a unified response schema:

```json
{
  "status": 400,
  "error": "Bad Request",
  "message": "Field 'blood_type' must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.",
  "timestamp": "2026-10-29T14:02:00Z"
}
```