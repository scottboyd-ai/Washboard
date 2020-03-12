import html2text
import re
from scrapy.settings.default_settings import COOKIES_ENABLED, DOWNLOAD_DELAY
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from itemov import Itemov
import nltk
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import word_tokenize


def tokenizewords(text):
    # nltk.download('stopwords')
    # nltk.download('punkt')
    stopwords_ = stopwords.words('english')
    stopwords_ = [x.lower() for x in stopwords_]
    words = word_tokenize(text)
    bigram_list = list(bigrams(text.split()))
    bigram_list = [(x.lower(), y.lower()) for x, y in bigram_list]
    words = [x.lower() for x in words]
    tokenized_words = dict()
    for word in words:
        if word not in list(stopwords_):
            localword = word.lower()
            if localword in tokenized_words:
                tokenized_words[localword] += 1
            else:
                tokenized_words[localword] = 1
    bigram_count = dict()
    for bigram in bigram_list:
        if bigram in bigram_count:
            bigram_count[bigram] += 1
        else:
            bigram_count[bigram] = 1
    ret_val = []
    ret_val.append(tokenized_words)
    ret_val.append(bigram_count)
    return ret_val


class MySpider(CrawlSpider):
    name = 'myspider'
    allowed_domains = ['lamusicblog.com']
    start_urls = ['http://lamusicblog.com/']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    settings = {
        COOKIES_ENABLED: False,
        DOWNLOAD_DELAY: 2
    }

    rules = (
        Rule(LinkExtractor(allow=('', )), callback='parse_item'),
    )

    def parse_item(self, response):
        itemList = []
        items = response.selector.getall()
        for localItem in items:
            text = html2text.html2text(localItem)
            text = text.replace('\r\n', ' ').replace('\n', ' ')
            text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text, flags=re.MULTILINE)
            text = re.sub('[^0-9a-zA-Z\s]+', '', text, flags=re.MULTILINE)
            text_dict = tokenizewords(text)
            item = Itemov()
            item['words'] = text_dict[0]
            item['bigram_list'] = text_dict[1]
            item['url'] = response.url
            itemList.append(item)
        return itemList
