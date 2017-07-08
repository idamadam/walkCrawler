
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

			yield {
				'name': extract_with_css('div.intro h2::text'),
				'url': response.url,
				'state': response.url.split('/')[3],
				'location': extract_with_css('div.intro a::text'),
				'distanceNumber': extract_with_css('.stat .value::text'),
				'distanceUnit': extract_with_css('.stat .value + span::text'),
				'isReturn': extract_with_css('.stat .value + span + span::text'),
				'duration': response.css('.stat .value::text')[1].extract(),
				'durationUnit': response.css('.stat .value + span::text')[1].extract(),
				'difficulty': extract_with_css('.stat div::text'),
				'features': response.css('.tagViewer .tagViewLabel::text').extract(),
				'description': extract_with_css('.midBar p::text'),
			}
