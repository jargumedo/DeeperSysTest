from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import database as dbase
import time

db = dbase.dbConnection()

app = Flask(__name__)
CORS(app)

# App routes
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(db['users'].find())
    users = [{**user, '_id': str(user['_id'])} for user in users]  # Convertir ObjectId a string
    return jsonify(users)

@app.route('/users', methods=['POST'])
def addUser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    roles = data.get('roles', [])
    timezone = data.get('preferences', {}).get('timezone')

    if username and password and roles and timezone:
        user = {
            'username': username,
            'password': password,
            'roles': roles,
            'preferences': {'timezone': timezone},
            'active': True,
            'updated_ts': time.time(),
            'created_ts': time.time()
        }
        db['users'].insert_one(user)
        return jsonify({'message': 'User created successfully'}), 200
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/users/<username>', methods=['GET'])
def get_user_by_username(username):
    user = db['users'].find_one({'username': username})
    if user:
        user['_id'] = str(user['_id'])  # Convertir ObjectId a string
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/delete/<string:username>', methods=['GET', 'POST'])
def delete(username):
    db['users'].delete_one({'username': username})
    return jsonify({'message': 'User deleted successfully'}), 200

from flask import request, jsonify

@app.route('/update/<string:username>', methods=['POST'])
def update(username):
    data = request.json
    new_username = data.get('username')
    password = data.get('password')
    roles = data.get('roles')
    active = data.get('active', False)
    preferences = data.get('preferences')

    if new_username and (password is not None) and roles is not None and preferences is not None:
        updated_user = {
            'username': new_username,
            'password': password,
            'roles': roles,
            'preferences': preferences,
            'active': active,
            'updated_ts': time.time()
        }

        # Actualiza el usuario basado en el username original
        result = db['users'].update_one({'username': username}, {'$set': updated_user})

        # Si el nombre de usuario se ha cambiado, actualiza el nombre en la base de datos
        if username != new_username:
            db['users'].update_one({'username': username}, {'$set': {'username': new_username}})

        if result.modified_count > 0:
            return jsonify({'message': f'User {new_username} updated successfully.'}), 200
        else:
            return jsonify({'message': 'No changes made to the user.'}), 200
    else:
        return notFound()



@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'Resource not found. ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000)
