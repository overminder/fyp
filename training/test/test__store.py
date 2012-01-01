import os
from training._store import (create_engine_and_session,
                             Article, Paragraph, Sentence, ImportanceLabel)
from training.util import local_path

def test_make_engine_and_session():
    db_path = local_path('test.db', __file__)
    engine, Session = create_engine_and_session(db_path)
    assert os.path.isfile(db_path)
    os.unlink(db_path)

def test_populate_database():
    engine, Session = create_engine_and_session() # defaults to memory
    session = Session()
    #
    not_important = ImportanceLabel(0)
    important = ImportanceLabel(1)
    article = Article('How to write interpreter')
    paragraph = Paragraph()
    sentence_1 = Sentence('Interpreter is usually slow.')
    sentence_2 = Sentence('And native code compiler is too expensive '
                          'to implement in terms of time, '
                          'complexity and correctness.')
    #
    session.add_all([not_important, important,
                     article, paragraph, sentence_1, sentence_2])
    sentence_1.importance_label = not_important
    sentence_2.importance_label = important
    paragraph.sentences = [sentence_1, sentence_2]
    article.paragraph = paragraph
    session.commit()
    #
    assert (session.query(Article)
                   .all() == [article])
    assert (session.query(Paragraph)
                   .all() == [paragraph])
    assert (session.query(Sentence)
                   .filter(Sentence.importance_label == important)
                   .all() == [sentence_2])
    assert (session.query(Sentence)
                   .join(ImportanceLabel)
                   .filter(ImportanceLabel.value == 0)
                   .all() == [sentence_1])

