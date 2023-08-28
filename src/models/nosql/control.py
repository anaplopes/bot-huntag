from datetime import datetime

from bson import ObjectId
from mongoengine import (
    DateTimeField,
    Document,
    IntField,
    ObjectIdField,
    StringField,
)


class ControlModelNoSQL(Document):
    id = ObjectIdField(db_field="_id", primary_key=True, default=ObjectId)
    kit_id = IntField()
    kit_creation_date = StringField(max_length=10, null=True)
    file_name = StringField(max_length=100)
    action = StringField(max_length=20)
    status = StringField(max_length=20)
    detail = StringField(max_length=500, null=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "download_control", "indexes": ["file_name"]}
