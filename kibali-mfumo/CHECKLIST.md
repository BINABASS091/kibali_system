# Installation Checklist

Use this checklist to verify your system is properly set up and running.

## Pre-Installation

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Node.js 16+ installed: `node --version`
- [ ] npm installed: `npm --version`
- [ ] PostgreSQL available: `brew services list`
- [ ] Git available (optional): `git --version`
- [ ] Sufficient disk space: ~500 MB

## PostgreSQL Setup

- [ ] PostgreSQL service running: `brew services list`
- [ ] Database created: `kibali_db`
- [ ] Database user created: `postgres`
- [ ] Password set correctly for database user
- [ ] Database connection working: `psql -U postgres -d kibali_db`

## Backend Setup

- [ ] Project directory copied/accessed: `/Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/backend`
- [ ] Virtual environment created: `venv/` exists
- [ ] Virtual environment activated: `(venv)` shows in terminal
- [ ] Requirements installed: No errors from `pip install -r requirements.txt`
- [ ] Migrations applied: `python manage.py migrate` succeeded
- [ ] Admin user created: `python manage.py createsuperuser` completed
- [ ] Officer test user created: `python manage.py shell` commands executed
- [ ] Backend server starts: `python manage.py runserver` works
- [ ] Backend accessible: `http://localhost:8000` shows Django welcome page
- [ ] Admin panel works: `http://localhost:8000/admin` shows login

## Frontend Setup

- [ ] Project directory accessed: `/Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/frontend`
- [ ] package.json exists: Can be read
- [ ] Dependencies installed: `node_modules/` folder exists
- [ ] No installation errors: `npm install` completed successfully
- [ ] Vite config correct: `vite.config.js` present
- [ ] Frontend server starts: `npm run dev` succeeds
- [ ] Frontend accessible: `http://localhost:5173` shows login page
- [ ] No console errors: Browser DevTools (F12) shows no errors

## Functional Tests

### Login Test
- [ ] Can access login page: `http://localhost:5173`
- [ ] Can login as officer: username: `officer1`, password: `officer123`
- [ ] Redirected to dashboard after login
- [ ] User name displayed: Shows "Karibu, officer1"
- [ ] Token stored: localStorage has `access_token`

### Permit Creation Test
- [ ] Can access create permit form: Click "Unda Kibali Kipya" button
- [ ] All form fields visible and editable
- [ ] Can fill all required fields
- [ ] Form submits without errors
- [ ] Permit created with auto-generated number: KU-0001
- [ ] Redirected to dashboard
- [ ] New permit visible in list

### PDF Generation Test
- [ ] PDF file created: `backend/media/permits/KU-0001.pdf` exists
- [ ] PDF can be downloaded: Click download button
- [ ] PDF opens correctly: Shows government permit format
- [ ] PDF contains all permit data
- [ ] PDF has official styling: Gold border, Swahili text

### Admin Features Test
- [ ] Login as admin user
- [ ] Can see all permits (not just own)
- [ ] Access Django admin: `http://localhost:8000/admin`
- [ ] Can see users and permits in admin panel

## Common Issues Resolved

- [ ] "Connection refused" error: PostgreSQL was started
- [ ] "No module named django": Virtual environment activated and deps installed
- [ ] "Port 8000 in use": Django running on different port or process killed
- [ ] "npm command not found": Node.js properly installed and in PATH
- [ ] "CORS error": Backend CORS settings include frontend URL
- [ ] "PDF not generating": WeasyPrint and system dependencies installed
- [ ] "Token invalid": Page reloaded and token re-obtained from login

## Performance Verification

- [ ] Frontend loads in <3 seconds
- [ ] Dashboard loads permits in <1 second
- [ ] Creating permit takes <5 seconds (including PDF generation)
- [ ] PDF downloads successfully
- [ ] No memory leaks: RAM usage stable
- [ ] No console errors: DevTools clean

## Security Verification

- [ ] Passwords not visible in browser console
- [ ] JWT token stored in localStorage (not in cookies by default)
- [ ] API requires authentication: Endpoints return 401 without token
- [ ] Officer can't access other officer's permits
- [ ] Officer can't access admin endpoints

## Database Verification

- [ ] Tables exist: `kibali_app_kibaliuser`, `kibali_app_permit`, `auth_user`
- [ ] Test permit record exists in database
- [ ] User roles assigned correctly
- [ ] Permit numbers auto-increment: KU-0001, KU-0002, etc.
- [ ] Dates auto-set correctly

## Documentation Verification

- [ ] README.md is comprehensive
- [ ] SETUP.md covers quick start
- [ ] ARCHITECTURE.md explains system design
- [ ] QUICK_REFERENCE.md provides commands
- [ ] API endpoints documented
- [ ] All code is readable with comments where needed

## Deployment Readiness (Optional)

- [ ] SECRET_KEY changed in settings.py
- [ ] DEBUG set to False for testing
- [ ] ALLOWED_HOSTS configured
- [ ] Environment variables set up
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Production database configured
- [ ] Error logging configured
- [ ] Backups strategy planned

## Sign-Off

- [ ] **System Owner:** _________________ Date: _______
- [ ] **Tested By:** _________________ Date: _______
- [ ] **Approval:** _________________ Date: _______

**Notes:**
```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

## Quick Status Check (Copy & Paste)

If everything is set up, you should be able to run these commands without errors:

```bash
# Terminal 1 - Backend Status
cd backend
source venv/bin/activate
python manage.py runserver
# Should show: Starting development server at http://127.0.0.1:8000/

# Terminal 2 - Frontend Status (in new terminal)
cd frontend
npm run dev
# Should show: ➜  Local:   http://localhost:5173/

# Terminal 3 - Database Status (in new terminal)
psql -U postgres -d kibali_db -c "SELECT COUNT(*) FROM kibali_app_permit;"
# Should show: (1 row) with count of permits

# Browser Test
# Visit http://localhost:5173
# Login with: officer1 / officer123
# Should see: Dashboard with permit list and create button
```

If all three show proper output, your system is ✅ **READY TO GO!**
