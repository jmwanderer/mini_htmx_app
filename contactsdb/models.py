"""
Data models for the contactdb application
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Contact:
    # Note: order defines arguments in __init__
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    address: str = ""
    phone: str = ""
    contact_id: str = ""

    # Class singleton variable
    null_contact: ClassVar[Contact] | None = None

    def __repr__(self):
        return f"Contact(id={self.contact_id}, first={self.first_name} last={self.last_name}, email={self.email}, address={self.address}xa, phone={self.phone})"

    def isValid(self) -> bool:
        # Require a first and last name
        return len(self.first_name) > 0 and len(self.last_name) > 0

    def isNull(self) -> bool:
        """
        Was a record not found in the database?
        """
        return self == Contact.null_contact

    @classmethod 
    def nullContact(cls) -> Contact:
        """
        Used to indicate a contact is not found.
        Avoids using a None value in logic
        """
        if Contact.null_contact is None:
            Contact.null_contact = Contact("Null", "Contact")
        return Contact.null_contact
