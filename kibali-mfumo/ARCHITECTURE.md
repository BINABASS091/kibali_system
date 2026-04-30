# Project Architecture & Features

## System Overview

Kibali cha Ujenzi is a government building permit management system built with:

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend                         │
│           (Vite, Axios, React Router)                    │
│         Running on http://localhost:5173                 │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/REST
                   │ JSON (JWT Auth)
┌──────────────────▼──────────────────────────────────────┐
│              Django REST API                             │
│    (Django, DRF, JWT, WeasyPrint)                        │
│      Running on http://localhost:8000                    │
└──────────────────┬──────────────────────────────────────┘
                   │ SQL Queries
┌──────────────────▼──────────────────────────────────────┐
│              PostgreSQL Database                         │
│        (kibali_db - Users, Permits, etc.)               │
└─────────────────────────────────────────────────────────┘
```

## Core Features

### 1. Authentication System
- **JWT-based authentication** for secure API access
- **Two user roles:**
  - Admin: Can view all permits in the system
  - Officer: Can create permits and view their own

**Login Flow:**
```
User Login (username/password)
    ↓
Django Backend validates credentials
    ↓
Generate JWT token (valid for 24 hours)
    ↓
Return token to frontend
    ↓
Frontend stores token in localStorage
    ↓
All API requests include token in Authorization header
```

### 2. Permit Management

**Permit Creation:**
- Officers fill in permit form with applicant details
- Auto-generated permit number (KU-0001, KU-0002, etc.)
- Auto-set issue date (today)
- System generates government-style PDF

**Permit Fields:**
1. **Applicant Info**
   - Jina (Applicant name)
   - Email (optional)

2. **Construction Details**
   - Aina (Type: UKUTA, NYUMBA, JENGO, KIWANDA, DUKA, OFISI)
   - Pahala (Location)
   - Shehia (Ward/Parish)

3. **Land Boundaries**
   - Kaskazini (North)
   - Mashariki (East)
   - Magharibi (West)
   - Kusini (South)

4. **Measurements**
   - Upana (Width in meters)
   - Urefu (Height/Length in meters)

5. **Dates**
   - Tarehe Kutolewa (Issue date) - Auto-set to today
   - Tarehe Mwisho (Expiry date) - User selects

### 3. PDF Generation

**WeasyPrint Process:**
```
Permit Form Data
    ↓
Django renders HTML template with permit data
    ↓
WeasyPrint converts HTML → PDF
    ↓
PDF saved to /backend/media/permits/
    ↓
User can download from dashboard
```

**PDF Includes:**
- Official government header
- Permit number and date
- All permit details in structured layout
- Land boundaries in 2x2 grid
- Signature section
- Gold-colored border
- Swahili text throughout

### 4. Database Schema

**Users Table:**
```
User (Django's built-in)
├── id (primary key)
├── username
├── password (hashed)
├── email
├── first_name
└── last_name

KibaliUser (Custom model)
├── id (primary key)
├── user (FK to User)
├── role (admin/officer)
└── created_at
```

**Permits Table:**
```
Permit
├── id (primary key)
├── permit_number (unique, auto-generated)
├── created_by (FK to User)
├── jina
├── aina
├── pahala
├── shehia
├── kaskazini
├── mashariki
├── magharibi
├── kusini
├── upana
├── urefu
├── tarehe_kutolewa (auto-set)
├── tarehe_mwisho
├── pdf_file (path to generated PDF)
├── created_at
└── updated_at
```

## API Endpoints

### Authentication
```
POST /api/login/
Request:  { username, password }
Response: { access_token, user: { id, username, email, role } }
Status:   200 (success) or 401 (invalid credentials)
```

### Permit Creation
```
POST /api/permits/create/
Headers:  Authorization: Bearer {token}
Request:  {
  jina, aina, pahala, shehia,
  kaskazini, mashariki, magharibi, kusini,
  upana, urefu, tarehe_mwisho
}
Response: { id, permit_number, ... (full permit data) }
Status:   201 (created) or 400 (validation error)
```

### List Permits
```
GET /api/permits/
Headers:  Authorization: Bearer {token}
Response: [ { permit_object }, ... ]
Notes:    Admin sees all, Officer sees only their own
```

### Get Permit Detail
```
GET /api/permits/{permit_id}/
Headers:  Authorization: Bearer {token}
Response: { permit_object }
```

### Download Permit PDF
```
GET /api/permits/{permit_id}/download/
Headers:  Authorization: Bearer {token}
Response: PDF file
```

## Frontend Architecture

### Pages

**1. Login.jsx**
- Login form with username/password
- Stores JWT token in localStorage
- Redirects to dashboard on success

**2. Dashboard.jsx**
- Lists all permits (admin: all, officer: own)
- Shows permit details in table format
- Download PDF button for each permit
- Create new permit button
- Logout button

**3. CreatePermit.jsx**
- Multi-section form
- Validates all required fields
- Submits to backend
- Shows success/error messages
- Redirects to dashboard on success

### State Management
- Simple React hooks (useState, useEffect)
- localStorage for token persistence
- useNavigate for routing
- Protected routes (requires authentication)

### API Client
- Axios for HTTP requests
- Interceptors for JWT token injection
- Error handling and logging

## Backend Architecture

### Models
- **User** - Django's built-in user model
- **KibaliUser** - Extends User with role
- **Permit** - Building permit records

### Views (API Endpoints)
- `login_view()` - JWT authentication
- `create_permit()` - Create permit + generate PDF
- `list_permits()` - List permits
- `get_permit_detail()` - Get single permit
- `download_permit_pdf()` - Download PDF file

### Serializers
- `UserSerializer` - Serialize user data
- `KibaliUserSerializer` - Serialize role/user
- `PermitSerializer` - Serialize permit data
- `LoginSerializer` - Validate login input

### PDF Generation
- Template: `templates/permit.html`
- Engine: WeasyPrint
- Styling: CSS in HTML template
- Output: PDF files in `media/permits/`

## Security Features

1. **JWT Authentication**
   - Token-based, not session-based
   - 24-hour expiration
   - Secret key signing

2. **Role-based Access Control**
   - Admin: Full access
   - Officer: Limited access (own permits)

3. **CORS Protection**
   - Only whitelisted domains can access API
   - Credentials allowed

4. **Database Constraints**
   - Permit numbers are unique
   - Foreign key relationships enforced

## Data Flow Examples

### Creating a Permit
```
1. Officer fills form and clicks "Unda Kibali"
2. Frontend validates form data
3. Frontend sends POST to /api/permits/create/
4. Backend receives request (JWT verified)
5. Backend creates Permit record in database
6. Backend auto-generates permit number
7. Backend renders HTML template with permit data
8. Backend converts HTML to PDF using WeasyPrint
9. Backend saves PDF to media/permits/
10. Backend returns permit data + PDF URL to frontend
11. Frontend redirects to dashboard
12. Officer sees new permit in list
13. Officer can download PDF
```

### Logging In
```
1. User enters username/password in login form
2. Frontend validates input
3. Frontend sends POST to /api/login/
4. Backend validates credentials against database
5. Backend generates JWT token (valid 24 hours)
6. Backend returns token + user info
7. Frontend stores token in localStorage
8. Frontend stores user info in state
9. Frontend redirects to dashboard
10. All future API requests include token
```

### Viewing Permits
```
1. Officer lands on dashboard
2. Frontend checks if authenticated (token in localStorage)
3. Frontend sends GET to /api/permits/
4. Backend retrieves permits WHERE created_by = user_id
5. Backend returns list of officer's permits
6. Frontend displays permits in table
7. Officer can download individual PDFs
```

## Performance Considerations

1. **Database Indexing**
   - permit_number: unique index for fast lookup
   - created_by: foreign key index for filtering

2. **File Storage**
   - PDFs stored in /media/permits/ directory
   - Serve directly from Django in development
   - Use CDN or S3 in production

3. **API Response Times**
   - JWT validation: <5ms
   - Database query: <50ms (with proper indexes)
   - PDF generation: 1-3 seconds (can be optimized with async tasks)

4. **Frontend Performance**
   - React components are lightweight
   - Vite provides fast bundling
   - No external CSS framework (minimal dependencies)

## Scalability Improvements for Production

1. **Backend**
   - Use Celery for async PDF generation
   - Add caching (Redis) for permit list
   - Implement pagination for large datasets
   - Use Gunicorn/uWSGI for production server

2. **Frontend**
   - Code splitting for lazy loading
   - Image optimization
   - Service workers for offline support

3. **Database**
   - Connection pooling
   - Read replicas for scaling
   - Regular backups

4. **Deployment**
   - Docker containerization
   - Kubernetes orchestration
   - Load balancing
   - CDN for static assets

## Testing

To add tests in production:

**Backend:**
```bash
python manage.py test kibali_app
```

**Frontend:**
```bash
npm test
```

Add test files:
- `backend/kibali_app/tests.py` - Django tests
- `frontend/src/__tests__/` - React tests with Jest/Vitest
