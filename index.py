import scraper
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import os
import json
import sys


def test():
    print('done')
    global_word_count = dict()
    for line in open('./items.json'):
        data_line = json.loads(line)
        word_counts = data_line['text']
        sorted_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_counts:
            if key in global_word_count:
                global_word_count[key] += sorted_counts[key]
            else:
                global_word_count[key] = sorted_counts[key]
    global_word_count = {k: v for k, v in sorted(global_word_count.items(), key=lambda item: item[1], reverse=True)}
    print(global_word_count)


if len(sys.argv) > 0 and sys.argv[0] == 'crawl':
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

