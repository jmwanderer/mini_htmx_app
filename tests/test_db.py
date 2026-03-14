"""
Test functions for sqlite.db
"""
import os
import contactsdb.sqlite as sqlite
import contactsdb.models as models

TEST_DB_NAME = "test.sqlite"
FIRST = "Jim"
LAST = "Wanderer"
EMAIL = "JimWanderer@example.com"
ADDRESS = "PO Box 10\nPalo Alto, CA"
PHONE = "(555)555-5555"

NEW_FIRST = "Jim"

def test():
    """
    A test to run the functions in sqlite.py
    """
    # Initialize and open the database
    sqlite.SqliteDB.set_db_config(TEST_DB_NAME)
    db = sqlite.SqliteDB.open_db()

    # Add a contact to the DB
    contact = models.Contact(FIRST, LAST, EMAIL, ADDRESS, PHONE)
    db.add_contact(contact)

    # Read it back and verify expected values
    contact = db.read_contact(contact.contact_id)
    assert(contact.first_name == FIRST)
    assert(contact.last_name == LAST)
    assert(contact.email == EMAIL)
    assert(contact.address == ADDRESS)
    assert(contact.phone == PHONE)

    # Update the contact, re-read, and verity
    result = db.update_contact(contact)
    assert(result)
    contact = db.read_contact(contact.contact_id)
    assert(contact.first_name == FIRST)
    assert(contact.last_name == LAST)
    assert(contact.email == EMAIL)
    assert(contact.address == ADDRESS)
    assert(contact.phone == PHONE)

    # Read non-existant contact
    contact_2 = db.read_contact("IDNotExist")
    assert(contact_2.isNull())

    # Read list of contacts
    results = db.get_contact_list()
    assert(len(results) == 1)

    # Delete a contact
    result = db.delete_contact(contact.contact_id)
    assert(result)

    # Verify can't read it
    contact_2 = db.read_contact(contact.contact_id)
    assert(contact_2.isNull())
    
    # Read list of contacts
    results = db.get_contact_list()
    assert(len(results) == 0)
    os.unlink(TEST_DB_NAME)
    

if __name__ == "__main__":
    test()

