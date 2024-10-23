import json
from pymongo import MongoClient
from dataclasses import dataclass, asdict, field
from typing import List
import time
from datetime import datetime

# Dataclasses
@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    active: bool = True
    created_ts: float = field(default_factory=lambda: time.time())
    updated_ts: float = field(default_factory=lambda: time.time())  # Add updated_ts

# Parse JSON to User Class
def parse_user(data):
    # Parse roles, except 'active' role
    roles = [role.split('_')[-1] for role, value in data.items() if role.startswith('is_user_') and value and role != 'is_user_active']
    
    # Create preferences
    preferences = UserPreferences(timezone=data['user_timezone'])

    # Convert the creation timestamp to a float (timestamp)
    created_ts = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ").timestamp()

    # Create user object with updated_ts
    user = User(
        username=data['user'],
        password=data['password'],
        roles=roles,
        preferences=preferences,
        active=data.get('is_user_active', True),
        created_ts=created_ts,
        updated_ts=time.time() 
    )
    return user

# Import from JSON file to MongoDB
def import_users_from_file_to_mongodb(file_path, db_name='deepersysdb', collection_name='users'):
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://testsjuliarg:root@cluster0.3tvwf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") 
    db = client[db_name]
    collection = db[collection_name]
    
    # Load JSON from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
        users_data = data.get('users', [])  

        if not users_data:
            print("Users not found in json.")
            return

    # Insert each user into the database
    for user_data in users_data:
        user = parse_user(user_data)
        try:
            collection.insert_one(asdict(user))
            print(f"Usuario {user.username} inserted correctly.")
        except Exception as e:
            print(f"Error inserting user {user.username}: {e}")

if __name__ == "__main__":
    file_path = "../api/users.json" 
    import_users_from_file_to_mongodb(file_path)
