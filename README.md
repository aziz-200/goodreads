# 📚 Goodreads Clone — Django Full-Stack + REST API

A full-stack **Goodreads-inspired book review platform** built with **Django 6**, **PostgreSQL**, **Celery**, and **Django REST Framework**. Users can browse books, write star-rated reviews, manage their profiles, and receive a welcome email upon registration — all powered by an asynchronous task queue and a complementary REST API layer.

---

## 🚀 Features

### 📖 Books
- **Book Listing** — Paginated list of all books (4 per page), ordered by newest first
- **Search** — Full-text search across book title, description, and ISBN using Django `Q` objects
- **Book Detail** — Full book info with cover image, author(s), and all reviews
- **Cover Images** — Upload custom covers; falls back to a default cover image
- **Book–Author Relationship** — Many-to-many via explicit `BookAuthor` junction model with `full_name` property

### ⭐ Reviews
- **Write Reviews** — Authenticated users can post a star rating (1–5) and written comment
- **Edit Reviews** — Authors can update their own reviews via a dedicated edit page
- **Delete Reviews** — Confirmation page before deletion; success flash message on completion
- **Validation** — `MinValueValidator` and `MaxValueValidator` enforce 1–5 star range at the model level

### 👤 Users & Profiles
- **Custom User Model** — Extends `AbstractUser` with a `profile_pic` field
- **Registration** — Custom `UserCreateForm` with profile picture upload
- **Login / Logout** — Session-based auth with Django's `AuthenticationForm`
- **Profile Page** — Displays user info and uploaded profile picture
- **Profile Edit** — Update name, email, and profile photo
- **Welcome Email** — Automatically sent on registration via Django Signals + Celery async task

### 📡 REST API
- **Book Review CRUD** — Full create, retrieve, update, delete via DRF `APIView`
- **Paginated List** — DRF `PageNumberPagination` (10 per page) on review list endpoint
- **Nested Serializers** — `BookReviewSerializer` embeds full `UserSerializer` and `BookSerializer`
- **Write via IDs** — Accepts `user_id` and `book_id` as writable FK fields alongside read-only nested objects
- **Auth Protected** — All API endpoints require `IsAuthenticated`
- **Browsable API** — DRF's built-in browsable API available at `/api-auth/`

### ⚙️ Async & Infrastructure
- **Celery** — Async task queue for non-blocking email delivery
- **Django Signals** — `post_save` on `CustomUser` triggers the welcome email task automatically
- **SMTP Email** — Configurable via `.env` (Gmail / any SMTP provider)
- **Environment Config** — All secrets managed via `django-environ` and `.env`
- **Custom Middleware** — `SimpleMiddleware` scaffold included (currently disabled, ready to activate)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.14 |
| **Framework** | Django 6.0.7 |
| **REST API** | Django REST Framework 3.17 |
| **Database** | PostgreSQL (`psycopg2`) |
| **Task Queue** | Celery 5.6 |
| **Message Broker** | RabbitMQ (AMQP via `kombu`) |
| **Email** | Django SMTP + Celery async task |
| **Signals** | Django `post_save` signal |
| **Image Handling** | Pillow |
| **Config** | `django-environ` (.env) |
| **Frontend** | Django Templates + HTML/CSS |
| **Package Manager** | Pipenv |

---

## 📁 Project Structure

```
goodreads/
├── config/                        # Project configuration
│   ├── settings.py                # DB, Email, Celery, DRF, Media config
│   ├── urls.py                    # Root URL routing
│   ├── celery.py                  # Celery app setup & autodiscovery
│   ├── middleware.py              # Custom middleware scaffold
│   ├── views.py                   # Landing & home page views
│   └── wsgi.py
│
├── books/                         # Core book & review app
│   ├── models.py                  # Book, Author, BookAuthor, BookReview
│   ├── views.py                   # List, Detail, Add/Edit/Delete Review views
│   ├── forms.py                   # BookReviewForm (ModelForm)
│   ├── urls.py                    # Books URL patterns
│   └── templates/books/
│       ├── list.html              # Paginated book list + search
│       ├── detail.html            # Book detail + reviews + review form
│       ├── edit_review.html       # Edit review page
│       └── confirm_delete_review.html
│
├── users/                         # Auth & profile app
│   ├── models.py                  # CustomUser (AbstractUser + profile_pic)
│   ├── views.py                   # Register, Login, Logout, Profile, Edit
│   ├── forms.py                   # UserCreateForm, UserUpdateForm
│   ├── signals.py                 # post_save → send welcome email via Celery
│   ├── tasks.py                   # Celery task: send_email()
│   ├── urls.py                    # User URL patterns
│   └── templates/users/
│       ├── register.html
│       ├── login.html
│       ├── profile.html
│       └── profile_edit.html
│
├── api/                           # REST API app
│   ├── serializers.py             # UserSerializer, BookSerializer, BookReviewSerializer
│   ├── views.py                   # BookReviewAPIView, BookReviewListAPIView
│   └── urls.py                    # API URL patterns
│
├── templates/                     # Global templates
│   ├── base.html                  # Base layout
│   ├── home.html                  # Home page
│   └── landing.html               # Landing page
│
├── .env                           # Environment variables (not committed)
├── .env.example                   # Environment variable template
├── requierments.txt               # Pinned production dependencies
├── Pipfile
└── manage.py
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/aziz-200/goodreads.git
cd goodreads
```

### 2. Install dependencies
```bash
pip install pipenv
pipenv install
pipenv shell
```

### 3. Configure environment variables

Copy the example file and fill in your values:
```bash
cp .env.example .env
```

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgres://user:password@localhost:5432/goodreads_db

EMAIL_FROM=noreply@yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
```

### 4. Create PostgreSQL database
```sql
CREATE DATABASE goodreads_db;
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Start the Celery worker
```bash
celery -A config worker --loglevel=info
```

> **Note:** RabbitMQ must be running before starting the Celery worker.
> Install via Docker: `docker run -d -p 5672:5672 rabbitmq`

### 8. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 📦 Dependencies

```
django==6.0.7
djangorestframework==3.17.1
psycopg2==2.9.12
celery==5.6.3
kombu==5.6.2
pillow==12.3.0
django-environ==0.12.0
```

Install all:
```bash
pipenv install
```

---

## 🌐 URL Overview

### Web Pages

| URL | View | Description |
|---|---|---|
| `/` | `landing` | Landing page |
| `/home/` | `home` | Home page (authenticated) |
| `/books/` | `BooksView` | Paginated book list + search |
| `/books/<id>/` | `BookDetailView` | Book detail + review form |
| `/books/<id>/reviews/` | `AddReviewView` | POST: submit a new review |
| `/books/<bookid>/reviews/<reviewId>/edit/` | `EditReviewView` | GET/POST: edit a review |
| `/books/<bookid>/reviews/<reviewId>/delete/confirm/` | `ConfirmDeleteReviewView` | Confirm deletion page |
| `/books/<bookid>/reviews/<reviewId>/delete/` | `DeleteReviewView` | Delete a review |
| `/users/register/` | `RegisterView` | Register a new account |
| `/users/login/` | `LoginView` | Login page |
| `/users/logout/` | `LogOutView` | Logout |
| `/users/profile/` | `ProfileView` | View own profile |
| `/users/profile/edit/` | `ProfileUpdateView` | Edit profile & photo |
| `/admin/` | Django Admin | Superuser admin panel |

---

## 📡 API Endpoints

All endpoints are prefixed with `/api/` and require **session authentication** or browsable API login at `/api-auth/`.

### Book Reviews

| Method | Endpoint | Auth | Request Body | Response |
|---|---|---|---|---|
| `GET` | `/api/reviews/` | ✅ | — | Paginated list of all reviews (10/page) |
| `POST` | `/api/reviews/` | ✅ | `{ stars_given, comment, user_id, book_id }` | Created review object (201) |
| `GET` | `/api/reviews/<id>` | ✅ | — | Single review with nested user & book |
| `PUT` | `/api/reviews/<id>` | ✅ | `{ stars_given, comment, user_id, book_id }` | Updated review object |
| `DELETE` | `/api/reviews/<id>` | ✅ | — | 204 No Content |

### Sample Response — GET `/api/reviews/<id>`

```json
{
  "id": 3,
  "stars_given": 4,
  "comment": "A wonderful read, highly recommend!",
  "user": {
    "id": 1,
    "first_name": "Aziz",
    "last_name": "Doe",
    "username": "aziz_dev",
    "email": "aziz@example.com"
  },
  "book": {
    "id": 7,
    "title": "The Alchemist",
    "description": "A classic novel about following your dreams...",
    "isbn": 9780062315007
  },
  "user_id": 1,
  "book_id": 7
}
```

### Sample Response — GET `/api/reviews/` (paginated)

```json
{
  "count": 38,
  "next": "http://localhost:8000/api/reviews/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## 🗄️ Data Models

### CustomUser (extends `AbstractUser`)
| Field | Type | Notes |
|---|---|---|
| `id` | AutoField | Primary key |
| `profile_pic` | ImageField | `profile_pic/` — defaults to `profile_default_pic.jpg` |
| + all Django `AbstractUser` fields | | `username`, `email`, `first_name`, `last_name`, etc. |

### Book
| Field | Type | Notes |
|---|---|---|
| `title` | CharField(100) | |
| `description` | TextField(5000) | |
| `isbn` | IntegerField | |
| `cover_picture` | ImageField | `cover_pic/` — defaults to `cover_default_pic.jpg` |

### Author
| Field | Type | Notes |
|---|---|---|
| `first_name` | CharField(100) | |
| `last_name` | CharField(100) | |
| `email` | EmailField | |
| `bio` | TextField | |

### BookAuthor (junction table)
| Field | Type | Notes |
|---|---|---|
| `book` | FK → Book | |
| `author` | FK → Author | |
| `full_name` | property | `author.first_name + last_name` |

### BookReview
| Field | Type | Notes |
|---|---|---|
| `user` | FK → CustomUser | |
| `book` | FK → Book | |
| `comment` | TextField | |
| `stars_given` | IntegerField | Validated 1–5 |
| `created_at` | DateTimeField | Auto set to `timezone.now` |

---

## 📧 Async Email Flow

When a new user registers, a welcome email is dispatched automatically — without blocking the HTTP response:

```
User registers
      │
      ▼
CustomUser.post_save signal fires
      │
      ▼
send_email.delay(subject, message, [email])   ← Celery async task
      │
      ▼
Celery worker picks up task from RabbitMQ
      │
      ▼
Django send_mail() → SMTP → user's inbox
```

---

## 👤 Author

**Aziz** — [azizaxtamov0201@gmail.com](mailto:azizaxtamov0201@gmail.com) · [github.com/aziz-200](https://github.com/aziz-200)
