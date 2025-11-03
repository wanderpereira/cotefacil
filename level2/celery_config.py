# celery_config.py
import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

# Instância do Celery. O nome 'cotefacil_worker' é o nome da aplicação.
app = Celery(
    'cotefacil_worker',
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=['tasks']  # Importa o módulo onde as tarefas estão definidas
)

# Configurações do Celery
app.conf.update(
    task_always_eager=False,  # Garante que a tarefa use a fila
    worker_prefetch_multiplier=1,
)