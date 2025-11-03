import scrapy


class ServimedspiderSpider(scrapy.Spider):
    name = "ServimedSpider"
    allowed_domains = ["pedidoeletronico.servimed.com.br"]
    start_urls = ["https://pedidoeletronico.servimed.com.br/"]

    def parse(self, response):
        pass
