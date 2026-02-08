# HPCL Lead Intelligence - Backend API

Backend API for HPCL B2B Lead Intelligence System built with FastAPI.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database (or use SQLite for testing)

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
```

2. **Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Configure environment**

Copy `.env.example` to `.env` and update:
```bash
copy .env.example .env
```

Edit `.env` file with your settings:
- For testing, use SQLite: `DATABASE_URL=sqlite:///./hpcl_leads.db`
- For production, use PostgreSQL from Supabase

6. **Setup database**
```bash
python setup_database.py
```

7. **Run the server**
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

## 📡 API Documentation

Once server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database Setup (Supabase - Free Tier)

1. Go to https://supabase.com
2. Create free account
3. Create new project
4. Get connection string from Settings → Database
5. Update `.env`:
```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

## 📧 Email Setup (Gmail)

1. Go to your Google Account → Security
2. Enable 2-Step Verification
3. Create App Password: https://myaccount.google.com/apppasswords
4. Update `.env`:
```
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

## 🧪 Testing

Access the API:
```bash
curl http://localhost:8000/
```

Get demo leads:
```bash
curl http://localhost:8000/api/leads/
```

## 📂 Project Structure
```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── config/       # Settings & database
│   ├── models/       # SQLAlchemy models & schemas
│   ├── services/     # Business logic
│   ├── scrapers/     # Web scraping
│   ├── ml/           # AI/ML inference
│   └── main.py       # FastAPI app
├── requirements.txt
└── setup_database.py
```

## 🔑 Key Features

✅ Lead intelligence from web signals  
✅ AI-powered product recommendations  
✅ Email notifications to sales officers  
✅ Complete REST API  
✅ Analytics dashboard data  

## 🛠️ Tech Stack

- FastAPI - Modern web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- spaCy - NLP
- BeautifulSoup - Web scraping
- Gmail SMTP - Email notifications