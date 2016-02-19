from app import application, flask_db, database

from models import *
from views import *

def create_tables():
    # Create table for each model if it does not exist.
    database.create_tables([Entry, Tag, EntryTags, FTSEntry], safe=True)


if __name__ == '__main__':
    create_tables()
    application.run(host='0.0.0.0', port=8000, debug=True)
