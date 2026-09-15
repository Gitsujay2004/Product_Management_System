# Product Management System

## Overview

A full-featured RESTful API for managing products, categories, users, sessions, and product images. Built with FastAPI and PostgreSQL, this application provides a robust backend for product management workflows with async database operations, UUID-based primary keys, and automatic schema validation.

## Features

- **Full CRUD Operations** — Create, Read, Update, and Delete resources across all entities
- **Async Architecture** — Non-blocking database operations using SQLAlchemy async and asyncpg
- **UUID Primary Keys** — All models use UUIDs for unique, non-sequential identification
- **Automatic Schema Creation** — Database tables are auto-created on application startup
- **Pydantic Validation** — Request and response payloads are validated with Pydantic schemas
- **Docker-Ready Database** — PostgreSQL 16 containerized via Docker Compose
- **Database Connectivity Test** — Dedicated endpoint to verify database connection
- **Structured Codebase** — Clean separation of models, schemas, API routes, and configuration

## Project Architecture

```
Product_Management_System/
├── app/
│   ├── main.py                  # FastAPI application entrypoint
│   ├── core/
│   │   └── config.py            # Pydantic settings (env-based configuration)
│   ├── database/
│   │   └── database.py          # Async SQLAlchemy engine and session management
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── session.py           # Session model
│   │   ├── product.py           # Product model
│   │   ├── category.py          # Category model
│   │   └── product_image.py     # Product_Image model
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── user.py              # UserCreate, UserUpdate
│   │   ├── session.py           # SessionCreate, SessionUpdate
│   │   ├── product.py           # ProductCreate, ProductUpdate
│   │   ├── category.py          # CategoryCreate, CategoryUpdate
│   │   └── product_image.py     # ProductImageCreate, ProductImageUpdate
│   └── api/                     # API route handlers
│       ├── user.py              # User CRUD endpoints
│       ├── session.py           # Session CRUD endpoints
│       ├── product.py           # Product CRUD endpoints
│       ├── category.py          # Category CRUD endpoints
│       └── product_image.py     # Product Image CRUD endpoints
├── .env                         # Environment variables (DATABASE_URL)
├── docker-compose.yml           # PostgreSQL container configuration
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

**Key Files:**
- `app/main.py` — Initializes FastAPI, mounts routers, creates database tables on startup
- `app/core/config.py` — Loads settings from `.env` using `pydantic-settings`
- `app/database/database.py` — Manages async SQLAlchemy engine and session factory
- `app/models/` — Defines all database tables with relationships
- `app/schemas/` — Pydantic models for input validation and response serialization
- `app/api/` — Route handlers implementing CRUD logic for each resource

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Async web framework for building REST APIs |
| **Python 3.11** | Programming language |
| **SQLAlchemy 2.0** | Async ORM with declarative models and mapped columns |
| **asyncpg** | High-performance async PostgreSQL driver |
| **PostgreSQL 16** | Relational database |
| **Pydantic v2** | Data validation and serialization |
| **pydantic-settings** | Environment-based configuration management |
| **Uvicorn** | ASGI server for running FastAPI |
| **Docker Compose** | Containerized PostgreSQL setup |

## Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose** (for PostgreSQL)
- **pip** (Python package manager)
- A virtual environment tool (recommended)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Gitsujay2004/Product_Management_System.git
cd Product_Management_System
```

### 2. Create and activate a virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy asyncpg pydantic pydantic-settings python-dotenv
```

### 4. Start PostgreSQL with Docker

```bash
docker compose up -d
```

This starts a PostgreSQL 16 container with the following defaults:

| Setting | Value |
|---------|-------|
| Host | `localhost` |
| Port | `5432` |
| User | `postgres` |
| Password | `postgres123` |
| Database | `product_management` |

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@localhost:5432/product_management
```

Adjust the credentials if you changed them in `docker-compose.yml`.

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

## API Endpoints

### Root

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/database-test` | Test database connectivity |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/categories/` | Create a new category |
| GET | `/categories/` | List all categories |
| GET | `/categories/{category_id}` | Get a category by ID |
| PUT | `/categories/{category_id}` | Update a category |
| DELETE | `/categories/{category_id}` | Delete a category |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products/` | Create a new product |
| GET | `/products/` | List all products |
| GET | `/products/{product_id}` | Get a product by ID |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |

### Product Images

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/product-images/` | Add a product image |
| GET | `/product-images/` | List all product images |
| GET | `/product-images/{image_id}` | Get an image by ID |
| PUT | `/product-images/{image_id}` | Update an image |
| DELETE | `/product-images/{image_id}` | Delete an image |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | List all users |
| GET | `/users/{user_id}` | Get a user by ID |
| PUT | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |

### Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions/` | Create a new session |
| GET | `/sessions/` | List all sessions |
| GET | `/sessions/{session_id}` | Get a session by ID |
| PUT | `/sessions/{session_id}` | Update a session |
| DELETE | `/sessions/{session_id}` | Delete a session |

## Database Schema

### Entity Relationship

```
Users 1 ──< N Sessions
Categories 1 ──< N Products
Products 1 ──< N Product Images
```

### Tables

**Users**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | Primary Key |
| username | String(100) | Unique, Not Null |
| email | String(150) | Unique, Not Null |
| password | String(255) | Not Null |
| is_active | Boolean | Default: True |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

**Sessions**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | Primary Key |
| user_id | UUID | Foreign Key → Users |
| token | String(500) | Not Null |
| expires_at | DateTime | Not Null |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

**Categories**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | Primary Key |
| name | String(100) | Unique, Not Null |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

**Products**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | Primary Key |
| name | String(100) | Unique, Not Null |
| category_id | UUID | Foreign Key → Categories |
| price | Numeric(10,2) | Not Null |
| stock | Integer | Not Null |
| status | String(20) | Not Null |
| description | Text | Nullable |
| sku | String(100) | Not Null |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

**Product Images**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | Primary Key |
| product_id | UUID | Foreign Key → Products |
| url | String(100) | Not Null |
| is_primary | Boolean | Not Null |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

## Docker

The `docker-compose.yml` runs PostgreSQL only:

```bash
# Start PostgreSQL
docker compose up -d

# Stop PostgreSQL
docker compose down

# Stop and remove data
docker compose down -v
```
