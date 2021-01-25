import fnv
import numpy


class DFTable:
    def __init__(self, filepath=None, n_row=10000000):
        self.table = numpy.zeros(n_row, )
        self.length = n_row
        self.doc_count = 0
        if filepath:
            self.filepath = filepath
            self._load()    # for numpy greater than 1.16 this rasies error so use numpy verison <= 1.16.6
 
    def _hash(self, word):
        return fnv.hash(str.encode(word)) % self.length

    def _load(self):
        self.table, self.length, self.doc_count = numpy.load(self.filepath)

    def save(self, filepath):
        numpy.save(filepath, [self.table, self.length, self.doc_count])

    def getDF(self, word):
        return self.table[self._hash(word)]

    def addDF(self, word, num=1):
        self.table[self._hash(word)] += num

    def scanArticle(self, article):
        article = list(set(article))
        for word in article:
            self.addDF(word)
        self.doc_count += 1

if __name__ == '__main__':
    articles = [['a', 'b', 'c'], ['c']]
    _df = DFTable(n_row = 10)
    for article in articles:
        _df.scanArticle(article)
    _df.save("test.df.npy")
    _df = DFTable("test.df.npy")
    print("a: ", _df.getDF('a'))
    print("b: ", _df.getDF('b'))
    print("c: ", _df.getDF('c'))
