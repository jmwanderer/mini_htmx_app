"""
Application routes

We are using HTMX and serving portions of a web page.
"""
import flask
import contactsdb
import contactsdb.models as models

# Create a blueprint and register routs
main_bp = flask.Blueprint("contacts", __name__)

@main_bp.route("/")
def hello_world():
    """Top level view."""
    return flask.render_template("top.html")

@main_bp.route("/contacts")
def show_contact_list():
    """List of contacts with a create button """
    db = contactsdb.get_db()
    contacts = db.get_contact_list()
    return flask.render_template("contacts.html", contacts=contacts)

@main_bp.route("/create-contact")
def create_contact_form():
    """
    Produce an empty form for a contact
    """
    return flask.render_template("contact_form.html", contact=models.Contact())

@main_bp.route("/contact/<contact_id>/edit")
def edit_contact_form(contact_id):
    """
    Produce a populated form for a contact
    """
    db = contactsdb.get_db()
    contact = db.read_contact(contact_id)

    # If not found, refresh list
    if contact.isNull():
        return show_contact_list()

    return flask.render_template("contact_form.html", contact=contact)

@main_bp.route("/contact/", methods=["PUT"])
def new_contact():
    """Create a new contact """
    contact = models.Contact(
        flask.request.form["first_name"],
        flask.request.form["last_name"],
        flask.request.form["email"],
        flask.request.form["address"],
        flask.request.form["phone"],
    )
    if not contact.isValid():
        # don't allow to save
        return flask.render_template("contact_form.html", contact=contact)

    db = contactsdb.get_db()
    db.add_contact(contact)
    return flask.render_template("contact_show.html", contact=contact)

@main_bp.route("/contact/<contact_id>", methods=["GET", "PUT", "DELETE"])
def access_contact(contact_id):
    """ Show, update, or delete a contact"""
    db = contactsdb.get_db()
    if flask.request.method == "DELETE":
        db.delete_contact(contact_id)
        return show_contact_list()

    contact = db.read_contact(contact_id)
    # If not found, refresh list
    if contact.isNull():
        # don't allow to save
        return show_contact_list()

    if flask.request.method == "PUT":
        contact.first_name = flask.request.form["first_name"]
        contact.last_name = flask.request.form["last_name"]
        contact.email = flask.request.form["email"]
        contact.address = flask.request.form["address"]
        contact.phone = flask.request.form["phone"]
        if not contact.isValid():
            return flask.render_template("contact_form.html", contact=contact)
        db.update_contact(contact);

    return flask.render_template("contact_show.html", contact=contact)


