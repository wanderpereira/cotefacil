# crawler_runner.py
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy_app.spiders.servimed_spider import ServimedSpider 
from twisted.internet import reactor, defer
import os

# Classe para coletar os itens extraídos pelo Scrapy em uma lista
class ItemCollectorPipeline:
    def __init__(self):
        self.products = []

    def process_item(self, item, spider):
        self.products.append(dict(item))
        return item

@defer.inlineCallbacks
def run_spider(login_user, login_pass):
    """
    Roda o ServimedSpider programaticamente e coleta todos os resultados.
    Retorna uma Deferred (Twisted) que, quando resolvida, contém a lista de produtos.
    """
    
    collector = ItemCollectorPipeline()
    settings = get_project_settings()
    
    # 1. Configurações para o Worker
    settings.set('LOG_LEVEL', 'WARNING')
    settings.set('DOWNLOAD_DELAY', 0)
    settings.set('COOKIES_ENABLED', True) 
    settings.set('FEED_URI', None) # Desabilita Feed Export para não salvar em arquivo

    # 2. Configura o pipeline de coleta (usa a classe ItemCollectorPipeline)
    settings.set('ITEM_PIPELINES', {
        '__main__.ItemCollectorPipeline': 1 
    }, priority='cmdline') # Garante que o pipeline é usado
    
    # 3. Roda o spider com as credenciais fornecidas
    runner = CrawlerRunner(settings)
    
    yield runner.crawl(ServimedSpider, login_user=login_user, login_pass=login_pass)

   return collector.products # Retorna a lista de produtos coletada