"""
Module level functions and variables for the contactdb

Use contactdb:app to access the wsgi application instance
"""
from flask import Flask, g
import contactsdb.sqlite as sqlite

def get_db():
    """
    Get the open database from the app contact or create it
    """
    if "db" not in g:
        g.db = sqlite.SqliteDB.open_db()
    return g.db

def close_db(e=None):
    """
    Close an open database in the app context
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    # Database file is just in the current directory
    sqlite.SqliteDB.set_db_config("./contacts.sqlite")

    # Register blueprints and routes
    from contactsdb.main import main_bp
    app.register_blueprint(main_bp)

    # Cleanup when app context is cleared at the end of a request
    app.teardown_appcontext(close_db)

    return app

app = create_app()
