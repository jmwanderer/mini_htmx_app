"""
Database access functions for the createdb app
"""
from __future__ import annotations 
import os
import sqlite3
import contactsdb.models as models

class SqliteDB:
    """
    Provides access to models in an sqlite database
    """
    db_file = ""

    @classmethod
    def set_db_config(cls, database:str):
        """
        Specify the path to the database file.
        """
        cls.db_file = database

        # If path doesn't exist, create it
        data_dir = os.path.dirname(cls.db_file)
        if len(data_dir) > 0 and not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # if file doesn't exist, initialize with the schema
        if not os.path.exists(cls.db_file):
            path = os.path.join(os.path.dirname(__file__), "schema.sql")
            conn = sqlite3.connect(cls.db_file)
            with open(path) as f:
                conn.executescript(f.read())
            conn.close()

    @classmethod
    def open_db(cls):
        """
        Open a connection to the database
        """
        sqlitedb = SqliteDB()
        sqlitedb.conn = sqlite3.connect(SqliteDB.db_file)
        return sqlitedb

    def __init__(self):
        self.conn: sqlite3.Connection

    def close(self):
        """
        Close the database connection
        """
        self.conn.close()

    def add_contact(self, contact: models.Contact):
        """
        Add a contact to the database
        """
        # Generate a random ID
        cid = os.urandom(4).hex()
        self.conn.execute("INSERT INTO contacts (id, first_name, last_name, email, address, phone) VALUES (?, ?, ?, ?, ?, ?)",
               (cid, contact.first_name, contact.last_name, contact.email, contact.address, contact.phone))
        self.conn.commit()
        contact.contact_id = cid
        return cid

    def update_contact(self, contact: models.Contact) -> bool:
        """
        Change a contact in the database. Return true if a record is updated
        """
        cursor = self.conn.execute("UPDATE contacts SET first_name = ?, last_name = ?, email = ?, address = ?, phone = ? WHERE id = ?",
               (contact.first_name, contact.last_name, contact.email, contact.address, contact.phone, contact.contact_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def read_contact(self, contact_id: str) -> models.Contact:
        """
        Read a contact entry from the database.
        If not found, return a nullContact from the model
        """
        cur = self.conn.execute("SELECT first_name, last_name, email, address, phone FROM contacts WHERE id = ?",
                            (contact_id,))
        row = cur.fetchone()
        if row is None:
            return models.Contact.nullContact()
        return models.Contact(row[0], row[1], row[2], row[3], row[4], contact_id)

    def delete_contact(self, contact_id: str) -> bool:
        """
        Remove a contact from the database.
        Return true if a record is deleted.
        """
        cursor = self.conn.execute("DELETE FROM contacts WHERE id = ?",
                   (contact_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_contact_list(self, ) -> list[models.Contact]:
        """
        Return a ordered list of all contacts in the database
        """
        result = []
        cursor = self.conn.execute("SELECT first_name, last_name, email, address, phone, id FROM contacts ORDER BY last_name, first_name")
        for row in cursor.fetchall():
            result.append(models.Contact(row[0], row[1], row[2], row[3], row[4], row[5]))
        return result



