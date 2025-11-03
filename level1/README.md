# Documentação - Nível 1

## Descrição Geral
Este módulo executa a coleta de dados utilizando o framework Scrapy, realizando autenticação na API do Servimed para extrair dados de produtos e exportá-los em JSON. 

## Estrutura de Pastas
- `level1/` - Código principal do spider.
    - `items.py`, `middlewares.py`, `pipelines.py`, `settings.py` - Arquivos de configuração do Scrapy.
    - `spiders/servimed.py` - Spider responsável pela automação de login e coleta dos produtos via API.

## Como Executar
1. Instale as dependências requeridas (Scrapy, etc). 
2. Rode o spider com:
```bash
scrapy crawl servimed
```

Os resultados serão salvos em `produtos.json`. É possível configurar as credenciais no próprio spider.

## Pontos Importantes
- O spider realiza autenticação via endpoint protegido POST antes de coletar os produtos.
- Produtos extraídos: GTIN, Código, Descrição, Preço de fábrica, Estoque.

## Requisitos
- Python >= 3.10
- Scrapy

---
Autor: Wander Pereira da Silva
