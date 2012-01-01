""" store.py

    Interacts with the backend database.
"""
from _store import (create_engine_and_session,
                    Article, Paragraph, Sentence, ImportanceLabel)
from util import local_path

engine, Session = create_engine_and_session(local_path('store.sqlite3'))

# --------------------------------------------------------------------------

def populate_labels():
    global important, not_important
    session = Session()
    #
    importance_labels = (session.query(ImportanceLabel)
                                .order_by(ImportanceLabel.id)
                                .all())
    if importance_labels:
        not_important, important = importance_labels
    else:
        not_important = ImportanceLabel(value=0)
        important = ImportanceLabel(value=1)
        session.add_all([not_important, important])
        session.commit()

populate_labels()

