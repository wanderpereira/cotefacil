# Cotefacil - Desafio Python

Este projeto contempla dois desafios principais, construídos em Python, que abordam scraping de dados em API protegida e processamento assíncrono com envio de dados para API externa:

## 📌 Level 1 – Scraper (Coleta e Exportação)
- Desenvolve um spider Scrapy que autentica na API Servimed, coleta dados dos produtos e exporta resultados para um arquivo JSON.
- Todos os detalhes de configuração e execução encontram-se em `level1/README.md`.

## 📌 Level 2 – Celery, Fila e Callback
- Adiciona uma arquitetura de fila usando Celery e Redis para orquestrar a coleta automática e chamada de callback para uma API externa, simulando um cenário real de processamento assíncrono.
- Detalhes de setup, fluxo e código em `level2/README.md`.

## Configuração Inicial
- Copie `.env.example` para `.env` e preencha as variáveis (credenciais e endpoints).
- Sempre garanta que `.env` está incluído no `.gitignore` e não é versionado.

## Dependências Gerais
- Requisitos completos em cada subprojeto.
- Recomenda-se uso de ambiente virtual (ex.: `.venv/`).

---
Autor: Wander Pereira da Silva