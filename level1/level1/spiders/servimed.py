import scrapy
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ServimedSpider(scrapy.Spider):
    name = 'servimed'
    
    LOGIN_API_URL = 'https://peapi.servimed.com.br/api/usuario/login' 
    PRODUCTS_API_URL = 'https://peapi.servimed.com.br/api/produto' 
    
    # Carrega das variáveis de ambiente (ver .env):
    LOGIN_USER = os.getenv("SERVMED_USER")
    LOGIN_PASS = os.getenv("SERVMED_PASS")
    
    # Payload padrão para listar produtos
    PRODUCTS_PAYLOAD = {
        "filtro":"", 
        "pagina":1,
        "registrosPorPagina":100, 
        "ordenarDecrescente":False,
        "colunaOrdenacao":"nenhuma",
        "clienteId":267511, 
        "tipoVendaId":1,    
        "fabricanteIdFiltro":0,
        "pIIdFiltro":0,
        "cestaPPFiltro":False,
        "codigoExterno":0,
        "codigoUsuario":22850,
        "promocaoSelecionada":"",
        "indicadorTipoUsuario":"CLI",
        "kindUser":0,
        "xlsx":[],
        "principioAtivo":"",
        "master":False,
        "kindSeller":0,
        "grupoEconomico":"",
        "users":[518565,267511], # Ajuste este campo se necessário
        "list":True
    }

    def start_requests(self):
        # Verifica se as variáveis estão definidas no ambiente
        if not self.LOGIN_USER or not self.LOGIN_PASS:
            self.logger.error('Variáveis SERVMED_USER ou SERVMED_PASS não definidas! Configure-as no arquivo .env.')
            return
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
        """2. Verifica o login e, se sucesso, chama a listagem de produtos."""
        if response.status in [200, 201]:
            self.logger.info("Login bem-sucedido. Cookies de sessão/acesso gerados.")
            
            # --- Próxima Etapa: Chamar a listagem de produtos ---
            return self.request_product_list()
                
        else:
            self.logger.error(f"Falha no login. Status: {response.status}")


    def request_product_list(self):
        """
        3. Cria a requisição GET para /api/produto.
        O Scrapy irá anexar o header 'Cookie' (com sessiontoken e accesstoken)
        automaticamente a esta requisição.
        """
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://pedidoeletronico.servimed.com.br/',
        }
        
        self.logger.info("Fazendo GET autorizado na lista de produtos (rely on Scrapy Cookies).")
        
        return scrapy.Request(
            url=self.PRODUCTS_API_URL,
            method='GET',
            headers=headers,
            body=json.dumps(self.PRODUCTS_PAYLOAD),
            callback=self.parse_product_list
        )


    def parse_product_list(self, response):
        """
        4. Processa a lista de produtos (JSON) e extrai os campos.
        """
        if response.status == 200:
            self.logger.info("Lista de produtos recebida. Iniciando extração.")
            
            try:
                product_data = response.json()
                self.logger.info(f"Recebidos {len(product_data)} itens.")
                
                # Extraindo os 5 campos (GTIN, Código, Descrição, Preço de fábrica, Estoque)
                for product in product_data:
                    yield {
                        'gtin': product.get('gtin'),
                        'codigo': product.get('codigo'),
                        'descricao': product.get('descricao'), 
                        'preco_fabrica': product.get('preco_fabrica'), 
                        'estoque': product.get('estoque'),
                    }
                
            except json.JSONDecodeError:
                self.logger.error("Resposta de produto não é JSON. Olhe o payload.")
                
        else:
            self.logger.error(f"Falha ao acessar lista de produtos. Status: {response.status}")