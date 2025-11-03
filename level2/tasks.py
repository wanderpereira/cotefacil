# tasks.py
from .celery_config import app
from .crawler_runner import run_spider # Função do Scrapy Runner
from .api_client import send_products_callback
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

@app.task(name="process_scraping_job")
def process_scraping_job(job_data):
    """
    Celery Task:
    1. Recebe as credenciais (dict job_data).
    2. Executa scraping com run_spider.
    3. Envia para callback de produtos enviados para API.
    Retorna dict com status e quantidade de produtos encontrados/enviados.
    """
    fornecedor_user = job_data.get("usuario")
    fornecedor_pass = job_data.get("senha")
    logging.info(f"Worker processando job para o usuário: {fornecedor_user}")
    try:
        produtos_encontrados = run_spider(fornecedor_user, fornecedor_pass)
    except Exception as e:
        logging.error(f"Erro durante a execução do Scrapy: {e}")
        return {"status": "error", "message": f"Scraping failed: {e}"}
    try:
        send_products_callback(produtos_encontrados)
        return {"status": "success", "count": len(produtos_encontrados)}
    except Exception as e:
        logging.error(f"Erro no Callback da API: {e}")
        return {"status": "error", "message": f"Callback API failed: {e}"}