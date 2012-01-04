""" store.py

    This module is intended to be imported from application codes.
    It populates some labels and ensures the database connection.
"""
from _store import (create_engine_and_session,
                    Article, Paragraph, Sentence, ImportanceLabel)
from config import get_database_path

engine, Session = create_engine_and_session(get_database_path())
session = Session() # since we are in single-threaded environment, session
                    # could be shared between modules.

# --------------------------------------------------------------------------

important, not_important = None, None

def fetch_article(article_id):
    """ Fetch an article from the database.
    """
    article = (session.query(Article)
                      .filter_by(id=article_id)
                      .first())
    return article.dump_json()

def put_article(article_json):
    """ Put a new article into the database.
    """
    article = Article.load_json(article_json)
    session.add(article)
    session.commit()

def populate_labels():
    global important, not_important
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

