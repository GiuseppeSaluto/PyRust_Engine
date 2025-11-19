# PyRust Engine (Mongo Edition) 🚀

A high-performance hybrid architecture that combines the flexibility of Python (Flask) with the speed of Rust and the scalability of MongoDB.

## 📋 Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Hybrid Architecture**: Python for API flexibility, Rust for computational performance
- **Microservices**: Decoupled services for scalability
- **MongoDB Integration**: NoSQL database for flexible data storage
- **Input Validation**: Comprehensive request validation on both layers
- **Error Handling**: Graceful error responses with proper HTTP status codes
- **Security Headers**: CORS, XSS protection, and other security best practices
- **Health Checks**: Service health monitoring endpoints
- **Docker Ready**: Full containerization with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐
│   Client        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  Core API (Py)  │────▶│ Pricing Engine   │
│  Port: 5000     │     │ (Rust)           │
│  - Flask        │     │ Port: 8080       │
│  - Validation   │     │ - Actix-web      │
│  - CORS         │     │ - Fast compute   │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│   MongoDB       │
│   Port: 27017   │
└─────────────────┘
```

### Services:
- **core_api_py**: Flask API Gateway. Handles user requests, validation, and DB operations
- **pricing_engine_rs**: Rust microservice. Performs heavy computational tasks
- **mongo**: MongoDB for NoSQL data persistence

## 📦 Prerequisites

- Docker (20.10+)
- Docker Compose (1.29+)
- Git

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd PyRust_Engine
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 3. Start the services

```bash
docker-compose up --build
```

### 4. Verify the services are running

```bash
# Check Python API
curl http://localhost:5000/

# Check health endpoint
curl http://localhost:5000/health
```

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### `GET /`
Get API information and available endpoints.

**Response:**
```json
{
  "message": "Core API Python (Mongo Edition) is running!",
  "version": "1.0.0",
  "endpoints": [
    {
      "path": "/calculate_price",
      "method": "POST",
      "description": "Calculate price using Rust engine"
    }
  ]
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "core_api"
}
```

#### `POST /calculate_price`
Calculate price using the Rust pricing engine.

**Request Body:**
```json
{
  "base_price": 100,
  "factor": 1.2
}
```

**Validation Rules:**
- `base_price`: Required, must be a non-negative number, max value: 1,000,000
- `factor`: Required, must be a non-negative number

**Success Response (200):**
```json
{
  "success": true,
  "api_source": "Python Flask Layer",
  "db_type": "MongoDB",
  "rust_computation": {
    "final_price": 120.0,
    "processed_by": "Rust High-Performance Engine v1.0.0"
  }
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input
```json
{
  "error": "'base_price' must be non-negative"
}
```

- `503 Service Unavailable`: Rust engine unavailable
```json
{
  "success": false,
  "error": "Cannot connect to pricing engine"
}
```

- `504 Gateway Timeout`: Rust engine timeout
```json
{
  "success": false,
  "error": "Rust service timeout"
}
```

## 🔒 Security

### Implemented Security Measures

1. **Input Validation**: All inputs are validated before processing
2. **Security Headers**:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `X-XSS-Protection: 1; mode=block`
   - `Strict-Transport-Security`
3. **CORS**: Configured for cross-origin requests
4. **Error Handling**: No sensitive information exposed in error messages
5. **Timeouts**: Request timeouts to prevent hanging connections
6. **Environment Variables**: Sensitive data stored in `.env` (not committed)

### Security Best Practices for Production

- [ ] Use strong passwords for MongoDB (change from default)
- [ ] Configure CORS to allow only specific origins
- [ ] Enable HTTPS/TLS
- [ ] Implement authentication/authorization
- [ ] Add rate limiting
- [ ] Regular dependency updates
- [ ] Use secrets management (e.g., Docker secrets, Vault)
- [ ] Enable MongoDB authentication
- [ ] Use read-only file systems in containers
- [ ] Implement logging and monitoring

## 🛠️ Development

### Project Structure

```
PyRust_Engine/
├── core_api_py/           # Python Flask API
│   ├── app/
│   │   ├── __init__.py   # App factory with CORS and security
│   │   ├── models.py     # Data models
│   │   └── routes.py     # API routes with validation
│   ├── config.py         # Configuration management
│   ├── Dockerfile        # Python service container
│   └── requirements.txt  # Python dependencies
├── pricing_engine_rs/     # Rust microservice
│   ├── src/
│   │   ├── main.rs       # Main server with validation
│   │   └── pricing_logic.rs  # Business logic
│   ├── Cargo.toml        # Rust dependencies
│   └── Dockerfile        # Rust service container
├── docker-compose.yml     # Services orchestration
├── .env                   # Environment variables (not committed)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Running Tests

**Python:**
```bash
cd core_api_py
python -m pytest
```

**Rust:**
```bash
cd pricing_engine_rs
cargo test
```

### Local Development (without Docker)

**Python API:**
```bash
cd core_api_py
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

**Rust Service:**
```bash
cd pricing_engine_rs
cargo run
```

## 🚢 Production Deployment

### Environment Variables

Create a production `.env` file with secure values:

```bash
# Generate a secure password
openssl rand -base64 32

# Update .env with production values
MONGO_INITDB_ROOT_PASSWORD=<generated-password>
FLASK_ENV=production
FLASK_DEBUG=0
```

### Docker Compose Production

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Scaling Services

```bash
# Scale Rust pricing engine to 3 instances
docker-compose up -d --scale pricing_engine=3
```

## 🔧 Troubleshooting

### Services won't start

1. Check Docker is running:
```bash
docker info
```

2. Check port availability:
```bash
# Linux/Mac
lsof -i :5000
lsof -i :8080
lsof -i :27017

# Windows
netstat -ano | findstr :5000
```

3. View service logs:
```bash
docker-compose logs -f
```

### Cannot connect to Rust service

1. Verify Rust service is running:
```bash
docker-compose ps
```

2. Check Rust service logs:
```bash
docker-compose logs pricing_engine
```

3. Test direct connection:
```bash
curl -X POST http://localhost:8080/calculate \
  -H "Content-Type: application/json" \
  -d '{"base_price": 100, "factor": 1.2}'
```

### MongoDB connection issues

1. Verify MongoDB is running:
```bash
docker-compose ps mongo
```

2. Check MongoDB logs:
```bash
docker-compose logs mongo
```

3. Test MongoDB connection:
```bash
docker-compose exec mongo mongosh -u user -p password
```

## 📝 License

MIT License - feel free to use this project for learning and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ using Python 🐍 and Rust 🦀
