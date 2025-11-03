import scrapy
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ServimedSpider(scrapy.Spider):
    name = 'servimed'
    
    LOGIN_API_URL = 'https://peapi.servimed.com.br/api/usuario/login' 
    PRODUCTS_API_URL = 'https://peapi.servimed.com.br/api/produto' 

    # Busca credenciais do ambiente:
    LOGIN_USER = os.getenv("SERVMED_USER")
    LOGIN_PASS = os.getenv("SERVMED_PASS")

    PRODUCTS_PAYLOAD = {
        "filtro":"", "pagina":1, "registrosPorPagina":100, "ordenarDecrescente":False, "colunaOrdenacao":"nenhuma", "clienteId":267511, "tipoVendaId":1, "fabricanteIdFiltro":0, "pIIdFiltro":0, "cestaPPFiltro":False, "codigoExterno":0, "codigoUsuario":22850, "promocaoSelecionada":"", "indicadorTipoUsuario":"CLI", "kindUser":0, "xlsx":[], "principioAtivo":"", "master":False, "kindSeller":0, "grupoEconomico":"", "users":[518565,267511], "list":True
    }

    def start_requests(self):
        """Inicia o login na API. Retorna a requisição POST de login. Não espera retorno direto."""
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
        """Analisa resposta do login. Em caso de sucesso, solicita lista de produtos."""
        if response.status in [200, 201]:
            self.logger.info("Login bem-sucedido. Cookies de sessão/acesso gerados.")
            return self.request_product_list()
        else:
            self.logger.error(f"Falha no login. Status: {response.status}")

    def request_product_list(self):
        """Requisição autenticada da lista de produtos. Retorna uma Request Scrapy."""
        headers = {'Content-Type': 'application/json', 'Referer': 'https://pedidoeletronico.servimed.com.br/'}
        self.logger.info("Solicitando lista de produtos.")
        return scrapy.Request(
            url=self.PRODUCTS_API_URL,
            method='GET',
            headers=headers,
            body=json.dumps(self.PRODUCTS_PAYLOAD),
            callback=self.parse_product_list
        )

    def parse_product_list(self, response):
        """Processa JSON dos produtos. Faz yield de dicionário com campos mapeados: gtin, código, descrição, preço de fábrica, estoque."""
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
                self.logger.error("Resposta de produto não é JSON válido.")
        else:
            self.logger.error(f"Falha ao acessar lista de produtos. Status: {response.status}")
