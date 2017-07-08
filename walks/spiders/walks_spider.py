import scrapy

class WalkSpider(scrapy.Spider):
	name = 'walks'

	start_urls = ['https://www.aussiebushwalking.com/world']

	def parse(self, response):
		# Follow links to walks
		for href in response.css('.walkBox h4 a::attr(href)'):
			yield response.follow(href, self.parse_walk)

		# Follow link to next page
		# for href in response.css('.pagination .next  a::attr(href)'):
		# yield response.follow(href, self.parse)

	def parse_walk(self, response):
			
		def extract_with_css(query):
			return response.css(query).extract_first().strip()

		def is_walk_return(query):
			returnVar = response.css(query).extract_first()
			if returnVar != None:
				return 'y'
			else:
				return 'n'
		
		def duration_in_min(number, unit):
			durationTime = response.css(number)[1].extract()
			durationUnit = response.css(unit)[1].extract()
			
			if durationUnit == 'days':
				return durationTime*24*60
			elif durationUnit == 'hours':
				return durationTime*60
			elif durationUnit == 'mins':
				return durationTime
			else:
				return durationTime

		yield {
			'name': extract_with_css('div.intro h2::text'),
			'url': response.url,
			'state': response.url.split('/')[3],
			'location': extract_with_css('div.intro a::text'),
			'distance': response.xpath('//div[@class="homeLists"]/div/div[@class="stat"][2]/span/text()').extract(),
			'duration': response.xpath('//div[@class="homeLists"]/div/div[@class="stat"][3]/span/text()').extract(),
			'difficulty': extract_with_css('.stat div::text'),
			'features': response.css('.tagViewer .tagViewLabel::text').extract(),
			'description': extract_with_css('.midBar p::text'),
		}
