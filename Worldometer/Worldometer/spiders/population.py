import scrapy


class PopulationSpider(scrapy.Spider):
    name = "population"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        table = response.css("tbody tr")

        for data in table:

            yield {
                'Index': data.css("tr td::text").get(),
                'Country (or dependency)': data.css("td a::text").get(),
                'Population (2023)': data.css("td:nth-child(3)::text").get(),
                'Yearly Change': data.css("td:nth-child(4)::text").get(),
                'Net Change': data.css("td:nth-child(5)::text").get(),
                'Density (P/Km²)': data.css("td:nth-child(6)::text").get(),
                'Land Area (Km²)': data.css("td:nth-child(7)::text").get(),
                'Migrants (net)': data.css("td:nth-child(8)::text").get(),
                'Fert.  Rate': data.css("td:nth-child(9)::text").get(),
                'Med. Age': data.css("td:nth-child(10)::text").get(),
                'Urban Pop %': data.css("td:nth-child(11)::text").get(),
                'World Share': data.css("td:nth-child(12)::text").get()
            }

