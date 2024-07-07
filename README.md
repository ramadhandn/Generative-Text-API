# SEND REQUEST TO ENDPOINT

## DOCKER ENVIRONMENT

POST
```bash
curl \
    -X POST http://localhost:7151/generate-text \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"Sebutkan 3 komponen komputer\"}"
```

GET
```bash
curl \
    -X GET http://localhost:7151/generated-response \
    -H "Content-Type: application/json"
```

## LOCAL ENVIRONMENT

POST
```bash
curl \
    -X POST http://localhost:5000/generate-text \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"Sebutkan 3 komponen komputer\"}"
```

GET
```bash
curl \
    -X GET http://localhost:5000/generated-response \
    -H "Content-Type: application/json"
```

<br>

# DEPLOY & SHUTDOWN CONTAINER

Run
```bash
./setup.sh
```

Shutdown
```bash
./shutdown.sh
```
