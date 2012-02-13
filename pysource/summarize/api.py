from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pysource.db.config import get_db_path
from pysource.db.schema import Base, OrigPost, SumPost

def create_engine_and_session(path=':memory:', **kwargs):
    """ Create a sqlite engine at :path and a session factory for it.
    """
    engine = create_engine('sqlite:///%s' % path, **kwargs)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

engine, Session = create_engine_and_session(get_db_path())

def get_all_posts():
    return Session().query(OrigPost).all()

def done_with_one_post(orig_post, summary):
    session = Session()
    sum_post = SumPost(orig_post, summary)
    session.add(sum_post)
    session.commit()

