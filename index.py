import scraper
from wordcount import WordCount
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import os
import json
import sys
import time


def parse_items():
    global_word_count = dict()
    global_bigram_count = dict()
    shrunk_line_list = []
    shrunk_bigram_list = []
    for line in open('./items.json'):
        data_line = json.loads(line)
        local_shrunk_line_list = []
        blah = handle_data(data_line['words'], local_shrunk_line_list, global_word_count)
        shrunk_line_list.append(blah[0].copy())
        global_word_count.update(blah[1].copy())
        local_shrunk_line_list = []
        blah2 = handle_data(eval(data_line['bigram_list']), local_shrunk_line_list, global_bigram_count)
        shrunk_bigram_list.append(blah2[0].copy())
        global_bigram_count.update(blah2[1].copy())
    print(shrunk_line_list)


def handle_data(data_list, shrunk_line_list, global_list):
    print('still going' + str(time.time()))
    sorted_counts = {k: v for k, v in sorted(data_list.items(), key=lambda item: item[1], reverse=True)}
    shrunk_list = {}
    for key in sorted_counts:
        if key in global_list:
            global_list[key].addCount(sorted_counts[key])
            global_list[key].incrementPageCount()
        else:
            global_list[key] = WordCount(key, sorted_counts[key])
        global_list = {k: v for k, v in
                             sorted(global_list.items(), key=lambda item: item[1].count, reverse=True)}
        global_word_count_list = list(global_list)
        X = 5
        in_top_X = False
        for x in range(min(X, len(global_list))):
            if key == global_word_count_list[x]:
                in_top_X = True
        if not (in_top_X):
            shrunk_list[key] = sorted_counts[key]
    shrunk_list = {k: v for k, v in sorted(shrunk_list.items(), key=lambda item: item[1], reverse=True)}
    shrunk_line_list.append(shrunk_list.copy())
    retVal = list()
    retVal.append(shrunk_line_list)
    retVal.append(global_list)
    return retVal


if len(sys.argv) > 1 and sys.argv[1] == 'crawl':
    if os.path.exists('./items.json'):
        os.remove('./items.json')

    process = CrawlerRunner(settings={
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'items.json'
    })

    d = process.crawl(scraper.MySpider)
    d.addBoth(lambda _: parse_items())

    reactor.run()
else:
    parse_items()

