# 📧 TaskMailer – Django Email Scheduler

TaskMailer is a Django-based backend application that allows users to register using email & OTP verification, upload profile pictures to AWS S3, and schedule emails to be sent at a specific future time using Celery and Redis.

---

## 🚀 Features

- 🔐 User Registration with Email & OTP Verification
- 🔑 JWT Authentication (Login/Logout)
- 🖼️ Upload Profile Picture to AWS S3
- 📅 Schedule Emails for Future Delivery
- 📬 Celery Task Queue + Redis for Asynchronous Sending
- 🗂️ API Documentation via Swagger
- 🐳 Fully Dockerized (PostgreSQL + Redis + Celery + Django)

---

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** Simple JWT, OTP via Email
- **Task Queue:** Celery + Redis
- **Database:** PostgreSQL
- **File Storage:** AWS S3
- **Containerization:** Docker & Docker Compose
- **API Docs:** drf-yasg (Swagger)

---

## 📂 Project Structure

TaskMailer/
├── users/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── utils/
├── templates/
│ ├── index.html
│ ├── register.html
│ ├── dashboard.html
│ ├── schedule-email.html
│ └── view-emails.html
├── celery.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/TaskMailer.git
cd TaskMailer
### 2. Create a .env file with the following:
SECRET_KEY=your-django-secret
DEBUG=True

# PostgreSQL
POSTGRES_DB=taskmailer
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
###  Build & Run with Docker
docker-compose up --build
| Method | Endpoint              | Description                |
| ------ | --------------------- | -------------------------- |
| POST   | `/api/register/`      | Register with email        |
| POST   | `/api/verify-otp/`    | Verify OTP                 |
| POST   | `/api/token/`         | Login and get tokens       |
| POST   | `/api/token/refresh/` | Refresh JWT token          |
| POST   | `/api/logout/`        | Logout and blacklist token |
| Method | Endpoint                   | Description                  |
| ------ | -------------------------- | ---------------------------- |
| PUT    | `/api/update-profile-pic/` | Upload profile picture to S3 |
| Method | Endpoint                      | Description              |
| ------ | ----------------------------- | ------------------------ |
| GET    | `/api/scheduled-emails/`      | List scheduled emails    |
| POST   | `/api/scheduled-emails/`      | Schedule a new email     |
| PUT    | `/api/scheduled-emails/<id>/` | Update a scheduled email |
| DELETE | `/api/scheduled-emails/<id>/` | Delete a scheduled email |
