from flask import url_for
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.database.models import User, Publication


class UserSchema(SQLAlchemySchema):
    """User schema"""
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    email = auto_field()
    password = auto_field(load_only=True)
    fullname = auto_field()

    photo_url = fields.Method('_serialize_photo_url')
    def _serialize_photo_url(self, obj):
        return url_for("api.files_id", file_id=obj.photo_file_id, _external=True) if obj.photo_file_id else None

    
# Publication Schema
class PublicationSchema(SQLAlchemySchema):
    """Publication schema"""
    class Meta:
        model = Publication
        load_instance = True

    id = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    title = auto_field()
    description = auto_field()
    priority = auto_field()
    status = auto_field()
    user_id = auto_field()
    user = fields.Nested(UserSchema, many=False)    

    time_since_publishment = fields.Method('_serialize_time_since_publishment')
    def _serialize_time_since_publishment(self, obj):
        from datetime import datetime
        time_difference = datetime.now() - obj.created_at
        
        return dict(
            days = time_difference.days,
            hours = time_difference.seconds // 3600,
            minutes = (time_difference.seconds // 60) % 60,
            seconds = time_difference.seconds % 60,
        )


