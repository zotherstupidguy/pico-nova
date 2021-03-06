from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as Linx
from scrapy.contrib.spiders import Rule
from items import Torrent
from picolib import PicoSpider

class MiniSpider(PicoSpider):

    name = "piconova"
    start_urls = ["http://mininova.org"]
    allowed_domains = ["mininova.org"]
    
    deny_rules = ('/name', '/get/', '/comments', '/seeds', '/leech')
    torrent_links = '/tor/'
    category_links = ('/cat/', '/sub/')

    rules = (
        Rule(Linx(allow=torrent_links, deny=deny_rules), callback='parse_mininova_torrent', follow=True),
        Rule(Linx(allow=category_links, deny=deny_rules), callback='parse_category', follow=True)
    )

    xpath_dict = {
	'title': ('//*[@id="content"]/h1/text()',),
	'torrent': ('/html/body/div[3]/div[2]/div/h2/a/@href',
		    '/html/body/div[3]/div[2]/h2/a/@href'),
	'magnet': ('/html/body/div[3]/div[2]/div/a[2]/@href',
		   '/html/body/div[3]/div[2]/a[2]/@href'),
	'seeds': ('//*[@id="seedsleechers"]/span[1]/text()',),
	'leech': ('//*[@id="seedsleechers"]/span[2]/text()',),
	'size': ('/html/body/div[3]/div[4]/p[3]//text()',),
	'added': ('/html/body/div[3]/div[4]/p[4]//text()',),
	'updated': ('//*[@id="lastupdated"]/text()',),
	'category': ('//*[@id="specifications"]/p[2]/a[1]/text()',)
    }

    # mininova data needs some cleanup so we override this one
    def parse_mininova_torrent(self, response):
	page = Torrent()
        self.try_xpaths(page, self.xpath_dict, response)
        
	if len(page['torrent']) > 1:
            del page['torrent'][1]

        page['added'] = page['added'][2:]
        
	return page

spider = MiniSpider()
