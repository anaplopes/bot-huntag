from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField, DateTimeField, ObjectIdField
from src.models.nosql.kit import KitModelNoSQL
from datetime import datetime
from bson import ObjectId


class ControlModelNoSQL(EmbeddedDocument):

    id = ObjectIdField(db_field="_id", primary_key=True, unique=True, default=ObjectId)
    kit_id = EmbeddedDocumentField(KitModelNoSQL)
    file_name = StringField(max_length=100)
    action = StringField(max_length=20)
    status = StringField(max_length=20)
    detail = StringField(max_length=500, null=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "download_control",
        "indexes": ["id", "file_name"]
    }
