# Product Management System

A production-oriented asynchronous REST API backend for managing products, categories,
product images, users, and refresh-token sessions. Built with FastAPI on an async
SQLAlchemy / PostgreSQL stack, with JWT authentication, role-based authorization,
rate limiting, centralized error handling, Alembic migrations, Docker packaging, and
an automated test suite.

---

## 1. Project Overview

The **Product Management System** is the backend service of a product catalogue
application. It exposes a versioned REST API (`/api/v1`) that lets authenticated users
browse and search products, while administrators manage the catalogue, users, and
sessions.

The purpose of the project is to demonstrate a clean, layered FastAPI backend
architecture that is:

- **Fully asynchronous** end-to-end — async SQLAlchemy sessions with the `asyncpg` driver.
- **Secure by design** — bcrypt password hashing, short-lived JWT access tokens,
  database-tracked refresh tokens, role-based authorization, rate limiting on
  sensitive auth endpoints, security headers, and host/CORS restrictions.
- **Maintainable** — a strict separation of API, service, repository, schema, and model
  layers so each concern can be tested and changed independently.
- **Deployable** — Docker image for the API plus a Docker Compose stack with
  PostgreSQL, and versioned Alembic migrations instead of runtime table creation.
- **Verified** — 70 automated async tests run against an isolated test database.

---

## 2. Key Features

The following capabilities are implemented in the current source code.

### Authentication

- **User registration** — `POST /api/v1/auth/register` with duplicate username and
  duplicate email checks before insertion.
- **User login** — `POST /api/v1/auth/login` using email + password, returning an access
  token, a refresh token, and the authenticated user's public fields.
- **JWT authentication** — tokens are signed with a configurable algorithm using
  `SECRET_KEY` from the environment.
- **Access tokens** — short-lived tokens (`ACCESS_TOKEN_EXPIRE_MINUTES`, default 30)
  carrying `sub`, `email`, `role`, `exp`, and a `type: "access"` claim.
- **Refresh tokens** — long-lived tokens (`REFRESH_TOKEN_EXPIRE_DAYS`) carrying
  `type: "refresh"`, and persisted in the database so they can be revoked.
- **Session management** — every successful login stores the refresh token in the
  `sessions` table with an expiry timestamp; `POST /auth/refresh` re-issues an access
  token only if the session exists, belongs to the same user, and has not expired;
  `POST /auth/logout` deletes the session, immediately invalidating the refresh token.
- **Current user profile** — `GET /api/v1/auth/me` and `GET /api/v1/users/me` return
  the authenticated user's profile.

### Authorization

- **Admin authorization** — a `require_admin` dependency checks `user.role == "admin"`
  and rejects non-admins with `403 Forbidden`. The `role` column defaults to `"user"`,
  and admin-only operations are protected across the user, product, and category
  routers.
- **User management** — admin-only create, list, read, update, delete, and an
  activate/deactivate status endpoint.
- **Account status enforcement** — `get_current_user` rejects tokens belonging to
  inactive accounts with `403 Forbidden` (`ACCOUNT_INACTIVE`).

### Catalogue Management

- **Product management** — create, read (with pagination, search, filtering, and
  sorting), update, and delete products; products can be created together with their
  images in a single request.
- **Category management** — create, list, read, update, and delete categories, with
  duplicate-name protection and a guard that blocks deleting a category that still has
  products assigned.
- **Product image management** — create, list, read, update, and delete product images,
  including a primary-image flag, with cascade deletion when the parent product is
  deleted.
- **Validation** — Pydantic v2 schemas enforce field lengths, non-negative prices and
  stock, two-decimal currency precision, valid email addresses (`EmailStr`), UUID
  path/query parameters, and whitespace-stripping `field_validator`s. Images nested
  inside a product-create payload are validated as `HttpUrl`. Query parameters are
  constrained with `ge`/`le` bounds and `Literal` allow-lists for sort fields and
  direction.
- **Deliberately minimal request schemas** — `RegisterRequest` / `LoginRequest` and the
  standalone `ProductImageCreate` / `ProductImageUpdate` schemas validate types and the
  email format only. Length and URL constraints live on the admin-facing user, product,
  and category schemas.

### Security & Operations

- **Centralized error handling** — global handlers convert application exceptions,
  request validation errors, database integrity errors, rate-limit violations, and
  any unhandled exception into a consistent JSON envelope.
- **Security headers** — every response carries `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, and `Content-Security-Policy`.
- **CORS** — an explicit allow-list of origins, methods, and headers.
- **Trusted Host** — requests are rejected unless the `Host` header matches an
  allow-list (`localhost`, `127.0.0.1`).
- **Rate limiting** — per-client-IP limits on registration, login, and token refresh,
  returning `429 Too Many Requests` when exceeded.
- **Environment-based configuration** — all secrets, connection strings, and token
  lifetimes come from environment variables via `pydantic-settings`.
- **Structured logging** — a single `setup_logging()` entry point configures root
  logging, and unhandled exceptions are logged with the request method and path.
- **Database migrations** — Alembic manages the schema; there is no `create_all` on
  startup.
- **Automated testing** — 70 async tests covering auth, products, categories, users,
  sessions, product images, and rate limiting.

---

## 3. Technology Stack

All of the following are present in `requirements.txt` / `Dockerfile` and used in the
source code. Versions reflect the current working environment (`env/`), not pins — see
the note below the table.

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 (base image `python:3.11-slim`) | Runtime language |
| FastAPI | 0.141.x | Async ASGI web framework, routing, dependency injection, OpenAPI generation |
| Starlette | 1.6.x | Middleware stack (`CORSMiddleware`, `TrustedHostMiddleware`, `BaseHTTPMiddleware`) |
| Uvicorn | 0.52.x | ASGI server used locally and as the container entrypoint |
| SQLAlchemy (async) | 2.0.x | Async ORM, `DeclarativeBase`, `Mapped`/`mapped_column` typing, `selectinload` eager loading |
| asyncpg | 0.31.x | Async PostgreSQL driver |
| PostgreSQL | 16 (container image) | Relational database |
| Pydantic | 2.13.x | Request/response validation and serialization |
| pydantic-settings | 2.15.x | Environment-based configuration (`BaseSettings`, `.env` loading) |
| email-validator | 2.3.x | Backs `EmailStr` validation |
| Alembic | 1.20.x | Versioned schema migrations |
| python-jose | 3.5.x | JWT encoding/decoding (`HS256` by default) |
| Passlib | 1.7.x | Password hashing framework (`CryptContext`) |
| bcrypt | 4.0.x | bcrypt password hashing scheme |
| cryptography | 50.x | Cryptographic backend required by `python-jose[cryptography]` |
| SlowAPI | 0.1.x | Rate limiting (`Limiter`, `RateLimitExceeded`) |
| limits | 5.8.x | Storage backend used by SlowAPI |
| pytest | 9.1.x | Test runner |
| pytest-asyncio | 1.4.x | Async test execution (`@pytest.mark.asyncio`, `pytest_asyncio.fixture`) |
| HTTPX | 0.28.x | `AsyncClient` + `ASGITransport` for in-process async API testing |
| python-dotenv | 1.2.x | `.env` file loading |
| Docker / Docker Compose | — | Containerized backend and PostgreSQL |

> **Note on JWT library:** the project uses `python-jose`, not `PyJWT`.

> **Note on versioning:** `requirements.txt` lists dependencies **without version
> pins**, so a fresh `pip install` resolves to the newest compatible release. Pinning
> exact versions (or a lock file) is listed under
> [Future Improvements](#21-future-improvements).

---

## 4. Project Architecture

Actual repository layout (local virtualenv `env/`, `.env`, `.git/`, and
`__pycache__/` are omitted because they are git-ignored or generated):

```
Product_Management_System/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app, middleware, exception handlers
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py              # get_current_user, require_admin (HTTPBearer)
│   │   ├── docker.txt                   # Notes: inspecting PostgreSQL via psql in Docker
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py                # Aggregates all v1 routers
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth_router.py
│   │           ├── user_router.py
│   │           ├── product_router.py
│   │           ├── category_router.py
│   │           ├── productImage_router.py
│   │           └── session_router.py
│   ├── core/
│   │   ├── settings.py                  # Pydantic Settings loaded from .env
│   │   ├── security.py                  # bcrypt hashing + JWT create/verify
│   │   ├── rate_limiter.py              # SlowAPI Limiter instance
│   │   ├── logging.py                   # setup_logging()
│   │   └── key.py                       # Helper that prints a generated secret key
│   ├── database/
│   │   ├── base.py                      # DeclarativeBase
│   │   └── session.py                   # Async engine, sessionmaker, get_db
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── session_model.py
│   │   ├── product_model.py
│   │   ├── category_model.py
│   │   └── productImage_model.py
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── user_response_schema.py
│   │   ├── product_schema.py
│   │   ├── product_response_schema.py
│   │   ├── category_schema.py
│   │   ├── category_response_schema.py
│   │   ├── productImage_schema.py
│   │   ├── session_schema.py
│   │   ├── common_schema.py             # MessageResponse, DataResponse[T]
│   │   └── error_schema.py              # ErrorResponse envelope
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   ├── session_repo.py
│   │   ├── product_repo.py
│   │   ├── category_repo.py
│   │   └── productImage_repo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── category_service.py
│   │   ├── productImage_service.py
│   │   └── session_service.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── custom_exceptions.py        # AppException hierarchy
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── security_headers.py
│   ├── integrations/
│   │   └── __init__.py                  # Reserved package (currently empty)
│   ├── tasks/
│   │   └── __init__.py                  # Reserved package (currently empty)
│   ├── utils/
│   │   └── __init__.py                  # Reserved package (currently empty)
│   └── old_approach/                    # Legacy pre-layered router modules
│       ├── user.py
│       ├── session.py
│       ├── product.py
│       ├── category.py
│       └── product_image.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # Test DB, client fixtures, admin_client fixture
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_products.py
│   ├── test_categories.py
│   ├── test_product_images.py
│   └── test_sessions.py
├── alembic/
│   ├── README
│   ├── env.py                           # Async Alembic env using settings.DATABASE_URL
│   ├── script.py.mako
│   └── versions/
│       └── 6722683572a5_update_session_token_constraints.py
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
├── git.txt                              # Git session notes (scratch file)
└── README.md
```

> There is no `scripts/` or `docker/` directory in this repository; Docker assets live
> in `Dockerfile`, `docker-compose.yml`, and `.dockerignore` at the project root.
> `app/integrations/`, `app/tasks/`, `app/utils/`, and `app/old_approach/` are present
> but contain no active application logic.
>
> There is also no `pytest.ini`, `pyproject.toml`, or `setup.cfg`, so `pytest-asyncio`
> runs in its default strict mode and every async test carries an explicit
> `@pytest.mark.asyncio` marker.

---

## 5. Backend Architecture

The application follows a strict layered architecture. Each layer has one
responsibility, and a request flows top-down through the stack.

```
HTTP Request
   ↓
Middleware Stack (CORS → TrustedHost → SecurityHeaders)
   ↓
API / Router Layer   (app/api/v1/endpoints/*)  – HTTP concerns, auth dependencies
   ↓
Service Layer        (app/services/*)          – business rules, orchestration
   ↓
Repository Layer     (app/repositories/*)      – SQL queries, persistence
   ↓
Model Layer          (app/models/*)            – SQLAlchemy ORM entities
   ↓
Database Layer       (app/database/session.py) – async engine + session factory
   ↕
PostgreSQL
```

Errors travel back up the same path and are converted to HTTP responses by the global
exception handlers registered in `app/main.py`.

### API Layer — `app/main.py`

- Instantiates the `FastAPI` application (title: `Product Management System`).
- Registers middleware: `SecurityHeadersMiddleware`, `TrustedHostMiddleware`,
  `CORSMiddleware`. Because Starlette prepends each `add_middleware` call, the last one
  added is the outermost, so the request passes through CORS first and the security
  headers are applied last, on the way out.
- Registers global exception handlers: `AppException`, `RequestValidationError`,
  `IntegrityError`, `RateLimitExceeded`, and a catch-all `Exception` handler.
- Attaches the SlowAPI limiter to `app.state.limiter`.
- Mounts the v1 API router under the `/api/v1` prefix.
- Exposes two operational endpoints: `GET /` (service health check) and
  `GET /database-test` (executes `SELECT 1` to verify database connectivity).
- Table creation on startup is intentionally **disabled** (the `@app.on_event("startup")`
  hook is present but fully commented out); the schema is managed by Alembic migrations.

### Router Layer — `app/api/v1/`

- `app/api/v1/router.py` aggregates the six feature routers (auth, users, products,
  categories, product images, sessions) into a single `APIRouter`.
- Each `*_router.py` module owns a single resource: it declares its `prefix`, OpenAPI
  `tags`, HTTP methods, path/query parameters, response models, authentication
  dependencies, and rate limits.
- Routers contain **no business logic and no SQL**; they parse input via Pydantic
  schemas, call one or more services, and shape the response.
- `app/api/dependencies.py` holds the reusable FastAPI dependencies:
  `get_current_user` (HTTP Bearer authentication) and `require_admin` (role check).

### Service Layer — `app/services/`

- Encapsulates all business rules and orchestrates repositories.
- Enforces domain rules before persistence: duplicate username/email on registration,
  duplicate category names, category-in-use protection on delete, and password hashing.
- Handles the full authentication workflow in `auth_service.py`: registration, login,
  refresh-token validation (JWT claim check → session lookup → session/user ownership
  check → expiry check → new access token), and logout.
- The router calls the service, and the service calls the repository — the service
  layer never touches the request/response objects.

### Repository Layer — `app/repositories/`

- The only layer that builds and executes SQLAlchemy queries.
- Provides data access for users (by id, email, username, list, update, delete,
  activate/deactivate, cascade session cleanup), sessions (by id, by token, list,
  update, delete), products (create with nested images, paginated/filtered/sorted list,
  read, update, delete), categories (create, list, read by id, read by name, update,
  delete, `category_has_products`), and product images.
- `product_repo.get_products` builds the dynamic list query: applies search
  (`ILIKE` on name), category/status/price filters, an allow-listed sort column and
  direction, `selectinload(Product.images)` eager loading, plus a separate `COUNT`
  query for pagination totals.
- Returns ORM objects, not HTTP responses.

### Schema Layer — `app/schemas/`

- Pydantic v2 models split into **request** schemas (`*_schema.py`) and **response**
  schemas (`*_response_schema.py`).
- Request schemas carry the validation rules (length bounds, `ge`/`le`, `EmailStr`,
  `HttpUrl`, `decimal_places`, `field_validator` whitespace stripping).
- Response schemas use `ConfigDict(from_attributes=True)` so ORM instances serialize
  directly, and deliberately exclude password hashes.
- `common_schema.py` defines the shared `MessageResponse` and generic
  `DataResponse[T]` envelopes; `error_schema.py` defines the standard error envelope.

### Model Layer — `app/models/`

- SQLAlchemy 2.0 declarative models using `Mapped[...]` / `mapped_column(...)` typing.
- All primary keys are application-generated UUIDs.
- Timestamps are timezone-aware with `server_default=func.now()` and
  `onupdate=func.now()`.
- `app/models/__init__.py` imports every model so Alembic autogenerate and the test
  metadata can discover all tables.

### Database Layer — `app/database/`

- `base.py` defines the shared `DeclarativeBase`.
- `session.py` creates the async engine from `settings.DATABASE_URL`, an
  `async_sessionmaker` with `expire_on_commit=False`, and the `get_db()` FastAPI
  dependency that yields a session per request and closes it afterwards.
- The engine is currently created with `echo=True`, so SQL is logged at `INFO` level in
  every environment. That is convenient while developing and should be driven by an
  environment setting before production deployment (see
  [Future Improvements](#21-future-improvements)).

### Core / Security Configuration — `app/core/`

- `settings.py` — `Settings(BaseSettings)` reading from `.env`; the single source of
  truth for database URLs, secret key, algorithm, and token lifetimes.
- `security.py` — `CryptContext` (bcrypt) hashing/verification plus
  `create_access_token`, `create_refresh_token`, `verify_access_token`, and
  `verify_refresh_token`.
- `rate_limiter.py` — the shared SlowAPI `Limiter` keyed by client IP.
- `logging.py` — centralized logging configuration.
- `key.py` — a small developer helper that generates a URL-safe random secret key.

### Exception Handling — `app/exceptions/` + `app/main.py`

- `app/exceptions/custom_exceptions.py` defines an `AppException` base class carrying
  `message`, `error_code`, and `status_code`, with `NotFoundException` (404),
  `BadRequestException` (400), `UnauthorizedException` (401), and
  `ForbiddenException` (403) subclasses.
- `app/main.py` registers the handlers that serialize every error type into a uniform
  response shape, and logs unhandled exceptions before returning a generic 500 so
  internal details are never leaked to the client.

---

## 6. Authentication & Authorization

### Registration

`POST /api/v1/auth/register` accepts `username`, `email`, and `password`.

1. Pydantic validates the payload. `RegisterRequest` checks that `email` is a valid
   address (`EmailStr`); it applies no length bounds, unlike the admin-facing
   `UserCreate` / `UserUpdate` schemas (min 3 chars for the username, 8 for the
   password).
2. `auth_service.register_user` looks up the username and email; a match raises
   `400 Bad Request`.
3. The password is hashed with bcrypt via `hash_password()` — the plaintext is never
   stored.
4. The new user is persisted and returned without the password field.

New accounts are created with the default `role = "user"`. The response is a `201` with
`message` and a `user` object containing only `id`, `username`, and `email`.

### Login

`POST /api/v1/auth/login` accepts `email` and `password`.

1. The user is looked up by email; an unknown email returns `401 Unauthorized` with a
   generic message.
2. `verify_password()` compares the submitted password against the stored bcrypt hash.
3. A JWT **access token** and a JWT **refresh token** are created from the same payload
   (`sub` = user id, `email`, `role`).
4. The refresh token and its expiry are persisted as a session row, which makes the
   refresh token revocable.
5. The response returns `access_token`, `refresh_token`, `token_type: "bearer"`, and
   the user's `id`, `username`, and `email`.

### JWT Access Token

- Signed with `SECRET_KEY` using `ALGORITHM` (default `HS256`) via `python-jose`.
- Claims: `sub` (user UUID string), `email`, `role`, `exp`, `type: "access"`.
- Lifetime: `ACCESS_TOKEN_EXPIRE_MINUTES` minutes (default 30).
- Sent by the client as `Authorization: Bearer <access_token>`.

### JWT Refresh Token

- Claims: `sub`, `email`, `role`, `exp`, `type: "refresh"`.
- Lifetime: `REFRESH_TOKEN_EXPIRE_DAYS` days.
- Stored in the `sessions` table (`token` is unique) with a server-side `expires_at`,
  so the token can be invalidated without waiting for cryptographic expiry.

### Token Expiration

- Access tokens expire cryptographically after `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Refresh tokens expire after `REFRESH_TOKEN_EXPIRE_DAYS`; the same value is stored in
  `sessions.expires_at`.
- `verify_access_token` / `verify_refresh_token` reject expired or malformed tokens and
  return `None`, which callers translate into `401 Unauthorized`.

### Token Type Validation

Access and refresh tokens are deliberately not interchangeable:

- `verify_access_token` requires `payload["type"] == "access"`.
- `verify_refresh_token` requires `payload["type"] == "refresh"`.

This prevents a refresh token from being used as a bearer access token (and vice
versa) at the API boundary.

### Password Hashing

- `passlib.context.CryptContext` configured with the `bcrypt` scheme and
  `deprecated="auto"`, so hashes are automatically upgraded when the scheme changes.
- Only the hash is stored in `users.password`; no endpoint returns it — enforced by the
  response schemas, which omit the field entirely.

### Authentication Dependency

`app/api/dependencies.py:get_current_user`

1. Extracts the bearer token using FastAPI's `HTTPBearer` security scheme.
2. Verifies the access token; failure raises `401 Unauthorized` (`INVALID_TOKEN`).
3. Reads the `sub` claim and parses it as a UUID; an unparsable value raises
   `INVALID_TOKEN_USER`.
4. Loads the user from the database; a missing user raises `TOKEN_USER_NOT_FOUND`.
5. Rejects inactive accounts with `403 Forbidden` (`ACCOUNT_INACTIVE`).
6. Returns the ORM `User` object for downstream handlers.

> One branch still uses a raw `HTTPException`: a token that decodes but carries no `sub`
> claim returns `401` with FastAPI's default `{"detail": "Invalid token"}` body instead
> of the standard error envelope. The custom handlers are already in place, so unifying
> it is a small follow-up (see [Future Improvements](#21-future-improvements)).

### Admin Authorization

`app/api/dependencies.py:require_admin` depends on `get_current_user` and compares
`current_user.role` against `"admin"`. A mismatch raises `403 Forbidden` with the
error code `ADMIN_ACCESS_REQUIRED`. Read operations on products and categories require
any authenticated user; all create/update/delete operations on users, products, and
categories require an admin.

### Session Handling

| Action | Behaviour |
|---|---|
| Login | A `sessions` row is created with the refresh token and its expiry |
| Refresh | The token must be a valid `type: "refresh"` JWT, exist in `sessions`, belong to the same user as the `sub` claim, and not be expired; expired sessions are deleted on the spot |
| Logout | The session is deleted, so the refresh token can no longer be exchanged |
| User deletion | All sessions belonging to that user are deleted before the user row is removed |
| User deactivation | `get_current_user` rejects the account with `403` on every subsequent authenticated request |

---

## 7. Rate Limiting

Rate limiting is implemented with **SlowAPI**, using a shared `Limiter` created in
`app/core/rate_limiter.py` and keyed by the client's remote IP address
(`get_remote_address`). The limiter is attached to the application via
`app.state.limiter`, and the `RateLimitExceeded` handler is registered so violations
are returned as proper JSON.

| Endpoint | Limit | Decorator |
|---|---|---|
| `POST /api/v1/auth/register` | **5 requests / minute** | `@limiter.limit("5/minute")` |
| `POST /api/v1/auth/login` | **5 requests / minute** | `@limiter.limit("5/minute")` |
| `POST /api/v1/auth/refresh` | **10 requests / minute** | `@limiter.limit("10/minute")` |

**When the configured limit is exceeded, the API responds with HTTP `429 Too Many
Requests`** instead of executing the operation. This protects the authentication flow
against brute-force login attempts, credential stuffing, automated registration, and
refresh-token abuse.

The test suite verifies this behaviour: the sixth login attempt within a minute and the
sixth registration attempt within a minute both assert a `429` response. The limiter
state is reset in the `client` fixture so tests are independent and deterministic.

---

## 8. Security

The security measures below are all implemented in the current source code.

| Measure | Implementation |
|---|---|
| **Password hashing** | bcrypt via Passlib `CryptContext`; plaintext passwords are never stored or returned |
| **JWT validation** | Signature and expiry verified with `python-jose` using `SECRET_KEY` and the configured algorithm |
| **Access/refresh token type validation** | `verify_access_token` / `verify_refresh_token` reject tokens whose `type` claim does not match |
| **Token expiration** | Access tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES`; refresh tokens after `REFRESH_TOKEN_EXPIRE_DAYS`, with a server-side session expiry check as a second line of defence |
| **Admin authorization** | `require_admin` dependency enforces role checks on all mutating admin endpoints |
| **Inactive account enforcement** | `get_current_user` returns `403` for deactivated users |
| **CORS** | `CORSMiddleware` with an explicit origin allow-list (`http://localhost:5173`), `allow_credentials=True`, and an explicit method/header allow-list — no wildcard origins |
| **Trusted Host** | `TrustedHostMiddleware` accepts only `localhost` and `127.0.0.1` |
| **Security headers** | `SecurityHeadersMiddleware` adds `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Content-Security-Policy: default-src 'self'` |
| **Rate limiting** | SlowAPI limits on register/login/refresh, returning `429` |
| **Environment-based configuration** | All secrets and connection strings are read from environment variables; `.env` is git-ignored and excluded from the Docker build |
| **Global exception handling** | Unhandled exceptions are logged server-side and returned as a generic `500` body, so stack traces and database details are never exposed |
| **Input validation** | Pydantic validation, UUID path parameters, bounded query parameters, allow-listed sort fields, and `HttpUrl` image URLs |
| **Database integrity** | `IntegrityError` is translated into safe, human-readable `400` responses instead of raw driver errors |

**Not currently implemented:** HTTPS/TLS termination and HSTS. The application does not
enable `HTTPSRedirectMiddleware` and does not set a `Strict-Transport-Security` header.
TLS is expected to be handled by a reverse proxy or load balancer in front of the
service.

---

## 9. Database

### PostgreSQL

PostgreSQL 16 is the system of record. It runs as a container in the Docker Compose
stack and is reachable on port `5432` from the host.

### SQLAlchemy Async

The entire data layer is asynchronous. `create_async_engine()` is built from
`settings.DATABASE_URL` (an `asyncpg` DSN such as
`postgresql+asyncpg://user:password@host:5432/database`), and every query is `await`ed
through `AsyncSession`. `expire_on_commit=False` keeps ORM attributes readable after a
commit without an extra round-trip.

### asyncpg

`asyncpg` is the async PostgreSQL driver used by SQLAlchemy, with Alembic configured to
run migrations through the same async engine (`create_async_engine` + `run_sync`).

### Models

| Model | Table | Columns |
|---|---|---|
| `User` | `users` | `id` (UUID PK), `username` (String 100, unique, not null), `email` (String 150, unique, not null), `password` (String 255, not null), `role` (String 20, default `user`, not null), `is_active` (Boolean, default `True`, not null), `created_at`, `updated_at` |
| `Session` | `sessions` | `id` (UUID PK), `user_id` (FK → `users.id`, not null), `token` (String 5000, not null, unique), `expires_at` (timezone-aware, not null), `created_at`, `updated_at` |
| `Category` | `categories` | `id` (UUID PK), `name` (String 100, unique, not null), `created_at`, `updated_at` |
| `Product` | `products` | `id` (UUID PK), `name` (String 100, unique, not null), `category_id` (FK → `categories.id`, not null), `price` (Numeric 10,2, not null), `stock` (Integer, not null), `status` (String 20, not null), `description` (Text, nullable), `sku` (String 100, not null), `created_at`, `updated_at` |
| `ProductImage` | `product_image` | `id` (UUID PK), `product_id` (FK → `products.id`, not null), `url` (String 100, not null), `is_primary` (Boolean), `created_at`, `updated_at` |

> The `ProductImage` table is named `product_image` (singular) in the database, while
> the API route is `/api/v1/product-images`.

### Relationships

```
users 1 ──< N sessions        (sessions.user_id  → users.id, FK)

categories 1 ──< N products   (products.category_id → categories.id, FK)
                               enforced in the service layer, not by an ORM relationship

products 1 ──< N product_image (product_image.product_id → products.id, FK)
                               ORM relationship: Product.images ⇄ ProductImage.product
                               cascade="all, delete-orphan"
```

- `Product.images` is a bidirectional SQLAlchemy `relationship` with
  `back_populates="product"` and `cascade="all, delete-orphan"`, so deleting a product
  automatically deletes its images in the same transaction.
- `Category` and `User` are linked to their children through foreign keys only;
  referential behaviour is managed explicitly in the repository/service layer.
- `users`, `categories`, `products`, and `product_image` all carry unique constraints
  that the error handler maps to friendly `400` responses.

### Database Sessions

- `AsyncSessionLocal` is an `async_sessionmaker` bound to the engine.
- `get_db()` is a FastAPI dependency that yields one session per request and disposes
  of it afterwards, so no session is shared across requests.
- Repositories receive the session explicitly as a parameter and are responsible for
  `commit()` and `refresh()`.
- Tests override `get_db` with a factory bound to the separate test engine, so the
  production session maker is never touched during a test run.

### Alembic Migrations

Alembic owns the schema. The app deliberately does **not** call
`Base.metadata.create_all()` on startup (the startup hook is present but commented
out), so production and test schemas are created and evolved the same way.

- `alembic/env.py` imports all five models, sets `target_metadata = Base.metadata`,
  reads the URL from `settings.DATABASE_URL`, and runs migrations through an async
  engine with `NullPool`.
- `alembic.ini` sets `script_location` to the `alembic/` directory and
  `prepend_sys_path = .` so the `app` package is importable.
- One revision is currently committed: `6722683572a5_update_session_token_constraints`,
  which widens `sessions.token` to 5000 characters and adds the
  `uq_sessions_token` unique constraint (the refresh token can exceed the original
  500-character column).
- Workflow: change a model → `alembic revision --autogenerate` → review the generated
  script → `alembic upgrade head`. Every deployment should apply migrations before
  serving traffic.

---

## 10. API Endpoints

All feature endpoints are served under the `/api/v1` prefix.

**Authentication column legend:**
`Public` = no token required · `User` = valid access token required ·
`Admin` = valid access token with `role = "admin"` required.

### System

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/` | Service health check — returns a status message | Public |
| GET | `/database-test` | Executes `SELECT 1` to verify database connectivity | Public |

### Authentication — `/api/v1/auth`

| Method | Endpoint | Purpose | Auth | Rate limit |
|---|---|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user account | Public | 5/minute |
| POST | `/api/v1/auth/login` | Authenticate with email + password; returns access and refresh tokens | Public | 5/minute |
| GET | `/api/v1/auth/me` | Return the authenticated user's profile | User | — |
| POST | `/api/v1/auth/refresh` | Exchange a valid refresh token for a new access token | Public (refresh token in body) | 10/minute |
| POST | `/api/v1/auth/logout` | Delete the session, invalidating the refresh token | Public (refresh token in body) | — |

### Users — `/api/v1/users`

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/users/` | Create a user (admin provisioning) | Admin |
| GET | `/api/v1/users/` | List all users | Admin |
| GET | `/api/v1/users/me` | Return the authenticated user's own profile | User |
| GET | `/api/v1/users/{user_id}` | Fetch a user by UUID | Admin |
| PUT | `/api/v1/users/{user_id}` | Update username, email, and password | Admin |
| DELETE | `/api/v1/users/{user_id}` | Delete a user and all of their sessions | Admin |
| PATCH | `/api/v1/users/{user_id}/status` | Activate or deactivate a user account | Admin |

### Products — `/api/v1/products`

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/products/` | Create a product, optionally with images in the same request | Admin |
| GET | `/api/v1/products/` | List products with pagination, search, filters, and sorting | User |
| GET | `/api/v1/products/{product_id}` | Fetch a single product with its images | User |
| PUT | `/api/v1/products/{product_id}` | Update a product | Admin |
| DELETE | `/api/v1/products/{product_id}` | Delete a product and cascade-delete its images | Admin |

`GET /api/v1/products/` query parameters:

| Parameter | Type / Default | Notes |
|---|---|---|
| `page` | int, default `1`, min `1` | Page number |
| `limit` | int, default `10`, range `1`–`100` | Page size |
| `search` | string, optional | Case-insensitive match on product name |
| `category_id` | UUID, optional | Filter by category |
| `status` | string, optional | Filter by status |
| `min_price` | decimal ≥ 0, optional | Lower price bound |
| `max_price` | decimal ≥ 0, optional | Upper price bound (`min_price > max_price` → `400 INVALID_PRICE_RANGE`) |
| `sort_by` | `name` \| `price` \| `stock` \| `created_at`, default `created_at` | Allow-listed sort column |
| `sort_order` | `asc` \| `desc`, default `desc` | Sort direction |

The response includes a `pagination` block: `page`, `limit`, `total`, `total_pages`,
`has_next`, `has_previous`, plus the applied filter values.

### Categories — `/api/v1/categories`

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/categories/` | Create a category (duplicate names rejected) | Admin |
| GET | `/api/v1/categories/` | List all categories | User |
| GET | `/api/v1/categories/{category_id}` | Fetch a category by UUID | User |
| PUT | `/api/v1/categories/{category_id}` | Rename a category | Admin |
| DELETE | `/api/v1/categories/{category_id}` | Delete a category (rejected while products are assigned) | Admin |

### Product Images — `/api/v1/product-images`

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/product-images/` | Attach an image URL to a product | Currently public |
| GET | `/api/v1/product-images/` | List all product images | Currently public |
| GET | `/api/v1/product-images/{image_id}` | Fetch a product image by UUID | Currently public |
| PUT | `/api/v1/product-images/{image_id}` | Update a product image | Currently public |
| DELETE | `/api/v1/product-images/{image_id}` | Delete a product image | Currently public |

> **Security note:** the product-image router does not currently declare an
> authentication dependency, so these five routes are reachable without a token. The
> same applies to the session routes below. Protecting them is listed under
> [Future Improvements](#21-future-improvements).
>
> `ProductImageCreate` / `ProductImageUpdate` accept `url` as a plain string, so these
> routes do **not** apply the `HttpUrl` validation used for images nested in a
> product-create payload.

### Sessions — `/api/v1/sessions`

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| POST | `/api/v1/sessions/` | Create a session record for a user and token | Currently public |
| GET | `/api/v1/sessions/` | List all session records | Currently public |
| GET | `/api/v1/sessions/{session_id}` | Fetch a session by UUID | Currently public |
| PUT | `/api/v1/sessions/{session_id}` | Update a session's token and expiry | Currently public |
| DELETE | `/api/v1/sessions/{session_id}` | Delete a session by UUID | Currently public |

> Session writes in the normal authentication flow happen through
> `auth_service` (login, refresh, logout), not through these routes. Note also that
> `GET /api/v1/sessions/` returns stored refresh tokens in the response body.

---

## 11. Error Handling

All errors are normalized into a single JSON envelope so clients can handle failures
predictably:

```json
{
  "success": false,
  "message": "Product not found",
  "error_code": "PRODUCT_NOT_FOUND",
  "details": null
}
```

The envelope is defined in `app/schemas/error_schema.py` and produced by the handlers
registered in `app/main.py`.

### Application Exceptions

`app/exceptions/custom_exceptions.py` provides a typed hierarchy, each carrying a
`message`, an `error_code`, and a `status_code`:

| Exception | Status | Typical use |
|---|---|---|
| `BadRequestException` | 400 | Invalid range, invalid price range |
| `UnauthorizedException` | 401 | Invalid/expired token, inactive user context |
| `ForbiddenException` | 403 | Admin access required, inactive account |
| `NotFoundException` | 404 | User, product, or category not found |

The `AppException` handler returns the exception's own message, error code, and status
code, with `details` set to `null`.

### Validation Errors

`RequestValidationError` is handled globally and returns **HTTP 422** with
`error_code: "VALIDATION_ERROR"` and the serialized Pydantic error list in `details`.
This covers missing fields, wrong types, failed UUID parsing, out-of-range numbers,
and failed `EmailStr` / `HttpUrl` validation.

### Integrity Errors

`IntegrityError` is caught and inspected so raw driver messages are never returned:

| Detected in the database message | Status | `error_code` |
|---|---|---|
| `unique` | 400 | `DUPLICATE_VALUE` |
| `foreign key` | 400 | `INVALID_REFERENCE` |
| anything else | 400 | `DATABASE_CONSTRAINT_ERROR` |

### Rate Limit Errors

`RateLimitExceeded` is handled using SlowAPI's built-in handler, returning
**HTTP 429** for requests that exceed a configured limit.

### Global Exception Handling

A catch-all `Exception` handler logs the failure with the request method and path via
`logger.exception`, then returns **HTTP 500** with
`error_code: "INTERNAL_SERVER_ERROR"` and a generic message. This prevents stack
traces, SQL fragments, and internal state from leaking to clients.

### HTTP Status Codes

| Code | Meaning in this API |
|---|---|
| 200 | Successful read, update, or delete |
| 201 | Resource created (registration, user, category, product) |
| 400 | Business-rule violation or database constraint violation |
| 401 | Missing, invalid, or expired token; invalid credentials |
| 403 | Authenticated but not permitted (non-admin, inactive account) |
| 404 | Resource does not exist |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Unhandled server error (generic body, details logged server-side) |

Some handlers still raise `HTTPException` directly and therefore return FastAPI's
default `{"detail": "..."}` body rather than the standard envelope — specifically
register, login, refresh, logout, product update/delete, all product-image routes, and
all session routes. The test suite asserts against these `detail` bodies, so changing
them is a coordinated follow-up rather than a drop-in fix. The exception handlers are
already in place; unifying these responses is listed under
[Future Improvements](#21-future-improvements).

---

## 12. Testing

The suite is built on **pytest** with **pytest-asyncio** and **HTTPX**.

```bash
pytest
```

```
70 passed
```

### Test tooling

| Component | Usage |
|---|---|
| `pytest` | Test discovery and assertions |
| `pytest-asyncio` | `@pytest.mark.asyncio` on every test, `pytest_asyncio.fixture` for async fixtures |
| `httpx.AsyncClient` + `ASGITransport` | In-process async HTTP calls against the real FastAPI app — no live server needed |
| Dependency overrides | `fastapi_app.dependency_overrides[get_db]` redirects the app to the test session factory |
| `sqlalchemy.pool.NullPool` | The test engine avoids connection pooling so teardown is clean |

### Fixtures (`tests/conftest.py`)

- **`test_engine` / `TestSessionLocal`** — a separate async engine built from
  `settings.TEST_DATABASE_URL`, entirely distinct from the application engine.
- **`test_database`** — creates all tables from `Base.metadata` before each test and
  drops them afterwards, giving each test a clean, isolated database.
- **`client`** — resets the SlowAPI limiter, installs the `get_db` override, and yields
  an `AsyncClient` bound to the app; dependency overrides are cleared on teardown.
- **`admin_client`** — seeds an admin user (`role="admin"`, `is_active=True`) with a
  bcrypt-hashed password, logs in through the real `/api/v1/auth/login` endpoint, and
  returns the client together with a ready-to-use `Authorization: Bearer <token>` header.

Because the admin flow goes through the actual login endpoint, admin-only endpoints are
tested through the full authentication stack rather than by mocking.

### Database isolation

- Tests run against `TEST_DATABASE_URL`; the development/production `DATABASE_URL` is
  never touched.
- Tables are dropped after every test, so no state leaks between tests.
- The `admin_client` fixture creates its own admin per test.

### Coverage by area

| Test file | Tests | What it covers |
|---|---|---|
| `tests/test_auth.py` | 11 | Registration, login, invalid password, duplicate username, refresh, invalid refresh token, logout, `/auth/me`, invalid token, **login rate limit**, **register rate limit** |
| `tests/test_users.py` | 17 | Own profile, missing token, list users, non-admin `403`, get by id, not found, create, duplicate username, duplicate email, update, status toggle, delete, and the admin-only `403` path for each |
| `tests/test_products.py` | 14 | List authenticated/unauthenticated, get by id, not found, create, non-admin `403`, validation errors, update, delete, cascade verification after delete |
| `tests/test_categories.py` | 13 | List authenticated/unauthenticated, get by id, not found, create, non-admin `403`, duplicate name, update, delete, and deleting a category that still has products |
| `tests/test_product_images.py` | 8 | Create, list all, get by id, get-not-found, update, update-not-found, delete, delete-not-found |
| `tests/test_sessions.py` | 7 | Refresh success, invalid refresh token, missing refresh token field, logout, invalid logout token, missing logout token field, and refresh-after-logout being rejected |
| **Total** | **70** | |

> No code-coverage percentage is reported, because coverage measurement is not part of
> the current tooling (`pytest-cov` is not installed or configured). The figures above
> are test counts, not coverage.

---

## 13. Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Based on the slim `python:3.11` image.
- Dependencies are installed in a separate layer from the source code, so application
  edits do not invalidate the dependency layer.
- The app runs with Uvicorn bound to `0.0.0.0:8000` (no `--reload`, which is correct for
  a containerized runtime).
- `.dockerignore` keeps `.env`, `.env.*`, `.git/`, virtualenvs, caches, IDE folders, and
  `tests/` out of the image — **secrets and the test suite are never baked into the
  build context.**

### Docker Compose

`docker-compose.yml` defines two services and one named volume:

| Service | Image / Build | Container | Port | Role |
|---|---|---|---|---|
| `postgres` | `postgres:16` | `product_postgre` | `5432:5432` | PostgreSQL database, data persisted in the `postgres_data` volume |
| `backend` | built from `Dockerfile` | `product_backend` | `8000:8000` | FastAPI application |

- The backend service loads the local `.env` file via `env_file`, and additionally
  overrides `DATABASE_URL` in its `environment` block.
- `depends_on: postgres` makes Compose start the database before the backend.
- A named volume `postgres_data` is mounted at `/var/lib/postgresql/data`, so data
  survives `docker compose down` (but not `docker compose down -v`).

> **Note on credentials:** `docker-compose.yml` currently hard-codes the local
> PostgreSQL superuser, password, and database name directly in the `environment`
> blocks. These are local development values only and are intentionally **not**
> reproduced in this README. They should be externalized to `.env` (or a secrets
> manager) before any real deployment — see
> [Future Improvements](#21-future-improvements).

### Container networking

Inside the Compose network, services reach each other by **service name over the
default bridge network**, not by IP or `localhost`.

**The backend container connects to PostgreSQL using the Docker service hostname
`postgres`, not `localhost`.** Its `DATABASE_URL` is therefore built with the host
`postgres`:

```
postgresql+asyncpg://<user>:<password>@postgres:5432/product_management
```

This is a deliberate difference from local development, where the application runs on
the host and must connect to `localhost:5432` (the port published by the `postgres`
container). Compose's `environment` block supplies the container-correct value so the
same `.env` file works in both contexts.

### Environment variables in Docker

- `env_file: .env` passes every variable from the local `.env` into the container.
- The `environment: DATABASE_URL: ...` entry takes precedence over `env_file`, which is
  what makes the `postgres` hostname override the local `localhost` value.
- A `.env` file must exist in the project root before `docker compose up`, otherwise
  Compose fails to resolve `env_file`.

### Build and run

```bash
# Build the backend image and start both containers in the background
docker compose up -d --build

# Check container status
docker compose ps

# Follow backend logs
docker compose logs -f backend

# Stop and remove containers (database volume is preserved)
docker compose down

# Stop and also delete the database volume
docker compose down -v
```

### Applying migrations in the container

The `Dockerfile` `CMD` starts Uvicorn directly; it does not run migrations. Apply them
once after the containers are up:

```bash
docker compose exec backend alembic upgrade head
```

---

## 14. Environment Variables

Configuration is read by `app/core/settings.py` from environment variables, with a
local `.env` file as the source. **`.env` is git-ignored and excluded from the Docker
build — never commit real values.**

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | Async PostgreSQL DSN for the application, e.g. `postgresql+asyncpg://<user>:<password>@localhost:5432/<database>` |
| `TEST_DATABASE_URL` | Yes | — | Separate async DSN used only by the test suite; must point at a **different** database than `DATABASE_URL` |
| `SECRET_KEY` | Yes | — | Secret used to sign and verify JWTs. Generate a strong random value |
| `ALGORITHM` | No | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Access token lifetime in minutes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Yes | — | Refresh token lifetime in days |

### Template (placeholders only)

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@localhost:5432/<database>

TEST_DATABASE_URL=postgresql+asyncpg://<user>:<password>@localhost:5432/<test_database>

SECRET_KEY=<your_secret_key>

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7
```

`.env.example` in the repository provides a starting template.

> **Gap worth noting:** `.env.example` currently documents `DATABASE_URL`, `SECRET_KEY`,
> `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and `REFRESH_TOKEN_EXPIRE_DAYS`, but not
> `TEST_DATABASE_URL`. Because `TEST_DATABASE_URL` has no default in `Settings`, the
> application cannot start (and the tests cannot run) until it is supplied in `.env`.
> Adding it to `.env.example` is a small pending improvement.

### Generating a secret key

`app/core/key.py` is a helper that prints a freshly generated URL-safe random key:

```bash
python app/core/key.py
```

Use the printed value for `SECRET_KEY`. Rotating this key invalidates all existing
access and refresh tokens.

---

## 15. Local Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 16 — provided via Docker
- Docker and Docker Compose
- `pip`

### 1. Clone the repository

```bash
git clone https://github.com/Gitsujay2004/Product_Management_System.git
cd Product_Management_System
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the environment

```bash
# Windows (Command Prompt)
env\Scripts\activate

# Windows (PowerShell)
.\env\Scripts\Activate.ps1

# macOS / Linux
source env/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure `.env`

Copy the template and fill in your own values:

```bash
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux
```

Then set `DATABASE_URL`, `TEST_DATABASE_URL`, `SECRET_KEY`, and
`REFRESH_TOKEN_EXPIRE_DAYS`. You can generate a secret key with:

```bash
python app/core/key.py
```

### 6. Start PostgreSQL

```bash
docker compose up -d postgres
```

This starts only the database service, leaving the API to run on your host.
Verify it is healthy:

```bash
docker compose ps
```

Optionally inspect the database directly:

```bash
docker exec -it product_postgre psql -U postgres -d product_management
```

### 7. Apply database migrations

```bash
alembic upgrade head
```

The schema is created by migrations, not by the application. When you change a model,
generate a revision:

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

### 8. Start the FastAPI application

```bash
uvicorn app.main:app --reload
```

The API is served at `http://127.0.0.1:8000`.

> If the app raises a `ValidationError` from `Settings` on startup, a required
> environment variable is missing from `.env` — most commonly `TEST_DATABASE_URL`.

### 9. Open the API documentation

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI — interactive API explorer |
| `http://127.0.0.1:8000/redoc` | ReDoc — reference-style API documentation |
| `http://127.0.0.1:8000/openapi.json` | Raw OpenAPI schema |

### 10. Run the tests

```bash
pytest
```

This uses `TEST_DATABASE_URL`, creates and drops its own tables, and never touches
`DATABASE_URL`.

---

## 16. Docker Setup

Run the full stack — PostgreSQL and the FastAPI backend — in containers.

```bash
# Build the backend image and start both services in the background
docker compose up -d --build

# Check container status
docker compose ps

# Follow the backend logs
docker compose logs -f backend

# Stop and remove the containers (keeps the postgres_data volume)
docker compose down

# Stop and remove containers plus the database volume
docker compose down -v
```

Then apply migrations inside the running backend container and open the docs:

```bash
docker compose exec backend alembic upgrade head
```

The API is then available at `http://localhost:8000`, with Swagger UI at
`http://localhost:8000/docs`.

> `.env` must exist in the project root before `docker compose up`, since the backend
> service references it through `env_file`.

---

## 17. API Documentation

FastAPI generates interactive documentation automatically; no extra configuration is
required.

| Endpoint | Description |
|---|---|
| `/docs` | **Swagger UI** — interactive explorer with per-endpoint "Try it out", grouped by the tags set on each router (`Authentication`, `Users`, `Products`, `Categories`, `Product Images`, `Sessions`) |
| `/redoc` | **ReDoc** — three-panel reference documentation rendered from the same OpenAPI schema |
| `/openapi.json` | The raw **OpenAPI** schema, suitable for client generators and tooling |

The schema reflects the declared response models, so generic envelopes such as
`DataResponse[ProductResponse]`, `MessageResponse`, and `ProductListResponse` are
documented alongside each operation. Rate limits, the `require_admin` dependency, and
global error handlers are not expressible in OpenAPI today and are described in this
README instead.

---

## 18. Database Migrations

Schema changes are managed with **Alembic**. There is no runtime `create_all`, so the
schema is reproducible and versioned across environments.

### Configuration

- `alembic.ini` points `script_location` at the `alembic/` directory and sets
  `prepend_sys_path = .` so the `app` package is importable.
- `alembic/env.py` imports all five models, sets `target_metadata = Base.metadata`,
  reads the URL from `settings.DATABASE_URL`, and executes migrations through an async
  engine with `NullPool` — the same driver the application uses.
- `alembic/script.py.mako` is the template for new revision files.
- `alembic/versions/` holds the committed revision history.

### Creating a migration

After modifying a model in `app/models/`:

```bash
alembic revision --autogenerate -m "add status column to products"
```

Always **review the generated script** before committing it — autogenerate detects
column and index changes reliably, but renames and certain constraint changes are often
missed. Edit `alembic/versions/<revision>.py` as needed.

### Applying migrations

```bash
# Upgrade to the latest revision
alembic upgrade head

# Upgrade one revision
alembic upgrade +1

# Revert the most recent revision
alembic downgrade -1

# Revert everything
alembic downgrade base
```

Inside Docker:

```bash
docker compose exec backend alembic upgrade head
```

### Checking migration status

```bash
# Show the current revision
alembic current

# Show the current and available revisions
alembic history --verbose

# List revisions and mark the ones not yet applied as current
alembic history --indicate-current
```

### Current revision history

| Revision | Description |
|---|---|
| `6722683572a5` | `update session token constraints` — widens `sessions.token` to `String(5000)` and adds the `uq_sessions_token` unique constraint |

---

## 19. Production Readiness

### Implemented

The following production-oriented capabilities are present in the current codebase:

- **Dockerized backend** — reproducible `python:3.11-slim` image, layered dependency
  install, non-reloading Uvicorn bound to `0.0.0.0`.
- **Container networking** — Compose bridge network with the database reached by
  service hostname, and a named volume for data persistence.
- **PostgreSQL** — production-grade relational store accessed through the async
  `asyncpg` driver.
- **Environment-based configuration** — every secret, DSN, and token lifetime is
  externalized; `.env` is git-ignored and excluded from the image.
- **JWT authentication** — bcrypt password hashing, signed access and refresh tokens,
  cryptographic expiry enforcement, and separate `type` claims so the token kinds
  cannot be confused.
- **Authorization** — role-based admin checks via a reusable FastAPI dependency, plus
  inactive-account enforcement on every authenticated request.
- **Session management** — refresh tokens persisted in the database so they can be
  revoked, with server-side expiry checks and cascade cleanup on user deletion.
- **Rate limiting** — SlowAPI limits on registration, login, and refresh, returning
  `429 Too Many Requests`.
- **Security headers** — `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`,
  and `Content-Security-Policy` on every response.
- **TrustedHost** — `Host`-header allow-list to block Host-header attacks.
- **CORS** — explicit origin, method, and header allow-list with credentials enabled and
  no wildcard origins.
- **Error handling** — global handlers for application, validation, integrity,
  rate-limit, and unhandled errors, all returning a consistent envelope with
  `500` responses deliberately generic.
- **Database migrations** — Alembic-driven, versioned, reversible schema changes instead
  of runtime table creation.
- **Automated tests** — 70 async tests against an isolated test database, covering auth,
  authorization, every CRUD resource, validation, and rate limiting.

### Not yet implemented

HTTPS/TLS termination, HSTS, Redis-backed distributed rate limiting, cloud deployment,
CI/CD pipelines, centralized monitoring, advanced observability (metrics/tracing), and
production log aggregation are **not** part of the current codebase. They are outlined
in [Future Improvements](#21-future-improvements).

---

## 20. Current Test Status

```
70 passed
```

The suite currently validates the backend's functional behaviour and its rate limiting:

- **Functional coverage** — registration, login, refresh, logout, current-user
  retrieval, and token rejection; full CRUD for products, categories, product images,
  and users; session lifecycle including refresh-after-logout rejection; pagination and
  validation error paths.
- **Authorization coverage** — non-admin users are explicitly verified to receive `403`
  on every admin-only endpoint, and unauthenticated requests to receive `401`.
- **Rate limiting coverage** — the login and register limits are verified to return
  `429` once exceeded, with limiter state reset per test for determinism.
- **Isolation** — all tests run against `TEST_DATABASE_URL` with tables created and
  dropped around each test, so the development and production databases are untouched.

Verified by running the suite in the current environment:

```
$ pytest -q
......................................................................   [100%]
70 passed in 106.69s (0:01:46)
```

All 70 tests pass with zero failures and zero errors.

No coverage percentage is claimed, as coverage tooling (`pytest-cov`) is not currently
configured.

---

## 21. Future Improvements

The following are reasonable next steps and are **not** currently implemented.

- **Redis-backed distributed rate limiting** — the current SlowAPI limiter uses
  in-process storage, so limits are per container and reset on restart. Moving to a
  shared Redis backend would make limits consistent across replicas.
- **Authentication on the product-image and session routes** — the
  `/product-images` and `/sessions` routers currently declare no authentication
  dependency; adding `get_current_user` (and `require_admin` for mutations) would close
  this gap. Returning refresh tokens from `GET /sessions/` should also be removed, and
  the same `HttpUrl` validation used for nested product images should be applied to the
  standalone product-image routes.
- **Unified error responses** — several endpoints still raise `HTTPException` and return
  FastAPI's `{"detail": ...}` body, as does one branch of `get_current_user`. Routing
  them through the custom exception classes would make every error response use the
  same envelope.
- **Externalized Docker credentials** — the PostgreSQL user, password, and database
  name are hard-coded in `docker-compose.yml` and should come from `.env` or a secrets
  manager, and the committed Compose stack should be limited to local development.
- **Dependency pinning** — `requirements.txt` currently has no version constraints, so
  builds are not reproducible. Pinning versions or committing a lock file would make
  container builds deterministic.
- **Configurable SQL echo** — the async engine is created with `echo=True`; this should
  be driven by an environment setting so SQL is not logged in production.
- **HTTPS and HSTS** — TLS termination plus a `Strict-Transport-Security` header and an
  optional HTTPS redirect middleware for production.
- **CI/CD pipeline** — automated linting, test execution, image builds, and deployment
  on every push.
- **Cloud deployment** — a managed container platform or orchestration setup for
  running the backend and PostgreSQL in production.
- **Centralized monitoring** — health/readiness probes, uptime checks, and metrics
  collection for request latency, error rate, and saturation.
- **Advanced observability** — distributed tracing and structured request logging with
  correlation IDs.
- **Production logging aggregation** — shipping logs to a centralized store with
  retention and alerting, rather than relying on container stdout.
- **Account management** — password reset, email verification, and password change for
  the current user.
- **Token rotation and revocation list** — rotating refresh tokens on each use and
  revoking access tokens before their natural expiry.
- **Query performance** — composite indexes on frequently filtered columns and
  keyset pagination for large product catalogues.
- **Code coverage reporting** — adding `pytest-cov` to measure and track coverage.
- **Refresh token hashing at rest** — storing a hash of the refresh token instead of
  the token itself.

---

## 22. License

License information has not yet been specified.
