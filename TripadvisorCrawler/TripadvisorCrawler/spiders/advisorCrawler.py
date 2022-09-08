import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from TripadvisorCrawler.items import TripadvisorCrawlerItem
from datetime import datetime


class AdvisorcrawlerSpider(CrawlSpider):
    name = 'CrawlAdviser'
    allowed_domains = ['tripadvisor.com.mx']
    start_urls = ['https://www.tripadvisor.com.mx/Restaurants-g150800-Mexico_City_Central_Mexico_and_Gulf_Coast.html']

    custom_settings = {
        'FEED_URI': 'tripadvisor_restaurants.csv',
        'FEED_FORMAT': 'csv',
        'CURRENT_REQUESTS': 100,  # Requests simultaneas
        'MEMUSAGE_LIMIT_MB': 2048,  # 2 gigas de memoria ram disponibles para no sobre cargar
        'ROBOTSTXT_OBEY': True,
        'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 0.25
    }

    restaurant_details = LinkExtractor(restrict_xpaths='//div[@class="YtrWs"]//div[@class="RfBGI"]//a')
    pagination = LinkExtractor(restrict_xpaths='//div[@class="unified pagination js_pageLinks"]/a')

    rule_page = Rule(pagination, follow=True)
    rule_restaurant_detail = Rule(restaurant_details, callback='parse_item', follow=False)



    rules = (
        rule_page,
        rule_restaurant_detail
    )


    def parse_item(self, response):
        now = datetime.now()
        extracted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        l = ItemLoader(item=TripadvisorCrawlerItem(), selector=response)
        l.add_xpath('restaurant_name', '//div[@class="acKDw w O"]/h1/text()')
        l.add_xpath('address', '//div[@class="vQlTa H3"][2]/span[1]//a/text()')
        l.add_xpath('prices_range', '//div[@class="BMlpu"]/div[1]/div[2]/text()')
        l.add_xpath('food_category', '//div[@class="BMlpu"]/div[2]/div[2]/text()')
        l.add_xpath('food_types', '//div[@class="BMlpu"]/div[3]/div[2]/text()')
        l.add_xpath('rating', '//div[@class="QEQvp"]/span[1]/text()')
        l.add_xpath('opinions', '//div[@class="QEQvp"]/a/text()')
        l.add_value('link', response.url)
        l.add_value('extracted_date', extracted_date)
        l.add_value('domain', response.url)

        yield l.load_item()
