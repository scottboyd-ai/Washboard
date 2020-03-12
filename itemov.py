import scrapy


def serialize_tuple(value):
    return str(value)


class Itemov(scrapy.Item):
    words = scrapy.Field()
    bigram_list = scrapy.Field(serializer=serialize_tuple)
    url = scrapy.Field()
