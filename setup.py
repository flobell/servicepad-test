from os import path
from io import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="app",  # Required
    version="0.0.1",  # Required
    author="Pedro Flores",  # Optional
    author_email="manuelflores1795@gmail.com",  # Optional
    packages=find_packages(),
    python_requires=">=3.9.6",
    install_requires=["alembic==1.7.6; python_version >= '3.6'", 'aniso8601==9.0.1', "apscheduler==3.9.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'", "attrs==21.4.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'azure-cognitiveservices-vision-face==0.6.0', 'azure-common==1.1.28', "bcrypt==3.2.0; python_version >= '3.6'", 'certifi==2021.10.8', 'cffi==1.15.0', "charset-normalizer==2.0.12; python_full_version >= '3.5.0'", 'click==8.0.4', "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'dependency-injector[yaml]==4.39.1', "et-xmlfile==1.1.0; python_version >= '3.6'", 'flask==2.0.3', 'flask-apscheduler==1.12.3', 'flask-bcrypt==0.7.1', 'flask-cors==3.0.10', 'flask-marshmallow==0.14.0', 'flask-migrate==3.1.0', 'flask-restx==0.5.1', 'flask-script==2.0.6', 'flask-seeder==1.2.0', 'flask-sqlalchemy==2.5.1', "greenlet==1.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'gunicorn==20.1.0', "idna==3.3; python_version >= '3.5'", 'isodate==0.6.1', "itsdangerous==2.1.0; python_version >= '3.7'", "jinja2==3.0.3; python_version >= '3.6'", "jsonschema==4.4.0; python_version >= '3.7'", "mako==1.1.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "markupsafe==2.1.0; python_version >= '3.7'", "marshmallow==3.14.1; python_version >= '3.6'", "marshmallow-sqlalchemy==0.27.0; python_version >= '3.6'", 'msrest==0.6.21', "oauthlib==3.2.0; python_version >= '3.6'", 'openpyxl==3.0.9', 'phonenumbers==8.12.44', "psycopg2==2.9.3; python_version >= '3.6'", 'pycparser==2.21', 'pyjwt==2.3.0', "pyrsistent==0.18.1; python_version >= '3.7'", "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'python-dotenv==0.19.2', "python-http-client==3.3.7; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pytz==2021.3', "pytz-deprecation-shim==0.1.0.post0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'", "pyyaml==6.0; python_version >= '3.6'", "requests==2.27.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'", "requests-oauthlib==1.3.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'sendgrid==6.9.7', "setuptools==60.9.3; python_version >= '3.7'", "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "sqlalchemy==1.4.31; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'", "sqlalchemy-utils==0.38.2; python_version ~= '3.4'", 'starkbank-ecdsa==2.0.3', 'twilio==7.7.0', "tzdata==2022.1; python_version >= '2'", "tzlocal==4.1; python_version >= '3.6'", "urllib3==1.26.8; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'", "werkzeug==2.0.3; python_version >= '3.6'", 'wheel==0.37.1'],
    extras_require={
        "dev": [
            "pytest",
            "pytest-clarity",
            "pytest-dotenv",
            "pytest-flask",
        ]
    },
    entry_points={"console_scripts": ["app=app:cli"]},
)