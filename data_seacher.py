from pymagnitude import *
import fetch
from fetch import db, Article
from tfidf import DFTable
import os
from annoy import AnnoyIndex
import logging
import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy
import random

class Seacher:
    def __init__(self, df_path='df.npy', annoy_path='index.ann', vec_model_path='wiki-news-300d-1M-subword.magnitude'):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.stop_words = stopwords.words('english')
        self.porter = PorterStemmer()
        self.dftable = DFTable()
        self.annoy = AnnoyIndex(300)
        self.vec_model = Magnitude(vec_model_path)
        if not os.path.isfile(df_path):
            logging.info("first use, building tf-idf table")
            self._build_tfidf()
            self.dftable.save(df_path)
            self.dftable = DFTable(df_path)
        self.dftable = DFTable(df_path)
        if not os.path.isfile(annoy_path):
            logging.info("for the first use, build annoy index")
            self._build_annoy()
            self.annoy.save(annoy_path)
            self.annoy = AnnoyIndex(300)
        self.annoy.load(annoy_path)

    def _tokenize_and_normalize(self, text):
        tokens = word_tokenize(text)
        words = list(filter(lambda word: word.isalpha() and word not in self.stop_words, tokens))
        stemmed = [self.porter.stem(word) for word in words]
        return stemmed

    def _get_sentence_vec(self, sentence):
        words = self._tokenize_and_normalize(sentence)
        _vec = self.vec_model.query(words)
        _weight = [self.dftable.getDF(word) for word in words]
        for i in range(len(words)):
            _vec[i] *= numpy.log(self.dftable.doc_count / (1 + _weight[i]))
        return numpy.mean(_vec, axis=0)

    def _build_tfidf(self):
        with db.atomic():
            for article in Article.select():
                self.dftable.scanArticle(self._tokenize_and_normalize(article.content))

    def _build_annoy(self):
        with db.atomic():
            for article in Article.select():
                _vecs = self._get_sentence_vec("{}\n{}\n{}\n{}".format(article.title, article.content, article.themes, article.nearby_station))
                self.annoy.add_item(article.id, _vecs)
        self.annoy.build(100)

    def search(self, text, step=0.02, limit=0.9, cascading=True):
        question_vec = self._get_sentence_vec(text)
        ids, ds = self.annoy.get_nns_by_vector(question_vec, 50, include_distances=True)
        ids = numpy.array(ids)
        ds = numpy.array(ds)
        for i in range(int(limit/step)+1):
            choices = ids[ds < (i * step)]
            if len(choices) > 0:
                return list(choices)
        return None

    def searchArticle(self, text):
        ids = self.search(text)
        if ids:
            _list = [{'content': "{} is locate at {}, near {} station. {}".format(article.title, article.address, article.nearby_station, article.content.replace("\n", ' '), ), 'url': article.url} for article in Article.select().where(Article.id.in_(ids))]
            return _list
        else:
            return None

if __name__ == '__main__':
    finder = Seacher()
    print('>> Where is the best seafood restaurant?')
    print(random.choice(finder.searchArticle('Where is the best seafood restaurant?')))
    print('>> Where is the best restaurant?')
    print(random.choice(finder.searchArticle('Where is the best restaurant?')))
    print('>> Where is a park I can take some rest?')
    print(random.choice(finder.searchArticle('Where is a park I can take some rest?')))
