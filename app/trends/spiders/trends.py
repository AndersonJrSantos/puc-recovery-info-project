import scrapy

class TrendsSpider(scrapy.Spider):
    name = "trends"
    allowed_domains = ["trends.google.com.br"]
    start_urls = ["https://g1.globo.com/ultimas-noticias/"]

    def parse(self, response):
        for post in response.css('div.post'):
            yield{
                'titulo': post.css('h2.post-title::text').get(),
                'url': post.css('a::attr(href)').get(),
            }
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)