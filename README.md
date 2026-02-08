# 🎯 HPCL Lead Intelligence System

> AI-Powered B2B Lead Discovery Platform for HPCL Direct Sales & Bulk Fuels Division

An intelligent lead generation system that automatically discovers high-quality industrial fuel leads, infers product requirements using NLP, and delivers actionable insights with real-time email notifications.

![HPCL Lead Intelligence](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/React-18.x-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Natural Language Processing** - Extracts company information and detects purchase intent from unstructured text
- **Smart Product Recommendation** - ML models infer which HPCL products (FO, HSD, Bitumen, etc.) companies need
- **Lead Scoring** - Assigns priority scores (0-100) based on intent strength, urgency, and company profile

### 🔍 Automated Lead Discovery
- **Real-Time Web Scraping** - Monitors news, tenders, and business announcements 24/7
- **RSS Feed Integration** - Pulls real data from Economic Times, Business Standard, PIB, MoneyControl
- **Multi-Source Aggregation** - Combines signals from multiple sources for comprehensive coverage

### 📧 Instant Notifications
- **Email Alerts** - Sends beautiful HTML emails to territory sales officers
- **Complete Dossiers** - Includes company info, recommended products, signal context, and detected keywords
- **Territory Routing** - Automatically assigns leads to correct DSRO based on location

### 📊 Analytics Dashboard
- **Lead Management** - Track, filter, and manage all leads in one place
- **Product Distribution** - Visualize which products have the most opportunities
- **Territory Performance** - Monitor lead volume and conversion rates by region
- **Conversion Tracking** - Follow leads through the sales pipeline

### 🛡️ Enterprise Features
- **Dark Mode** - Professional UI with light/dark theme toggle
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **RESTful API** - Clean, documented API for integrations
- **Scalable Architecture** - Built to handle thousands of leads

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **spaCy** - Industrial-strength NLP
- **BeautifulSoup4** - Web scraping
- **FuzzyWuzzy** - Fuzzy string matching
- **Loguru** - Elegant logging
- **Pydantic** - Data validation
- **SMTP (Gmail)** - Email notifications

### Frontend
- **React 18** - UI library
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching/caching
- **Recharts** - Data visualization
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client

### Database
- **SQLite** - Lightweight SQL database (production: PostgreSQL recommended)

### AI/ML
- **spaCy NLP Models** - Named entity recognition, keyword extraction
- **Custom ML Pipeline** - Product inference, lead scoring algorithms
- **FuzzyWuzzy** - Company name matching

---

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     WEB SOURCES                              │
│  Economic Times | Business Standard | PIB | MoneyControl    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  SCRAPING LAYER                              │
│  • RSS Feed Scraper (Real Data)                             │
│  • Demo Scrapers (GeM Tenders, ET News)                     │
│  • Robots.txt Compliance & Rate Limiting                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  AI/ML PROCESSING                            │
│  • NLP: Extract company, keywords, intent                   │
│  • Product Inference: Bitumen, FO, HSD, etc.                │
│  • Lead Scoring: 0-100 based on signals                     │
│  • Company Matching: Fuzzy matching to database             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND API (FastAPI)                       │
│  • RESTful endpoints                                         │
│  • Database operations (SQLAlchemy)                          │
│  • Email service (SMTP)                                      │
│  • Analytics aggregation                                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND (React + Tailwind)                     │
│  • Dashboard with KPIs                                       │
│  • Lead management table                                     │
│  • Detailed lead dossiers                                    │
│  • Analytics & charts                                        │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                 NOTIFICATIONS                                │
│  Gmail alerts to territory sales officers                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hpcl-lead-intelligence.git
cd hpcl-lead-intelligence
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment template
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Mac/Linux

# Edit .env and add your credentials:
# - SMTP_USER=your-gmail@gmail.com
# - SMTP_PASSWORD=your-app-password

# Initialize database
python setup_database.py

# Populate demo data
python populate_demo.py

# Start backend server
python run.py
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## 💻 Usage

### Start the System

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
- **API Base:** http://localhost:8000/api

### Run Lead Scraper
```bash
cd backend
venv\Scripts\activate
python -m app.services.scraper_scheduler
```

This will:
1. Scrape real RSS feeds (Economic Times, Business Standard, etc.)
2. Generate demo tender data
3. Process all signals through AI/ML pipeline
4. Create leads in database
5. Send email notifications to sales officers

---

## 📚 API Documentation

### Get All Leads
```http
GET /api/leads/
```

**Response:**
```json
[
  {
    "id": 1,
    "company_name": "Reliance Industries Ltd",
    "lead_score": 76.0,
    "intent_strength": "high",
    "status": "new",
    "recommended_products": [
      {
        "product": "Bitumen",
        "confidence": 0.8,
        "reason": "Road construction project mentioned"
      }
    ],
    "signal_text": "Reliance announces new highway project...",
    "created_at": "2026-02-08T10:30:00"
  }
]
```

### Get Lead Details
```http
GET /api/leads/{lead_id}
```

### Get Analytics
```http
GET /api/analytics/
```

**Returns:**
- Product distribution
- Territory stats
- Conversion rates

### Get Summary Stats
```http
GET /api/stats/summary
```

**Full API documentation available at:** `http://localhost:8000/docs`

---

## 🌐 Deployment

### Backend Deployment (Render.com)

1. Create account on [Render.com](https://render.com)
2. Create new **Web Service**
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** Add all from `.env`
5. Deploy

### Frontend Deployment (Vercel)

1. Create account on [Vercel](https://vercel.com)
2. Import GitHub repository
3. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Add environment variable:
   - `VITE_API_URL=https://your-backend.onrender.com`
5. Deploy

---

## 📸 Screenshots

### Landing Page
![Landing Page](docs/landing-page.png)

### Dashboard
![Dashboard](docs/dashboard.png)

### Lead Detail
![Lead Detail](docs/lead-detail.png)

### Email Notification
![Email](docs/email-notification.png)

---

## 🗂️ Project Structure
```
hpcl-lead-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── models/           # Database models & schemas
│   │   ├── services/         # Business logic
│   │   ├── scrapers/         # Web scraping modules
│   │   ├── ml/              # AI/ML inference engine
│   │   └── config/          # Configuration
│   ├── tests/               # Unit tests
│   ├── requirements.txt
│   ├── run.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── assets/          # Static assets
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **HPCL Direct Sales Division** - For the opportunity and requirements
- **Anthropic Claude** - AI assistance in development
- **FastAPI Community** - Excellent documentation
- **React Team** - Amazing frontend framework

---

## 📞 Support

For support, email support@hpcl.co.in or open an issue in this repository.

---

## 🎯 Roadmap

- [x] Core lead discovery engine
- [x] Email notifications
- [x] Analytics dashboard
- [x] Dark mode
- [ ] Real GeM API integration (requires credentials)
- [ ] Advanced ML models for better product inference
- [ ] Mobile app (React Native)
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] WhatsApp notifications
- [ ] Multi-language support

---

**Built with ❤️ for HPCL Direct Sales**