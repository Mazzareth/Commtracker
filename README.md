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

## Automatic GitHub Updates

You can enable automatic updating of your deployment from GitHub using the built-in updater app. There are two approaches: webhook-based and polling.

### Webhook Approach

1. **Configure GitHub Webhook**  
   Set up a webhook in your GitHub repository to POST to:  
   ```
   http(s)://<your-server>/github-webhook/
   ```
   Recommended: Add a secret and set it as the environment variable `GITHUB_WEBHOOK_SECRET` or in your Django settings as `GITHUB_WEBHOOK_SECRET`.

2. **How it works**  
   - On each push, GitHub will send a payload to `/github-webhook/`.
   - The updater verifies the signature (if secret is set), fetches new commits, installs dependencies, runs migrations, and restarts the server process.

3. **Supported Events**
   - `push`: Triggers update process (async, so request returns immediately).
   - `ping`: Returns "pong" for GitHub webhook setup/testing.
   - All others: Ignored.

### Polling Approach

You may run a background process that periodically checks for updates and applies them automatically.

- **Run the updater**:
  ```bash
  python manage.py github_auto_updater --interval 60
  ```
  This will check every 60 seconds for new commits on the upstream branch.
- If an update is found, the project will:
  1. Pull new code (`git pull --rebase`)
  2. Install dependencies (`pip install -r requirements.txt`)
  3. Run migrations (`python manage.py migrate`)
  4. Restart the Python process so new code is loaded

- This command is designed to be run under a process manager like systemd or Supervisor for reliability.

#### Example systemd unit

```
[Unit]
Description=Django GitHub Auto-Updater

[Service]
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python3 manage.py github_auto_updater --interval 60
Restart=always
User=youruser
Environment=GITHUB_WEBHOOK_SECRET=your_webhook_secret
Environment=DJANGO_SETTINGS_MODULE=commissions_tracker.settings

[Install]
WantedBy=multi-user.target
```

## Environment Variables

- **GITHUB_WEBHOOK_SECRET** (optional but recommended):  
   Secret string for verifying GitHub webhook payloads (HMAC-SHA256).

## Enabling the Updater

- The updater app is included in `INSTALLED_APPS` and its URLs are wired at the root.
- Webhook endpoint: `/github-webhook/`
- Polling command: `python manage.py github_auto_updater --interval 60` (run as a service for continuous polling).

---

## Additional Requirements & Features

### File Uploads

- **Pillow** is required for file/image uploads via Django's `ImageField`.
  - Install with:
    ```bash
    pip install Pillow
    ```
- Uploaded character reference files are stored in `MEDIA_ROOT/character_references/`.
- If you haven't set up `MEDIA_ROOT` and `MEDIA_URL`, add them to your Django settings for file upload support:
    ```python
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / "media"
    ```
  And ensure these are served in development with:
    ```python
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

### Migrations

- After updating models, run:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Static Files

- Run `python manage.py collectstatic` after static/style changes.

### Notes System

- You can now add, edit, and list multiple notes for Clients and Commissions directly from the list panel UI.
- Notes are timestamped and support quick inline add and edit.