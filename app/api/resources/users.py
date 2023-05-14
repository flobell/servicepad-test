import os, shutil
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity
from app.api.decorators import http_exceptions_handler, jwt_required


api = Namespace(
    name='users', 
    description="Users namespace"
)


class UsersDto:
    
    user = api.model('user', {
        'id': fields.String(),
        'email': fields.String(),
        'fullname': fields.String(),
        'photo_url': fields.String(),
    })

    put_users = api.model('put_users', {
        'fullname': fields.String(),
        'photo_base64': fields.String(default=None, description="base64")
    })

    delete_users = api.model('delete_users', {
        'message': fields.String()
    })


@api.doc(security=['jwt'])
@api.route('', methods=['PUT', 'DELETE'], endpoint="users")
class UsersResource(Resource):
    method_decorators = [http_exceptions_handler, jwt_required]

    @api.expect(UsersDto.put_users, validate=True)
    @api.marshal_with(UsersDto.user)
    def put(self):
        """Update user data"""
        from app.database import db
        from app.database.models import User
        from app.schemas import UserSchema

        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()
        if not user:
            return dict({"message": "User not found"}), 404

        user.fullname = request.json.get("fullname", user.fullname)
        user.set_photo(request.json.get("photo_base64", None))   
        db.session.commit()

        user_schema = UserSchema()
        return user_schema.dump(user)

    @api.marshal_with(UsersDto.delete_users)
    def delete(self):
        """Delete current user"""
        from app.database import db
        from app.database.models import User

        current_user_id = get_jwt_identity()
        user: User = User.query.filter_by(id=current_user_id).first()
        if not user:
            return dict({"message": "User not found"}), 404

        # delete db data
        db.session.delete(user)
        db.session.commit()

        # delete stored files
        employee_folder = os.path.join("uploads","employees",str(user.id))
        absolute_path = os.path.join(os.getcwd(), employee_folder)
        if os.path.exists(absolute_path):
            shutil.rmtree(os.path.join("uploads","employees",str(user.id)))

        return dict({"message": "User deleted"})