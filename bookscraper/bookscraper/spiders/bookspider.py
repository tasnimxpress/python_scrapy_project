import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_url = book.css("h3 a ::attr(href)").get()
            if 'catalogue/' in book_url:
                book_page_url = 'https://books.toscrape.com/' + book_url
            else:
                book_page_url = 'https://books.toscrape.com/catalogue/' + book_url
            yield response.follow(book_page_url, callback=self.parse_book_page)

        next_page = response.css("li.next a ::attr(href)").get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)


    def parse_book_page(self, response):

        table_rows = response.css('table tr')

        yield {
            "url": response.url,
            "title": response.css(".product_main h1::text").get(),
            "category": response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get(),
            "product_type": table_rows[1].css('td ::text').get(),
            "price_excluded_tax": table_rows[2].css('td ::text').get(),
            "price_included_tax": table_rows[3].css('td ::text').get(),
            "price": response.css(".product_main p.price_color ::text").get(),
            "tax": table_rows[4].css('td ::text').get(),
            "rating": response.css("p.star-rating").attrib['class'],
            "num_reviews": table_rows[6].css('td ::text').get()
        }
