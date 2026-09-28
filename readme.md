## Run Agent API

### Endpoint

```http
POST /run-agent
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

### Swagger UI

```text
http://localhost:8000/docs
```


Add Run Agent API examples