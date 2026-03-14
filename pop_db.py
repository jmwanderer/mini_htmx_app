"""
Populate contact database with fake data
"""
import sys
import faker
import contactsdb
import contactsdb.models as models

fake = faker.Faker()

def gen_data_entry(db):
    """
    Add a contact with fake data
    """
    contact = models.Contact(fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.address(),
        fake.phone_number())
    db.add_contact(contact)
    print(f"Added {contact}")

if __name__ == "__main__":
    if len(sys.argv) != 2 or int(sys.argv[1]) == 0:
        print(f"Add fake data to the contacts database.")
        print(f"")
        print(f"Usage: {sys.argv[0]} <number of entries to add>")
        sys.exit(-1)

    count = int(sys.argv[1])
    print(f"Running populate database for {count} entries.")

    # Create a contactsdb app to access database
    with contactsdb.app.app_context():
        # Create count entries
        for _ in range(count):
            gen_data_entry(contactsdb.get_db())

    print(f"Populated {count} entries")

