# ESSL Reports

## Overview

Employee attendance reporting and AI agent integration.

## API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/` | Health Check |
| POST | `/run-agent` | Run Agent |
| GET | `/test-essl/{employee_id}` | Test ESSL Connection |

## Run Agent

### Request JSON

```json
{
  "goal": "Did employee 1006 punch in today? If not, check employee 1382."
}
```

### Response JSON

```json
"string"
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/run-agent" \
-H "accept: */*" \
-H "Content-Type: application/json" \
-d '{
  "goal": "Did employee 1006 punch in today? If not, check employee 1382."
}'
```

## Local Setup

```bash
npm install
```

```bash
python -m venv .venv
```

```bash
pip install -r backend/requirements.txt
```

```bash
npm run dev:api
```

```bash
npm run dev
```

## Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI:

```text
http://localhost:8000/openapi.json
```