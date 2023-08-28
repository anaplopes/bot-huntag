from datetime import datetime

from bson import ObjectId
from mongoengine import (
    DateTimeField,
    Document,
    IntField,
    ObjectIdField,
    StringField,
)


class KitModelNoSQL(Document):
    id = ObjectIdField(db_field="_id", primary_key=True, default=ObjectId)
    kit_id = IntField()
    kit_name = StringField(max_length=100)
    filter_to_kit = StringField(max_length=500, null=True)
    kit_creation_date = StringField(max_length=10, null=True)
    product_description = StringField(max_length=200, null=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "kits_info", "indexes": ["kit_id", "kit_name"]}
