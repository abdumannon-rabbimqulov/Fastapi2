# FastAPI Blog Platform

A modern, asynchronous blog/social media platform built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. This API supports user authentication, post management, comments, and wishlists.

## 🎯 Features

- **User Authentication**: Sign up and login with secure password hashing
- **Post Management**: Create, read, update, and delete blog posts
- **Comments System**: Users can comment on posts
- **Wishlists**: Save favorite posts to a wishlist
- **Async Operations**: Fully asynchronous with SQLAlchemy and asyncpg
- **Database Migrations**: Alembic for managing database schema changes
- **Docker Support**: Ready-to-use Docker setup for easy deployment

## 📋 Project Structure

```
FastAPI2/
├── main.py                 # FastAPI application entry point
├── db.py                   # Database configuration and session management
├── requirements.txt        # Python dependencies
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Docker compose configuration
├── Dockerfile             # Docker image configuration
├── alembic/               # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/          # Migration files
├── users/                 # User authentication module
│   ├── models.py         # User ORM models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── router.py         # User API routes
│   ├── auth.py           # Authentication utilities
│   └── crud.py           # Database operations
└── Post/                 # Post management module
    ├── models.py         # Post, Comment, Wishlist ORM models
    ├── schemas.py        # Pydantic schemas
    ├── router.py         # Post API routes
    └── crud.py           # Database operations
```

## 🛠 Tech Stack

- **Framework**: FastAPI 0.115.0
- **ORM**: SQLAlchemy 2.0.49 with async support
- **Database**: PostgreSQL 15
- **Async Driver**: asyncpg 0.29.0
- **Server**: Uvicorn 0.44.0
- **Authentication**: python-jose 3.5.0, passlib 1.7.4
- **Migrations**: Alembic
- **Container**: Docker & Docker Compose

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 15
- Docker & Docker Compose (optional)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FastAPI2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DB_URl=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi1
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations** (if needed)
   ```bash
   docker-compose exec api alembic upgrade head
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Authentication
- `POST /user/sign-up` - Register a new user
  ```json
  {
    "first_name": "John",
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
  }
  ```

- `POST /user/login` - Login user
  ```json
  {
    "username": "john_doe",
    "password": "secure_password"
  }
  ```

### Posts
- `GET /posts` - Get all posts
- `GET /posts/{post_id}` - Get a specific post
- `POST /posts` - Create a new post (requires authentication)
- `PUT /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post

### Comments
- `GET /posts/{post_id}/comments` - Get comments on a post
- `POST /posts/{post_id}/comments` - Add a comment (requires authentication)
- `DELETE /comments/{comment_id}` - Delete a comment

### Wishlists
- `GET /wishlist` - Get user's wishlisted posts
- `POST /wishlist/{post_id}` - Add post to wishlist
- `DELETE /wishlist/{post_id}` - Remove post from wishlist

## 📖 API Documentation

Once the application is running, access interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `first_name` (String, nullable)
- `username` (String, unique)
- `email` (String, unique)
- `password` (String, hashed)
- `is_staff` (Boolean, default: False)
- `is_active` (Boolean, default: True)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Posts Table
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `title` (String)
- `slug` (String, unique, nullable)
- `desc` (Text)
- `view_count` (Integer, default: 0)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Comments Table
- `id` (Primary Key)
- `post_id` (Foreign Key → posts.id)
- `user_id` (Foreign Key → users.id)
- `text` (Text)
- `created_at` (DateTime)

### Wishlists Table
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `post_id` (Foreign Key → posts.id)
- `added_at` (DateTime)
- **Unique Constraint**: (user_id, post_id)

## 🔐 Security Features

- Password hashing using passlib
- JWT token support via python-jose
- Cascade delete for referential integrity
- Input validation with Pydantic schemas
- Async database operations to prevent blocking

## 🚀 Development

### Create a new database migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migrations
```bash
alembic downgrade -1
```

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_URl` | Database connection URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi1` |

## 🐳 Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f api

# Run commands in container
docker-compose exec api <command>
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ by the development team

---

**Note**: This project is under active development. Features and endpoints may be subject to change.

