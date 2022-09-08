import click

from core import app, db
from core.models import User

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def admin():
    user = User(name='admin')
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()
    click.echo('Done.')