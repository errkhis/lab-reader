# Lab Reader

A FastAPI project initialized using `uv`.

## Features

- FastAPI for building APIs.
- `uv` for lightning-fast dependency management.
- Uvicorn for the ASGI server.

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd lab-reader
   ```

2. Sync dependencies:
   ```bash
   uv sync
   ```

### Running the Application

Start the development server:

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Documentation

- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`
