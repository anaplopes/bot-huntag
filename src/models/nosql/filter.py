from datetime import datetime

from bson import ObjectId
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    ObjectIdField,
    StringField,
)


class FilterModelNoSQL(Document):
    id = ObjectIdField(db_field="_id", primary_key=True, default=ObjectId)
    category = StringField(max_length=50)
    subcategory1 = StringField(max_length=100)
    subcategory2 = StringField(max_length=100)
    subcategory3 = StringField(max_length=100)
    subcategory4 = StringField(max_length=100, null=True)
    subcategory5 = StringField(max_length=100, null=True)
    subcategory6 = StringField(max_length=100, null=True)
    dir_kit_name = BooleanField(default=False)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "filters", "indexes": ["category"]}
