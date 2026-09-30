# ESSL Reports

Monorepo starter with a React + Vite frontend and a FastAPI backend.

## Requirements

- Node.js 20.19+ or 22.12+
- Python 3.10+

## Run locally

On Apple Silicon, if Node reports `Bad CPU type in executable`, put the native Homebrew installation first on `PATH`:

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

Install frontend dependencies from the repository root:

```bash
npm install
```

Start the API in one terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
npm run dev:api
```

Start the frontend in another terminal:

```bash
npm run dev
```

Open the Vite URL shown in the terminal. The frontend checks `GET http://localhost:8000/health` and displays the API status. FastAPI's interactive API docs are available at `http://localhost:8000/docs`.

To point the frontend at another API origin, create `frontend/.env.local` with:

```env
VITE_API_URL=http://localhost:8000
```

## Build

```bash
npm run build
```


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