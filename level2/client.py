# client.py
from tasks import process_scraping_job
from dotenv import load_dotenv
import os

load_dotenv()

# Dados que devem ser enfileirados para o worker do Celery
job_data = {
    "usuario": os.getenv("SERVMED_USER"), 
    "senha": os.getenv("SERVMED_PASS")
}

print(f"Enfileirando job para o usuário: {job_data['usuario']}...")

# Envia a tarefa para a fila
result = process_scraping_job.delay(job_data)

print(f"Tarefa enviada. ID da Tarefa Celery: {result.id}")
print("Execute o worker com: celery -A tasks worker -l info")