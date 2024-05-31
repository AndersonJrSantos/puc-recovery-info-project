import scrapy

class CheckNewsSpider(scrapy.Spider):
    name = "check_news"
    start_urls = [
        'https://g1.globo.com/'
    ]
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 11000,
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
      
        page_title = response.css('title::text').get()
        all_paragraphs = response.css('p::text').getall()
        
        yield {
            'title': page_title.strip(),
            'body': ' '.join(all_paragraphs).strip(),
        }

        for href in response.css('a::attr(href)').getall():
            yield response.follow(href, self.parse)


    # def parse(self, response):
    #     for body in response.css('p::text'):
    #         yield response.follow(body, self.parse_body)

    #     next_page = response.css('a::attr(href)').get()
    #     if next_page is not None:
    #         yield response.follow(next_page, self.parse)



    # def parse_body(self, response):
    #     title = response.css('title::text').get()
    #     body = response.css('p::text').getall()
    #     if title and body:
    #         yield {
    #             'title': title.strip(),
    #             'body': ' '.join(body).strip()
    #         }
