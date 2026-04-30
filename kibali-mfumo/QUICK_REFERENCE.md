# Kibali cha Ujenzi - Quick Reference Guide

## File Structure

```
kibali-mfumo/
│
├── README.md                    # Main documentation
├── SETUP.md                     # Quick setup guide
├── ARCHITECTURE.md              # Technical architecture
├── API_ENDPOINTS.md             # API documentation
│
├── backend/                     # Django Backend
│   ├── manage.py               # Django management
│   ├── requirements.txt         # Python packages
│   │
│   ├── kibali_project/          # Django Project Config
│   │   ├── __init__.py
│   │   ├── settings.py          # Database, installed apps
│   │   ├── urls.py              # URL routing
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── kibali_app/              # Main Application
│   │   ├── __init__.py
│   │   ├── models.py            # KibaliUser, Permit models
│   │   ├── serializers.py       # API serializers
│   │   ├── views.py             # API views/endpoints
│   │   ├── urls.py              # App URLs
│   │   ├── admin.py             # Admin panel config
│   │   ├── apps.py
│   │   └── migrations/
│   │       └── 0001_initial.py  # Initial migration
│   │
│   ├── templates/
│   │   └── permit.html          # PDF template
│   │
│   ├── media/
│   │   └── permits/             # Generated PDFs
│   │
│   └── venv/                    # Virtual environment (created on setup)
│
└── frontend/                    # React + Vite
    ├── package.json             # Dependencies
    ├── vite.config.js           # Vite config
    ├── index.html               # HTML entry point
    │
    ├── src/
    │   ├── main.jsx             # React entry point
    │   ├── App.jsx              # Root component
    │   ├── App.css
    │   ├── index.css
    │   ├── api.js               # API client configuration
    │   │
    │   └── pages/               # Page components
    │       ├── Login.jsx         # Login page
    │       ├── Login.css
    │       ├── Dashboard.jsx     # Permit list
    │       ├── Dashboard.css
    │       ├── CreatePermit.jsx  # Form to create permit
    │       └── CreatePermit.css
    │
    ├── node_modules/            # Dependencies (created on setup)
    └── dist/                    # Production build (created on build)
```

## Key Database Tables

### User (Django Built-in)
| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary key |
| username | String | Unique |
| password | String | Hashed |
| email | String | Optional |
| first_name | String | Optional |
| last_name | String | Optional |

### KibaliUser (Custom)
| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary key |
| user_id | Integer | FK to User |
| role | String | 'admin' or 'officer' |
| created_at | DateTime | Auto-set |

### Permit
| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary key |
| permit_number | String | Format: KU-0001, Unique |
| created_by_id | Integer | FK to User |
| jina | String | Applicant name |
| aina | String | Type of construction |
| pahala | String | Location |
| shehia | String | Ward |
| kaskazini | String | North boundary |
| mashariki | String | East boundary |
| magharibi | String | West boundary |
| kusini | String | South boundary |
| upana | Float | Width in meters |
| urefu | Float | Height in meters |
| tarehe_kutolewa | Date | Issue date (auto today) |
| tarehe_mwisho | Date | Expiry date |
| pdf_file | String | Path to PDF file |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-update |

## API Quick Reference

### Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/login/ | No | Get JWT token |
| POST | /api/permits/create/ | Yes | Create new permit |
| GET | /api/permits/ | Yes | List permits |
| GET | /api/permits/{id}/ | Yes | Get permit detail |
| GET | /api/permits/{id}/download/ | Yes | Download PDF |

### Request/Response Examples

**Login:**
```json
Request:  POST /api/login/
{
  "username": "officer1",
  "password": "officer123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 2,
    "username": "officer1",
    "email": "officer@kibali.go.tz",
    "role": "officer"
  }
}
```

**Create Permit:**
```json
Request:  POST /api/permits/create/
Headers:  Authorization: Bearer {token}
{
  "jina": "John Doe",
  "aina": "NYUMBA",
  "pahala": "Dar es Salaam",
  "shehia": "Ilala",
  "kaskazini": "Road Street",
  "mashariki": "Building Complex",
  "magharibi": "Green Area",
  "kusini": "School",
  "upana": 50.5,
  "urefu": 80.25,
  "tarehe_mwisho": "2025-12-31"
}

Response: 201 Created
{
  "id": 1,
  "permit_number": "KU-0001",
  "created_by_username": "officer1",
  "jina": "John Doe",
  "aina": "NYUMBA",
  ... (all fields)
  "pdf_file": "permits/KU-0001.pdf"
}
```

## Common Commands

### Backend Commands
```bash
# Setup
python3 -m venv venv               # Create virtual env
source venv/bin/activate           # Activate venv
pip install -r requirements.txt    # Install dependencies
python manage.py migrate           # Run migrations
python manage.py createsuperuser   # Create admin user

# Running
python manage.py runserver         # Start dev server
python manage.py runserver 8001    # Use different port
python manage.py shell             # Django interactive shell

# Database
python manage.py makemigrations    # Create migration
python manage.py migrate           # Apply migration
python manage.py dumpdata > db.json    # Backup
python manage.py loaddata db.json      # Restore
```

### Frontend Commands
```bash
# Setup
npm install                        # Install dependencies
npm install package-name           # Add package

# Development
npm run dev                        # Start dev server
npm run preview                    # Preview production build

# Production
npm run build                      # Build for production
npm run build -- --watch           # Build with watch
```

### PostgreSQL Commands
```bash
# Connection
psql -U postgres                   # Connect as postgres
psql -U postgres -d kibali_db      # Connect to database

# Database
\l                                 # List databases
\dt                                # List tables
\d table_name                      # Describe table
CREATE DATABASE kibali_db;         # Create database
DROP DATABASE kibali_db;           # Delete database

# Users
\du                                # List users
CREATE USER user WITH PASSWORD 'pass';
DROP USER user;
```

## Login Credentials (Default)

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Officer | officer1 | officer123 | Own permits |
| Admin | admin | (you set) | All permits |

## Important Files to Modify

| Purpose | File | What to Change |
|---------|------|-----------------|
| Add permit field | models.py | Add field to Permit model |
| Add form field | CreatePermit.jsx | Add input to form |
| Update API | views.py | Add/modify endpoint |
| Customize PDF | permit.html | Change HTML/CSS styling |
| Change API URL | api.js | Update API_BASE_URL |
| Database config | settings.py | DATABASES section |

## Debugging Tips

```bash
# Backend
python manage.py shell             # Debug models
# In shell: from kibali_app.models import *

# Frontend
# Open browser DevTools (F12)
# Check Console tab for errors
# Check Network tab for API calls

# Database
psql -U postgres -d kibali_db
SELECT * FROM kibali_app_permit;   # View permits
SELECT * FROM kibali_app_kibaliuser; # View users
```

## Permission Rules

| Action | Officer | Admin |
|--------|---------|-------|
| Create Permit | ✅ | ✅ |
| View Own Permits | ✅ | ✅ |
| View All Permits | ❌ | ✅ |
| Download PDF | ✅ (own) | ✅ (any) |
| Access Django Admin | ❌ | ✅ |

## File Sizes (Approx)
- Backend code: ~15 KB
- Frontend code: ~80 KB (after build: ~50 KB minified)
- Generated PDF: ~100-200 KB per permit
- Database: Grows with permit count (~1 KB per permit record)

## Resource Requirements
- **RAM:** 512 MB minimum (1 GB recommended)
- **Storage:** 100 MB for code + dependencies
- **CPU:** Single core sufficient for development
- **Network:** API calls average <100ms

## Support Resources

1. **Django Docs:** https://docs.djangoproject.com/
2. **DRF Docs:** https://www.django-rest-framework.org/
3. **React Docs:** https://react.dev/
4. **PostgreSQL Docs:** https://www.postgresql.org/docs/
5. **WeasyPrint Docs:** https://weasyprint.org/

## Troubleshooting Checklist

- [ ] PostgreSQL is running? `brew services list`
- [ ] Virtual environment activated? `source venv/bin/activate`
- [ ] Dependencies installed? `pip install -r requirements.txt`
- [ ] Migrations applied? `python manage.py migrate`
- [ ] Frontend dependencies installed? `npm install`
- [ ] Correct ports? Backend: 8000, Frontend: 5173
- [ ] CORS allowed? Check settings.py
- [ ] JWT token valid? Check token in browser localStorage
