from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.utils.response import get_base_url
from medcrawler.items import MedcrawlerItem
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request

class MySpider(CrawlSpider):
    name = 'spi'
    allowed_domains = ['321.portal.athenahealth.com']
    start_urls = ['https://6078.portal.athenahealth.com/']

    extractor = SgmlLinkExtractor()

    rules = (
        Rule(extractor,callback='parse_links',follow=True),
        )

    def parse_start_url(self, response):
        list(self.parse_links(response))

    def parse_links(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//a')
        for link in links:
            title = ''.join(link.select('./@title').extract())
            url = ''.join(link.select('./@href').extract())
            meta={'title':title,}
            cleaned_url = "%s/?1" % url if not '/' in url.partition('//')[2] else "%s?1" % url
            yield Request(cleaned_url, callback = self.parse_page, meta=meta,)

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        item=MedcrawlerItem()
        item['url'] = response.url
        item['title']=response.meta['title']
        item['h1']=hxs.select('//h1/text()').extract()
        return item
