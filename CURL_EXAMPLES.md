# cURL Examples

## Health

```bash
curl http://127.0.0.1:8000/health
```

## Order status

Windows CMD:

```cmd
curl -X POST http://127.0.0.1:8000/api/agent/chat -H "Content-Type: application/json" -d "{\"session_id\":\"demo-1\",\"message\":\"Where is my order ORD-1005?\"}"
```

## Complaint workflow

```cmd
curl -X POST http://127.0.0.1:8000/api/workflows/complaint -H "Content-Type: application/json" -d "{\"session_id\":\"demo-2\",\"message\":\"My payment was deducted but my order failed.\"}"
```
