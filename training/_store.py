""" _store.py

    Deals with sqlalchemy infrastructure. This is used by store.py and
    is usually not directly imported.
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

def create_engine_and_session(path=':memory:', **kwargs):
    """ Create a sqlite engine at :path and a session factory for it.
    """
    engine = create_engine('sqlite:///%s' % path, **kwargs)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

class Article(Base):
    """ An article contains a title and many paragraphs.
    """
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return 'Article(%s)' % self.title
#
class Paragraph(Base):
    """ A paragraph belongs to an article. It contains many sentences.
    """
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship('Article', backref=backref('paragraphs',
                                                      order_by=id))
    def __repr__(self):
        return 'Paragraph(article_id=%s)' % self.article_id
#
class Sentence(Base):
    """ A sentence belongs to a paragraph. It contains many labels.
    """
    __tablename__ = 'sentence'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    paragraph_id = Column(Integer, ForeignKey('paragraph.id'))
    importance_label_id = Column(Integer, ForeignKey('importance_label.id'))

    paragraph = relationship('Paragraph', backref=backref('sentences',
                                                      order_by=id))
    importance_label = relationship('ImportanceLabel',
                                    backref=backref('sentences',
                                                    order_by=paragraph_id))
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return 'Sentence(%s)' % self.content
#
class ImportanceLabel(Base):
    """ ImportanceLabel's value is either 0 or 1.
    """
    __tablename__ = 'importance_label'

    id = Column(Integer, primary_key=True)
    value = Column(Integer)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'ImportanceLabel(%s)' % self.value

