import html2text
import re
from scrapy.settings.default_settings import COOKIES_ENABLED, DOWNLOAD_DELAY
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from itemov import Itemov
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize


def tokenizewords(text):
    nltk.download('stopwords')
    nltk.download('punkt')
    stopwords_ = stopwords.words('english')
    words = word_tokenize(text)
    tokenized_words = dict()
    for word in words:
        if word not in list(stopwords_):
            localword = word.lower()
            if localword in tokenized_words:
                tokenized_words[localword] += 1
            else:
                tokenized_words[localword] = 1
    return tokenized_words


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
            item = Itemov(text=text_dict)
            itemList.append(item)
        return itemList
