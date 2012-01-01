from training.store import (Article, Paragraph, Sentence, ImportanceLabel,
                            Session)

article_title = 'Hello, world'
session = Session()

def populate_test_article():
    article = session.query(Article).filter_by(id=1).first()
    if not article:
        article = Article(article_title)
        session.add(article)
        session.commit()
    return article

def test_crud_article():
    article = populate_test_article()
    #
    assert article.id == 1
    assert article.title == article_title

def test_crud_sentences():
    article = populate_test_article()
    if not article.paragraphs:
        paragraph_1 = Paragraph()
        paragraph_1.sentences = [Sentence('This is the first sentence.'),
                                 Sentence('This is another sentence')]
        paragraph_1.article = article
        paragraph_2 = Paragraph()
        paragraph_2.sentences = [Sentence('Here comes another sentence')]
        paragraph_2.article = article
        article.paragraphs = [paragraph_1, paragraph_2]
        session.commit()
    #
    assert len(article.paragraphs) == 2 # 2 paragraphs in this article
    assert len(session.query(Sentence)
                      .join(Paragraph)
                      .join(Article)
                      .filter(Article.id == article.id)
                      .all()) == 3 # 3 sentences in this article

