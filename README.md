# Commissions Tracker

A simple Django application for tracking commissions and client work.

## Features

- **Dashboard**: Overview of commission statistics and recent activity
- **Commission Management**: Track commission details, status, and client information
- **Search & Filter**: Find commissions by title, client, or status
- **Admin Interface**: Full CRUD operations through Django admin
- **Responsive Design**: Bootstrap-based UI that works on all devices

## Commission Fields

- Title and description
- Client name and email
- Commission amount
- Status (Pending, In Progress, Completed, Cancelled)
- Due date and completion date
- Notes
- Timestamps (created/updated)

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Load Sample Data** (optional):
   ```bash
   python create_sample_data.py
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver 0.0.0.0:12000
   ```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## URLs

- `/` - Dashboard
- `/commissions/` - Commission list
- `/commissions/<id>/` - Commission detail
- `/admin/` - Django admin interface

## Technology Stack

- Django 5.2.3
- SQLite (default database)
- Bootstrap 5.1.3
- Font Awesome 6.0.0

## Development

The application is structured with a single `commissions` app that handles all commission-related functionality. The models, views, and templates are organized following Django best practices.

### Project Structure

```
commissions_tracker/
├── commissions/           # Main app
│   ├── models.py         # Commission model
│   ├── views.py          # Views for dashboard and commission pages
│   ├── admin.py          # Admin configuration
│   ├── urls.py           # App URL patterns
│   └── templates/        # HTML templates
├── commissions_tracker/  # Project settings
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```