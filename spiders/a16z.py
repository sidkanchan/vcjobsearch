# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from vcjobsearch.items import VcjobsearchItem

def recursive_ascii_encode(list):
	ret = []
	for x in list:
		if isinstance(x, basestring):
			ret.append(x.encode('ascii', 'ignore'))
		else:
			ret.append(recursive_ascii_encode(x))
	return ret


class A16zSpider(scrapy.Spider):
    name = "a16z"
    allowed_domains = ["a16z.com"]
    start_urls = (
        'http://www.a16z.com/portfolio',
    )

    def parse(self, response):
		count = 0;
		items = []
		for sel in response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " company ")]'):
			item = VcjobsearchItem()
			companyName = sel.xpath('./div[@class="meta"]/div[1]/text()').extract()
			item['companyName'] = recursive_ascii_encode(companyName)
			companyLoc = sel.xpath('./div[@class="meta"]/div[3]/text()').extract()
			item['companyLoc'] = recursive_ascii_encode(companyLoc)
			companyType = sel.xpath('./div[@class="meta"]/div[6]/text()[2]').extract()
			item['companyType'] = recursive_ascii_encode(companyType)
			companyURL = sel.xpath('./div[@class="meta"]/div/a/@href').extract()
			companyURL = recursive_ascii_encode(companyURL)
			link = ''.join(companyURL)
			link = link.rstrip('/')
			item['companyURL'] = link

			try:
				jobsRequest = requests.get(link + "/jobs", verify=False)
			except requests.exceptions.Timeout as e:
				print e
			except requests.exceptions.RequestException as e:
				print e
			except requests.exceptions.ConnectionError as e:
				print e
				#r = "No Response"
			if jobsRequest.status_code < 400:
				item['companyJobs'] = link + "/jobs"
			else:
				try:
					careersRequest = requests.get(link + "/careers", verify=False)
				except requests.exceptions.Timeout as e:
					print e
				except requests.exceptions.RequestException as e:
					print e
				except requests.exceptions.ConnectionError as e:
					print e
					#r = "No Response"
				if careersRequest.status_code < 400:
					item['companyJobs'] = link + "/careers"


			yield item
