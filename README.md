# veFastAPI Scaffold

This repository provides a scaffold FastAPI project with Docker support and pre-configured debugging capabilities using VS Code. It includes rate limiting by default using slowapi and configuration management with pydantic-settings.

## Features

- 🐳 Docker support with separate development and production configurations
- 🐞 Pre-configured debugging setup with debugpy
- 🚦 Built-in rate limiting with slowapi
- ⚙️ Environment-based configuration using pydantic-settings
- 🔍 Health check endpoint
- 📝 Comprehensive logging setup
- 🔒 CORS middleware configured
- 📚 Swagger UI (available only in development environment)
- ✅ Unit tests with pytest

## Prerequisites

- Python 3.12+
- Docker
- Visual Studio Code
- VS Code Python extension
- VS Code Docker extension

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/velais/veDocker-debug-python.git
cd veDocker-debug-python
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
env=Development
rate_limiter="5/minute"
```

## Development with Docker

### Running the Application

1. Build and run the development container:

```bash
docker build -f Dockerfile.debug -t vedocker-debug-python:dev .
docker run -p 8000:8000 -p 5678:5678 vedocker-debug-python:dev
```

2. The API will be available at: `http://localhost:8000`

### Debugging with VS Code

1. Open the project in VS Code
2. Set breakpoints in your code
3. Press F5 or use the Run and Debug panel to start debugging
4. The debugger will attach to the running container

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

This will execute all the tests in the `tests` directory and provide a summary of the results.

## API Documentation

### Swagger UI

When running in development mode (`env=Development`), the Swagger UI documentation is available at:

- http://localhost:8000/docs

The Swagger UI provides:

- Interactive API documentation
- Request/response examples
- Try-out functionality for all endpoints
- API schema visualization

Note: Swagger UI is intentionally disabled in production mode for security reasons.

## Detailed Project Structure

```
├── app/
│   ├── configuration/           # Application configuration
│   │   ├── __init__.py
│   │   ├── settings.py         # Environment and app settings
│   │   └── limiter.py          # Rate limiting configuration
│   │
│   ├── handlers/               # Custom exception handlers
│   │   ├── __init__.py
│   │   └── rate_limit_exceeded_handler.py
│   │
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── responses/        # Response models
│   │       ├── __init__.py
│   │       ├── health_response.py
│   │       └── rate_limit_exceeded_response.py
│   │
│   ├── routers/              # API route definitions
│   │   ├── __init__.py
│   │   └── health_check.py
│   │
│   ├── __init__.py
│   └── main.py              # Application entry point
│
├── tests/                   # Test cases
│   ├── test_health_check.py # Health check endpoint tests
│   └── test_rate_limit_exceeded.py # Rate limit exceeded tests
│
├── .vscode/                 # VS Code configuration
│   ├── launch.json         # Debug configuration
│   ├── settings.json      # Editor settings
│   └── tasks.json        # Build/run tasks
│
├── Dockerfile            # Production container configuration
├── Dockerfile.debug     # Development container with debugging
├── Dockerfile.prod     # Production-optimized container
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
├── .gitignore       # Git ignore rules
├── LICENSE         # MIT License
└── README.md      # Project documentation
```

### Key Components

- **configuration/**: Contains all configuration-related code

  - `settings.py`: Manages environment variables and app settings using pydantic-settings
  - `limiter.py`: Configures the rate limiting behavior

- **handlers/**: Custom exception handlers

  - `rate_limit_exceeded_handler.py`: Handles rate limit exceeded scenarios

- **models/**: Data models and schemas

  - `responses/`: Response models for API endpoints

- **routers/**: API route definitions

  - `health_check.py`: Health check endpoint implementation

- **tests/**: Test cases for the application

  - `test_health_check.py`: Tests for the health check endpoint
  - `test_rate_limit_exceeded.py`: Tests for rate limit exceeded scenarios

- **Docker Files**:
  - `Dockerfile`: Basic production container
  - `Dockerfile.debug`: Development container with debugging support
  - `Dockerfile.prod`: Optimized production container with security enhancements

## Rate Limiting

The application includes rate limiting by default using slowapi. To exempt a route from rate limiting, use the `@limiter.exempt` decorator:

```python
from app.configuration.limiter import limiter

@router.get("/my-endpoint")
@limiter.exempt
async def my_endpoint():
    return {"message": "This endpoint is not rate limited"}
```

## Configuration

Application settings are managed through environment variables and the `.env` file using pydantic-settings. Configure the following variables:

- `env`: Application environment (e.g., development or production)
- `rate_limiter`: Rate limiting rule (e.g., "5/minute")

## Production Deployment

For production deployment, use the production Dockerfile:

```bash
docker build -f Dockerfile.prod -t vedocker-debug-python:prod .
docker run -p 8000:8000 vedocker-debug-python:prod
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
