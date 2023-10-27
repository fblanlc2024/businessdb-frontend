import pymongo
from pymongo import MongoClient
import datetime

class Account:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.statistics = {
            "login_count": 0,
            "last_login": datetime.datetime.utcnow()
        }
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "statistics": self.statistics,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class GoogleAccount:
    def __init__(self, google_id, account_name, account_id):
        self.google_id = google_id  # New field for Google ID
        self.account_name = account_name
        self.account_id = account_id
        self.statistics = {
            "login_count": 0,
            "last_login": datetime.datetime.utcnow()
        }
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def to_dict(self):
        return {
            "google_id": self.google_id,  # Include Google ID in the dict
            "account_name": self.account_name,
            "account_id": self.account_id,
            "statistics": self.statistics,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }