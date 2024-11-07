from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory database (in real apps, use a proper database)
users = {}

# Middleware for logging
@app.before_request
def log_request():
    print(f"{datetime.now()}: {request.method} {request.path}")

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

# CREATE - POST /users
@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['name', 'email']):
        return jsonify({'error': 'Name and email are required'}), 400
    
    user_id = str(uuid.uuid4())
    new_user = {
        'id': user_id,
        'name': data['name'],
        'email': data['email'],
        'created_at': datetime.now().isoformat()
    }
    
    users[user_id] = new_user
    return jsonify(new_user), 201

# READ ALL - GET /users
@app.route('/api/users', methods=['GET'])
def get_users():
    # Handle pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Handle filtering
    name_filter = request.args.get('name')
    filtered_users = list(users.values())
    if name_filter:
        filtered_users = [u for u in filtered_users if name_filter.lower() in u['name'].lower()]
    
    # Calculate pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = filtered_users[start:end]
    
    return jsonify({
        'users': paginated_users,
        'total': len(filtered_users),
        'page': page,
        'per_page': per_page
    })

# READ ONE - GET /users/<id>
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

# UPDATE - PUT /users/<id>
@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['name', 'email']):
        return jsonify({'error': 'Name and email are required'}), 400
    
    users[user_id].update({
        'name': data['name'],
        'email': data['email'],
        'updated_at': datetime.now().isoformat()
    })
    
    return jsonify(users[user_id]), 200


# DELETE - DELETE /users/<id>
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    deleted_user = users.pop(user_id)
    return jsonify({
        'message': 'User deleted successfully',
        'user': deleted_user
    })



if __name__ == '__main__':
    app.run(debug=True)