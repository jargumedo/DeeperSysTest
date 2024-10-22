from dataclasses import dataclass, field
from typing import List
import time

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
    updated_ts: float = field(default_factory=lambda: time.time())  # Agregar updated_ts

    def toDBCollection(self):
        return {
            'username': self.username,
            'password': self.password,
            'roles': self.roles,
            'preferences': self.preferences.__dict__, 
            'active': self.active,
            'created_ts': self.created_ts,
            'updated_ts': self.updated_ts  # Incluir updated_ts en la colección de la base de datos
        }
