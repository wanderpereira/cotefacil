# api_client.py
import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("CALLBACK_API_BASE_URL", "https://desafio.cotefacil.net")
CALLBACK_USER = os.getenv("CALLBACK_USER")
CALLBACK_PASS = os.getenv("CALLBACK_PASS")

logging.basicConfig(level=logging.INFO)

def authenticate_callback_api():
    """
    Realiza o signup (/oauth/signup) e obtém o token (/oauth/token)
    para autenticar na API de Callback.
    """
    # Primeiro tenta criar o usuário (signup)
    signup_url = f"{API_BASE_URL}/oauth/signup"
    try:
        response = requests.post(signup_url, json={"email": CALLBACK_USER, "password": CALLBACK_PASS}, timeout=5)
        response.raise_for_status() 
        logging.info("API Client: Usuário criado com sucesso na API de Callback.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code != 409:
             logging.error(f"API Client: Erro inesperado no signup: {e}")
        
    # Agora obtém o token de autenticação
    token_url = f"{API_BASE_URL}/oauth/token"
    response = requests.post(token_url, json={"email": CALLBACK_USER, "password": CALLBACK_PASS}, timeout=5)
    response.raise_for_status() # Lança exceção para status 4xx/5xx
    
    return response.json().get('access_token')

def send_products_callback(products):
    """
    Envia os produtos encontrados para o endpoint /produto da API de Callback.
    """
    
    token = authenticate_callback_api()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    logging.info(f"API Client: Enviando {len(products)} produtos para {API_BASE_URL}/produto...")
    
    # O worker deve fazer POST para /produto com os dados extraídos 
    response = requests.post(
        f"{API_BASE_URL}/produto",
        headers=headers,
        json=products 
    )
    
    response.raise_for_status()
    logging.info(f"API Client: Callback de produtos realizado com sucesso! Status: {response.status_code}")
    return response.json()