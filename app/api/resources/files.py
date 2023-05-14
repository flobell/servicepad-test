import os, uuid
from flask import send_file
from flask_restx import Namespace, Resource, fields
from app.api.decorators import http_exceptions_handler


api = Namespace(
    name='files', 
    description="Uploads namespace"
)

@api.route("/<int:file_id>", methods=["GET"], endpoint='files_id')
class FilesResource(Resource):
    method_decorators = [http_exceptions_handler]

    def get(self, file_id):
        from app.database.models import File
        file: File = File.query.filter_by(id=file_id).first()
        if not file:
            return dict(message="File not found."), 404
            
        current_directory = os.getcwd()
        filepath = os.path.join(current_directory, file.filepath)

        return send_file(
            path_or_file=filepath,
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename=f'{file.id}.jpg'
        )
