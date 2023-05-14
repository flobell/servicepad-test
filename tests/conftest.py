"""Global pytest fixtures."""
import pytest, os
from main import app
from app.database import db
from flask_jwt_extended import create_access_token

def empty_folder(folder_path, exclude_file_name):
    """utility function to empty an specific folder and exclude some file"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename != exclude_file_name:
            os.remove(file_path)
        elif os.path.isdir(file_path):
            empty_folder(file_path, exclude_file_name)
            os.rmdir(file_path)

@pytest.fixture
def client(request):
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            def fin():
                with app.app_context():
                    empty_folder('uploads','.gitkeep')
                    db.drop_all()
                    db.session.remove()

            request.addfinalizer(fin)
            yield client

@pytest.fixture
def access_token(client):
    with app.app_context():
        from app.database.models import User
        user = User(email='test@example.com', password='password', fullname='Test User')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return create_access_token(identity=user.id)


@pytest.fixture
def user(client):
    with app.app_context():
        from app.database.models import User
        user = User(email='test2@example.com', password='password', fullname='Test User')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def publication(client, user):
    with app.app_context():
        from app.database.models import Publication
        publications = Publication(title='Test Publication', description='This is a test publication', priority=1, status="active", user_id=user.id)
        db.session.add(publications)
        db.session.commit()
        db.session.refresh(publications)
        return publications


@pytest.fixture
def file(client):
    with app.app_context():
        from app.database.models import File

        filename = 'test.test'
        current_directory = os.getcwd()
        relative_path = os.path.join(os.path.join("uploads","tests"))
        directory = os.path.join(current_directory, relative_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        absolute_path = os.path.join(directory, filename)
        full_relative_file_path = os.path.join(relative_path, filename)
    
        with open(absolute_path, "wb") as f:
            f.write(b"12345")

        file = File(filepath=full_relative_file_path)
        db.session.add(file)
        db.session.commit()
        db.session.refresh(file)

        return file