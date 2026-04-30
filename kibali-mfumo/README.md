# Kibali cha Ujenzi System

A complete building permit management system for the Zanzibar government. This is a full-stack web application built with Django REST Framework, React, and PostgreSQL.

## Project Structure

```
kibali-mfumo/
├── backend/                    # Django backend
│   ├── kibali_project/        # Django project settings
│   ├── kibali_app/            # Main Django application
│   ├── templates/             # HTML templates for PDF generation
│   ├── media/                 # Generated PDFs and uploads
│   ├── manage.py              # Django management script
│   └── requirements.txt        # Python dependencies
│
└── frontend/                  # React + Vite frontend
    ├── src/
    │   ├── pages/            # React pages
    │   ├── api.js            # API client
    │   ├── App.jsx           # Main App component
    │   └── main.jsx          # Entry point
    ├── index.html            # HTML entry point
    ├── package.json          # Node dependencies
    └── vite.config.js        # Vite configuration
```

## Features

- **JWT Authentication** - Secure login with JWT tokens
- **User Roles** - Admin and Officer roles with different permissions
- **Permit Management** - Create, view, and manage building permits
- **Auto-generated Permit Numbers** - Format: KU-0001, KU-0002, etc.
- **PDF Generation** - Generate official government-style permit PDFs
- **Responsive UI** - Clean, modern government-style interface in Swahili

## Technology Stack

**Backend:**
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL
- WeasyPrint (for PDF generation)
- JWT for authentication

**Frontend:**
- React 18.2.0
- Vite 5.0.8
- Axios (HTTP client)
- React Router (navigation)

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- pip (Python package manager)
- npm (Node package manager)

## Setup Instructions

### 1. Database Setup

First, create a PostgreSQL database:

```bash
# On macOS with Homebrew:
brew services start postgresql

# Connect to PostgreSQL
psql postgres

# In PostgreSQL shell:
CREATE DATABASE kibali_db;
CREATE USER postgres WITH PASSWORD 'password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO off;
ALTER ROLE postgres SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kibali_db TO postgres;
\q
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser

# When prompted:
# Username: admin
# Email: admin@kibali.go.tz
# Password: (choose a secure password)
# Password (again): (confirm)

# Create test user (Officer)
python manage.py shell
```

In the Django shell:

```python
from django.contrib.auth.models import User
from kibali_app.models import KibaliUser

# Create a test officer user
officer = User.objects.create_user(
    username='officer1',
    email='officer@kibali.go.tz',
    password='officer123'
)

# Assign officer role
KibaliUser.objects.create(user=officer, role='officer')

# Make admin user an admin
admin_user = User.objects.get(username='admin')
KibaliUser.objects.create(user=admin_user, role='admin')

exit()
```

### 3. Start Backend Server

```bash
# Make sure you're in backend directory and venv is activated
python manage.py runserver

# Backend will run on: http://localhost:8000
```

### 4. Frontend Setup

In a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will run on: http://localhost:5173
```

## Running the System

### Option 1: Local Development (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open your browser and go to: `http://localhost:5173`

### Option 2: Production Build

```bash
# Build frontend
cd frontend
npm run build

# This creates a dist/ folder with optimized production files
```

## Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: (password you set during superuser creation)

**Officer Account:**
- Username: `officer1`
- Password: `officer123`

## API Endpoints

### Authentication
- `POST /api/login/` - Login and get JWT token

### Permits
- `POST /api/permits/create/` - Create a new permit (requires JWT)
- `GET /api/permits/` - List permits (admin sees all, officer sees own)
- `GET /api/permits/<permit_id>/` - Get permit details
- `GET /api/permits/<permit_id>/download/` - Download permit PDF

## Using the System

### 1. Login
- Open http://localhost:5173
- Enter username and password
- Click "Ingia" (Login)

### 2. Create a Permit
- Click "Unda Kibali Kipya" (Create New Permit) button
- Fill in all required fields:
  - **Jina** - Applicant name
  - **Aina** - Type of construction
  - **Pahala** - Location
  - **Shehia** - Ward
  - **Land Boundaries** - North, East, West, South
  - **Measurements** - Width and Height in meters
  - **Tarehe ya Mwisho** - Expiry date
- Click "Unda Kibali" (Create Permit)
- System auto-generates:
  - Permit number (KU-0001, KU-0002, etc.)
  - Issue date (today's date)
  - PDF document

### 3. View Permits
- Dashboard shows list of all permits you created
- Click download button (↓ PDF) to get the permit as PDF
- PDFs are formatted as official government documents

### 4. Admin Features
- Admin users can see all permits in the system
- Access Django admin at: http://localhost:8000/admin

## Troubleshooting

### Issue: "Connection refused" when starting backend
**Solution:** Make sure PostgreSQL is running
```bash
brew services start postgresql  # macOS
```

### Issue: "No module named 'django'"
**Solution:** Activate virtual environment and install requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** Run Django on different port
```bash
python manage.py runserver 8001
```
Then update `API_BASE_URL` in `frontend/src/api.js`

### Issue: "Port 5173 already in use"
**Solution:** Run Vite on different port
```bash
npm run dev -- --port 5174
```

### Issue: PDF generation fails
**Solution:** Make sure WeasyPrint dependencies are installed
```bash
pip install WeasyPrint
# Also install system dependencies (macOS):
brew install cairo pango gdk-pixbuf libffi
```

## File Locations

- **Generated PDFs:** `backend/media/permits/`
- **Database:** PostgreSQL (kibali_db)
- **Django Admin:** http://localhost:8000/admin
- **Frontend:** http://localhost:5173

## Environment Variables

To use custom database credentials, create a `.env` file in the backend directory:

```
DB_NAME=kibali_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

Then update `settings.py` to use these variables.

## Security Notes

⚠️ **This is a development setup. For production:**

1. Change `SECRET_KEY` in `kibali_project/settings.py`
2. Set `DEBUG = False` in settings
3. Configure `ALLOWED_HOSTS` properly
4. Use environment variables for sensitive data
5. Configure HTTPS/SSL
6. Use a production database server
7. Deploy using gunicorn or similar

## Extending the System

### Adding New Fields to Permit
1. Update `Permit` model in `backend/kibali_app/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Update `PermitSerializer` in `serializers.py`
5. Update form in `frontend/src/pages/CreatePermit.jsx`
6. Update PDF template in `backend/templates/permit.html`

### Customizing PDF Layout
Edit `backend/templates/permit.html` to change:
- Header text and styling
- Permit fields layout
- Signature sections
- Colors and borders

## Support

For issues or questions, check:
1. Django logs in terminal running backend
2. Browser console (F12) for frontend errors
3. Database: `psql kibali_db -U postgres`

## License

This system is developed for the Zanzibar Government.
