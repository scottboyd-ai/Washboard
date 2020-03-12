import scraper
from wordcount import WordCount
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import os
import json
import sys


def test():
    global_word_count = dict()
    shrunk_line_list = []
    for line in open('./items.json'):
        data_line = json.loads(line)
        word_counts = data_line['words']
        sorted_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
        shrunk_list = {}
        for key in sorted_counts:
            if key in global_word_count:
                global_word_count[key].addCount(sorted_counts[key])
                global_word_count[key].incrementPageCount()
            else:
                global_word_count[key] = WordCount(key, sorted_counts[key])
            global_word_count = {k: v for k, v in sorted(global_word_count.items(), key=lambda item: item[1].count, reverse=True)}
            global_word_count_list = list(global_word_count)
            X = 5
            in_top_X = False
            for x in range(min(X, len(global_word_count))):
                if key == global_word_count_list[x]:
                    in_top_X = True
            if not(in_top_X):
                shrunk_list[key] = sorted_counts[key]
        shrunk_list = {k: v for k, v in sorted(shrunk_list.items(), key=lambda item: item[1], reverse=True)}
        shrunk_line_list.append(shrunk_list.copy())
    print(shrunk_line_list)


if len(sys.argv) > 1 and sys.argv[1] == 'crawl':
    if os.path.exists('./items.json'):
        os.remove('./items.json')

    process = CrawlerRunner(settings={
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'items.json'
    })

    d = process.crawl(scraper.MySpider)
    d.addBoth(lambda _: test())

    reactor.run()
else:
    test()

