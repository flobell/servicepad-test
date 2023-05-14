from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity
from app.api.decorators import http_exceptions_handler, jwt_required


api = Namespace(
    name='publications', 
    description="Publications namespace"
)


class PublicationsDto:

    publication = api.model('publication', {
        'id': fields.Integer(),
        'created_at': fields.DateTime(),
        'updated_at': fields.DateTime(),
        'title': fields.String(),
        'description': fields.String(),
        'priority': fields.Integer(),
        'status': fields.String(),  
        'user': fields.Nested(api.model('publication_user',{
            'id': fields.String(),
            'email': fields.String(),
            'fullname': fields.String()
        })),
        'time_since_publishment': fields.Nested(api.model('publication_time_since_publishment',{
            'days': fields.Integer(),
            'hours': fields.Integer(),
            'minutes': fields.Integer(),
            'seconds': fields.Integer(),
        }))
    })
    
    post_publications = api.model('post_publications', {
        'title': fields.String(required=True),
        'description': fields.String(required=True),
        'priority': fields.Integer(),
        'status': fields.String()
    })

    get_publications_response = api.model('get_publications_response', {
        'data': fields.List(fields.Nested(publication))
    })

    put_publications_id = api.model('put_publications_id', {
        'title': fields.String(),
        'description': fields.String(),
        'priority': fields.Integer(),
        'status': fields.String()
    })

    put_publications_id_response = api.clone('put_publications_id_response', publication, {
        'message': fields.String(default='success')
    })

    delete_publications_id = api.model('delete_publications_id', {
        'message': fields.String()
    })




@api.doc(security=['jwt'])
@api.route("", methods=["POST", "GET"], endpoint="publications")
class PublicationsResource(Resource):
    method_decorators = [http_exceptions_handler, jwt_required]

    @api.expect(PublicationsDto.post_publications, validate=True)
    @api.marshal_with(PublicationsDto.publication)
    def post(self):
        """Create publication"""
        from app.database import db
        from app.database.models import Publication
        from app.schemas import PublicationSchema

        title = request.json["title"]
        description = request.json["description"]
        priority = request.json.get("priority")
        status = request.json.get("status")
        current_user_id = get_jwt_identity()

        publication = Publication(
            title=title,
            description=description,
            priority=priority,
            status=status,
            user_id=current_user_id,
        )

        db.session.add(publication)
        db.session.commit()
        db.session.refresh(publication)

        publication_schema = PublicationSchema()
        return publication_schema.dump(publication)

    @api.marshal_with(PublicationsDto.get_publications_response)
    def get(self):
        """Get a list of publication from current user"""
        from app.database.models import Publication
        from app.schemas import PublicationSchema
        current_user_id = get_jwt_identity()
        publications = Publication.query.filter_by(user_id=current_user_id).all()
        publications_schema = PublicationSchema(many=True)
        return dict(data=publications_schema.dump(publications))


@api.doc(security=['jwt'])
@api.route("/<int:publication_id>", methods=["GET", "PUT", "DELETE"], endpoint="publications_id")
class PublicationsIdResource(Resource):
    method_decorators=[http_exceptions_handler, jwt_required]

    @api.marshal_with(PublicationsDto.publication)
    def get(self, publication_id):
        """Get an specific publication by id"""
        from app.database.models import Publication
        from app.schemas import PublicationSchema
        
        publication = Publication.query.filter_by(id=publication_id).first()
        if not publication:
            return dict({"message": "Publication not found"}), 404
        
        publication_schema = PublicationSchema()
        return publication_schema.dump(publication)

    @api.expect(PublicationsDto.put_publications_id, validate=True)
    @api.marshal_with(PublicationsDto.put_publications_id_response)
    def put(self, publication_id):
        """Update a publication by id"""
        from app.database import db
        from app.database.models import Publication
        from app.schemas import PublicationSchema

        publication = Publication.query.filter_by(id=publication_id).first()
        if not publication:
            return dict({"message": "Publication not found"}), 404

        publication.title = request.json.get("title", publication.title)
        publication.description = request.json.get("description", publication.description)
        publication.priority = request.json.get("priority", publication.priority)
        publication.status = request.json.get("status", publication.status)
        db.session.commit()

        publication_schema = PublicationSchema()
        return publication_schema.dump(publication)

    @api.marshal_with(PublicationsDto.delete_publications_id)
    def delete(self, publication_id):
        """Delete a publication by id"""
        from app.database import db
        from app.database.models import Publication

        publication = Publication.query.filter_by(id=publication_id).first()
        if not publication:
            return dict({"message": "Publication not found"}), 404

        db.session.delete(publication)
        db.session.commit()

        return dict({"message": "Publication deleted"})