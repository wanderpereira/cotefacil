# Documentação - Nível 2

## Descrição Geral
Este nível adiciona integração assíncrona via Celery, permitindo enfileiramento de jobs de scraping e callbacks automáticos, além de consumir dados de uma API protegida.

## Estrutura e Pastas 
- `api_client.py` – Envia dados extraídos para API externa e faz autenticação.
- `celery_config.py` – Configuração dos workers Celery.
- `client.py` – Consumer para disparar jobs de scraping.
- `crawler_runner.py` – Executa spiders Scrapy programaticamente.
- `tasks.py` – Tarefas Celery: coleta, processamento e callback dos produtos.
- `scrapy_pp/` – Projeto Scrapy desacoplado, com spiders, middlewares, etc.

## Fluxo Geral
1. `client.py` dispara um job com credenciais via Celery.
2. `tasks.py` processa o job: executa `run_spider`, coleta produtos e chama API callback.
3. Worker (Celery) executa cada job de scraping isoladamente.

## Como Executar
1. Instale dependências com Poetry:
```bash
poetry install
```
2. Inicie o worker Celery:
```bash
celery -A tasks worker -l info
```
3. Use `client.py` para enfileirar uma nova tarefa.

## Requisitos
- Python >=3.10
- Scrapy >=2.13
- Celery (com Redis), python-dotenv, requests

---
Autor: Wander Pereira da Silva
