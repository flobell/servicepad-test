import uuid, os, base64
from app.database import db

class BaseModel(db.Model):
    """Base DB Model Class"""

    # abstract model setup
    __abstract__ = True

    # columns definition
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class File(BaseModel):
    """File DB Model Class"""

    # columns definition
    filepath = db.Column(db.Text, nullable=False)

class User(BaseModel):
    """User DB Model Class"""

    # columns definition
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    photo_file_id = db.Column(db.Integer, db.ForeignKey("file.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)

    # relationships definition
    photo_file = db.relationship("File", backref=db.backref("photo_files", lazy=True))

    def set_photo(self, photo_base64: str):
        if photo_base64:
            # identify the file
            _id = uuid.uuid4().hex
            filename = _id + '.jpg'

            # if exits file then just rewrite on it
            if self.photo_file_id: 
                file: File = File.query.filter_by(id=self.photo_file_id).first()
                current_directory = os.getcwd()
                absolute_path = os.path.join(current_directory, file.filepath)

                with open(absolute_path, "wb") as f:
                    f.write(base64.decodebytes(photo_base64.encode('ascii')))
            else: 
                current_directory = os.getcwd()
                relative_path = os.path.join(os.path.join("uploads","employees",str(self.id)))
                directory = os.path.join(current_directory, relative_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                absolute_path = os.path.join(directory, filename)
                full_relative_file_path = os.path.join(relative_path, filename)
            
                with open(absolute_path, "wb") as f:
                    f.write(base64.decodebytes(photo_base64.encode('ascii')))

                file = File(filepath=full_relative_file_path)
                db.session.add(file)
                db.session.flush()
                db.session.refresh(file)

                self.photo_file_id = file.id
                db.session.commit()
                db.session.refresh(self)
        else: 
            if self.photo_file_id:
                file: File = File.query.filter_by(id=self.photo_file_id).first()
                current_directory = os.getcwd()
                absolute_path = os.path.join(current_directory, file.filepath)
                os.remove(absolute_path)
                self.photo_file_id = None
                db.session.delete(file)
                db.session.commit()
                db.session.refresh(self)

class Publication(BaseModel):
    """Publication DB Model Class"""

    # columns definition
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer)
    status = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    # relationships definition
    user = db.relationship("User", backref=db.backref("publications", lazy=True))

