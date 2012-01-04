from training import config
config.get_database_path = lambda: ':memory:' # for testing

from training.store import fetch_article, put_article

article_title = 'Hello, world'
sentence_1 = 'This is the first sentence.'
sentence_2 = 'This is another sentence'
sentence_3 = 'Here comes another sentence'

# This is the article format.
article_json = {
    'title': article_title,
    'paragraphs': [
        [{'content': sentence_1,
          'important': True },
         {'content': sentence_2,
          'important': False}],

        [{'content': sentence_3,
          'important': True}]
    ]
}

def test_fetch_article_json():
    populate_test_article()
    check_test_article()

def check_test_article():
    article_json_got = fetch_article(1)
    assert article_json_got == article_json

def populate_test_article():
    put_article(article_json)

