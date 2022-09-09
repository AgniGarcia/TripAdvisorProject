# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import replace_escape_chars, remove_tags
from urllib.parse import urlparse

def get_domain(response):
    parsed_uri = urlparse(response)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


class TripadvisorCrawlerItem(scrapy.Item):
    restaurant_name = scrapy.Field(
        output_processor=TakeFirst()
    )

    address = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars, remove_tags)
    )
    prices_range = scrapy.Field()

    food_category = scrapy.Field(
        output_processor=TakeFirst()
    )
    food_types = scrapy.Field(
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        output_processor=TakeFirst()
    )

    opinions = scrapy.Field(
        output_processor=TakeFirst()
    )

    link = scrapy.Field(
        output_processor=TakeFirst()
    )

    extracted_date = scrapy.Field(
        output_processor = TakeFirst()
    )

    domain = scrapy.Field(
        input_processor=MapCompose(get_domain),
        output_processor=TakeFirst()
    )

