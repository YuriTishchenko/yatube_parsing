import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        # all_groups = response.css('a[href^="/group/"]') 
        all_groups = response.css('a.group_link::attr(href)')
        for group_link in all_groups:
            yield response.follow(group_link, callback=self.parse_group)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        yield {
            'group_name': response.css('h2::text').get().strip(),
            'description': response.css('p.group_descr::text').get(),
            # 'posts_count': response.css('div.h6 posts_count::text').get(),
            'posts_count': int(response.xpath('//div[@class="h6 text-muted posts_count"]').css('div::text').get().replace('Записей:', '').strip()),
            # 'posts_count': response.xpath('//div[contains(., "Записей:")]').get(),
        }
