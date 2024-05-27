import scrapy


class G1NewsSpider(scrapy.Spider):
    name = "g1-news"
    allowed_domains = ["g1.globo.com"]
    start_urls = ["https://g1.globo.com/"]

    def parse(self, response):
        for noticia in response.css('div.bastian-feed-item'):
            yield {
                'titulo': noticia.css('a.feed-post-link::text').get(),
                'link': noticia.css('a.feed-post-link::attr(href)').get(),
            }

        next_page = response.css('a.load-more-link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
