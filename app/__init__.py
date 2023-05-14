import click, binascii, os
from app.core import get_core_obj

@click.group()
def cli():
    """General command line interface."""

@cli.group(help='Miscellaneous commands')
def misc():
    pass

@cli.group(help='Database commands')
def db():
    pass

@cli.group(help='Webserver commands')
def web():
    pass

@misc.command(help='Generate a key for flask configuration')
@click.option('--length', type=int, default=32)
def generate_key(length):
    """Generate random key and prints on terminal"""
    print('{}'.format(binascii.hexlify(os.urandom(length)).decode("utf-8")))


@db.command(help='Create all tables on database')
def create_all():
    if click.confirm('¡WARNING!: All database table will be created, continue?'):
        with get_core_obj().app().app_context():
            from app.database import db as database
            database.create_all()
        click.echo('¡Database tables created!')
    else:
        click.echo('Action aborted!')


@db.command(help='Drop all tables on database')
def drop_all():
    if click.confirm('¡WARNING!: All database table will be deleted, continue?'):
        with get_core_obj().app().app_context():
            from app.database import db as database
            database.drop_all()
        click.echo('¡Database tables deleted!')
    else:
        click.echo('Action aborted!')

@web.command(help='Run web dev server')
def run():
    app = get_core_obj().app()
    app.run(host=app.config['HOST'], port=app.config['PORT'])