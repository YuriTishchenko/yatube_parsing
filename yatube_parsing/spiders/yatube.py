import scrapy


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["51.250.32.185"]
    start_urls = [" http://51.250.32.185/"]

    def parse(self, response):
        print('|?||??|?|?|?|?|?|?|?|?|?|??||?')
        print(len(response.css('div.container div.card-body')))
        print('|?||??|?|?|?|?|?|?|?|?|?|??||?')
        for post in response.css('div.container div.card-body'):
            text = ' '.join(
                t.strip() for t in post.css('p::text').getall()
            ).strip()
            yield {
                'author': post.css('strong::text').get(),
                'text': text,
                'date': post.css('small::text').get(),
            }
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
