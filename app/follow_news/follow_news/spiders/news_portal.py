import scrapy


class NewsPortalSpider(scrapy.Spider):
    name = "news_portal"
    allowed_domains = ["g1.globo.com"]
    start_urls = [
        "https://g1.globo.com/",
    ]

    max_pages = 10000
    pages_crawled = 0

    def parse(self, response):
        if self.pages_crawled >= self.max_pages:
            self.logger.info('Número máximo de páginas atingido, parando a raspagem.')
            return
        
        self.pages_crawled += 1

        page_title = response.css('title::text').get()
        all_paragraphs = response.css('p::text').getall()
        
        yield {
            'title': page_title,
            'paragraphs': all_paragraphs,
        }

        for href in response.css('a::attr(href)').getall():
            yield response.follow(href, self.parse)

