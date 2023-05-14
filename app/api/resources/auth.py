from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from app.api.decorators import http_exceptions_handler, jwt_required


api = Namespace(
    name='auth', 
    description="Auth namespace"
)


class AuthDto:

    post_auth_signup = api.model('post_auth_signup', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'fullname': fields.String(required=True),
        'photo_base64': fields.String(required=False, default='base64 (OPTIONAL)')
    })

    post_auth_signup_response = api.model('post_auth_signup_response', {
        'id': fields.Integer(),
        'email': fields.String(),
        'fullname': fields.String(),
        'photo_url': fields.String()
    })

    post_auth_login = api.model('post_auth_login', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
    })

    post_auth_login_response = api.model('post_auth_login_response', {
        'message': fields.String(),
        'access_token': fields.String()
    })

    post_auth_logout_response = api.model('post_auth_logout_response', {
        'message': fields.String()
    })

    get_auth_users_current_response = api.model('get_auth_users_current_response', {
        'id': fields.Integer(),
        'email': fields.String(),
        'fullname': fields.String(),
        'photo_url': fields.String(default=None)
    })



@api.route('/signup', methods=['POST'], endpoint="auth_signup")
class AuthSignupResource(Resource):
    method_decorators = [http_exceptions_handler]

    @api.expect(AuthDto.post_auth_signup, validate=True)
    @api.marshal_with(AuthDto.post_auth_signup_response)
    def post(self):
        """sign up user"""
        from app.database import db
        from app.database.models import User
        from app.schemas import UserSchema

        email = request.json["email"]
        password: str = request.json["password"]
        hashed_password = current_app.bcrypt \
                                    .generate_password_hash(password, current_app.config.get("BCRYPT_LOG_ROUNDS")) \
                                    .decode("utf-8")
        fullname = request.json["fullname"]

        user = User(email=email, password=hashed_password, fullname=fullname)
        db.session.add(user)
        db.session.commit()

        user.set_photo(request.json.get("photo_base64"))

        db.session.refresh(user)
        user_schema = UserSchema()
        return user_schema.dump(user)


@api.route('/login', methods=['POST'], endpoint="auth_login")
class AuthLoginResource(Resource):
    method_decorators = [http_exceptions_handler]
    
    @api.expect(AuthDto.post_auth_login, validate=True)
    @api.marshal_with(AuthDto.post_auth_login_response)
    def post(self):
        """login user"""
        from app.database.models import User

        email = request.json["email"]
        password: str = request.json["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not current_app.bcrypt.check_password_hash(user.password, password):
            return dict(message="Invalid credentials"), 401

        access_token = create_access_token(identity=user.id)
        return dict(message="success",access_token=f'Bearer {access_token}'), 200


@api.doc(security=['jwt'])
@api.route('/logout', methods=['POST'], endpoint="auth_logout")
class AuthLogoutResource(Resource):
    method_decorators = [http_exceptions_handler, jwt_required]
    
    @api.marshal_with(AuthDto.post_auth_logout_response)
    def post(self):
        """logout user"""
        jti = get_jwt()["jti"]
        current_app.cache.set(jti, "blacklisted", timeout=300)
        return dict({"message": "Logout successful"})


@api.doc(security=['jwt'])
@api.route('/users/current', methods=['GET'], endpoint="auth_users_current")
class AuthUsersCurrentResource(Resource):
    method_decorators = [http_exceptions_handler, jwt_required]

    @api.marshal_with(AuthDto.get_auth_users_current_response)
    def get(self):
        """returns current user"""
        from app.database.models import User
        from app.schemas import UserSchema
        user_schema = UserSchema()
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()
        return user_schema.dump(user)

