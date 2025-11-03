# crawler_runner.py
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
import os
import scrapy
import json
from dotenv import load_dotenv

load_dotenv()

class ServimedSpider(scrapy.Spider):
    name = 'servimed'
    LOGIN_API_URL = 'https://peapi.servimed.com.br/api/usuario/login'
    PRODUCTS_API_URL = 'https://peapi.servimed.com.br/api/produto'
    LOGIN_USER = os.getenv("SERVMED_USER")
    LOGIN_PASS = os.getenv("SERVMED_PASS")
    PRODUCTS_PAYLOAD = {
        "filtro":"", "pagina":1, "registrosPorPagina":100, "ordenarDecrescente":False, "colunaOrdenacao":"nenhuma", "clienteId":267511, "tipoVendaId":1, "fabricanteIdFiltro":0, "pIIdFiltro":0, "cestaPPFiltro":False, "codigoExterno":0, "codigoUsuario":22850, "promocaoSelecionada":"", "indicadorTipoUsuario":"CLI", "kindUser":0, "xlsx":[], "principioAtivo":"", "master":False, "kindSeller":0, "grupoEconomico":"", "users":[518565,267511], "list":True
    }

    def start_requests(self):
        """Inicia processo de login (POST)."""
        payload = {'usuario': self.LOGIN_USER, 'senha': self.LOGIN_PASS}
        self.logger.info(f"Enviando login como {self.LOGIN_USER}")
        yield scrapy.Request(
            url=self.LOGIN_API_URL,
            method='POST',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(payload),
            callback=self.after_login,
            dont_filter=True
        )

    def after_login(self, response):
        """Checa status do login, chama próximo passo em caso de sucesso."""
        if response.status in [200, 201]:
            self.logger.info("Login bem-sucedido. Cookies de sessão/acesso gerados.")
            return self.request_product_list()
        else:
            self.logger.error(f"Falha no login. Status: {response.status}")
    
    def request_product_list(self):
        """Solicita GET dos produtos autenticado com cookies da sessão."""
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://pedidoeletronico.servimed.com.br/',
        }
        self.logger.info("Fazendo GET autorizado na lista de produtos")
        return scrapy.Request(
            url=self.PRODUCTS_API_URL,
            method='GET',
            headers=headers,
            body=json.dumps(self.PRODUCTS_PAYLOAD),
            callback=self.parse_product_list
        )

    def parse_product_list(self, response):
        """Processa e faz yield dos produtos extraídos do JSON recebido."""
        if response.status == 200:
            try:
                product_data = response.json()
                self.logger.info(f"Recebidos {len(product_data)} itens.")
                for product in product_data:
                    yield {
                        'gtin': product.get('gtin'),
                        'codigo': product.get('codigo'),
                        'descricao': product.get('descricao'),
                        'preco_fabrica': product.get('preco_fabrica'),
                        'estoque': product.get('estoque'),
                    }
            except json.JSONDecodeError:
                self.logger.error("Resposta de produto não é JSON.")
        else:
            self.logger.error(f"Falha ao acessar lista de produtos. Status: {response.status}")

# Classe para coletar os itens em uma lista
class ProductCollector:
    def __init__(self):
        self.products = []

    def process_item(self, item, spider):
        self.products.append(item)
        return item

    def close_spider(self, spider):
        pass

@defer.inlineCallbacks
def run_spider(login_user, login_pass):
    """Roda o spider, aguarda a conclusão e retorna a lista de produtos."""
    
    collector = ProductCollector()
    
    settings = get_project_settings()
    # Não queremos que o Scrapy salve o arquivo JSON (desabilitado o Feed Export)
    settings.set('FEED_URI', None)
    
    # Adiciona o coletor como um pipeline temporário
    settings.set('ITEM_PIPELINES', {'__main__.ProductCollector': 1})

    runner = CrawlerRunner(settings)
    
    # Passa as credenciais como argumentos do spider
    yield runner.crawl('servimed', login_user=login_user, login_pass=login_pass)
    
    return collector.products # Retorna a lista de produtos coletada