from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class OrigPost(Base):
    """ An original Stackoverflow post.
    """
    __tablename__ = 'orig_post'

    id = Column(Integer, primary_key=True)

    #: The original Stackoverflow post id.
    orig_id = Column(Integer)

    #: The question in JSON.
    question = Column(String)

    #: The answers in JSON.
    answers = Column(String)

    def __init__(self, orig_id, question, answers):
        self.orig_id = orig_id
        self.question = question
        self.answers = answers

    def __repr__(self):
        return '<OrigPost%d>' % self.orig_id

class SumPost(Base):
    """ An summarized Stackoverflow post.
    """
    __tablename__ = 'sum_post'

    id = Column(Integer, primary_key=True)

    #: Foreign key on OrigPost, the original post that this summarization
    #  belongs to.
    orig_post = relationship('OrigPost', backref=backref('sum_post'))

    #: Summary description.
    summary = Column(String)

    def __init__(self, orig_post, summary):
        self.orig_post = orig_post
        self.summary = summary

    def __repr__(self):
        return '<SumPost%d %s>' % (self.orig_id, self.summary)

