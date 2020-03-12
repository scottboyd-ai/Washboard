class WordCount:

    def __init__(self, word, count):
        self.word = word
        self.count = count
        self.pageCount = 1

    def incrementPageCount(self):
        self.pageCount += 1

    def addCount(self, count):
        self.count += count
