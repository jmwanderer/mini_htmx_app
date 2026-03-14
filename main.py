"""
Run a debug instance with the flask server on 8080
"""
import os
import contactsdb


if __name__ == "__main__":
    contactsdb.app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

