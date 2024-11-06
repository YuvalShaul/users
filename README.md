# users
A demo Flask application.

## Test it

```
# Create user
curl -X POST http://localhost:5000/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'

# Get all users
curl http://localhost:5000/api/users

# Get specific user
curl http://localhost:5000/api/users/{user_id}
```