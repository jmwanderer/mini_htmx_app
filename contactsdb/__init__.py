"""
Module level functions and variables for the contactdb

Use contactdb:app to access the wsgi application instance
"""
import os
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

    # Setup config parameters
    config = {
        # By default, the database file is just in the current directory
        "DB_PATH": os.environ.get("DB_PATH", "./")
    }
    app.config.update(**config)

    db_file = os.path.join(app.config["DB_PATH"], "contacts.sqlite")
    print(f"set db_path: {db_file}")
    sqlite.SqliteDB.set_db_config(db_file)

    # Register blueprints and routes
    from contactsdb.main import main_bp
    app.register_blueprint(main_bp)

    # Cleanup when app context is cleared at the end of a request
    app.teardown_appcontext(close_db)

    return app

app = create_app()
