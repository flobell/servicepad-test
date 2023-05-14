from flask import Flask
from app.core import get_core_obj

app: Flask = get_core_obj().app()

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])