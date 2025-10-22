# ⛽ API de Coleta de Preços de Combustíveis - ANP
<p align="center">
<img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13"/>
<img src="https://img.shields.io/badge/FastAPI-0.103.2-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
</p>

API para extração e consulta de dados semanais sobre preços de combustíveis, coletados diretamente do site da Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP).

O projeto utiliza web scraping para obter a planilha mais recente, processa os dados com Pandas e os armazena em um banco de dados PostgreSQL, disponibilizando-os através de endpoints REST.

✨ Principais Funcionalidades
Web Scraping Automatizado: Busca e faz o download da planilha de preços mais recente da ANP.

Processamento Inteligente: Utiliza Pandas para filtrar e tratar os dados de forma eficiente.

Armazenamento Robusto: Persiste os dados em um banco de dados PostgreSQL.

API Rápida: Disponibiliza os dados através de endpoints FastAPI assíncronos.

Containerizado: Pronto para rodar em qualquer ambiente com Docker.

🚀 Tecnologias Utilizadas
<p align="center">
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg" alt="fastapi" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original-wordmark.svg" alt="pandas" width="40" height="40"/> </a>
<a href="https://www.sqlalchemy.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlalchemy/sqlalchemy-original.svg" alt="sqlalchemy" width="40" height="40"/> </a>
</p>

📝 Endpoints da API
POST /atualizar
Dispara o processo de web scraping para buscar os dados mais recentes no site da ANP. Ele limpa a tabela existente (TRUNCATE) e a repopula com os novos dados.

Exemplo de Resposta (Sucesso):
'''
JSON

{
  "status": "ok",
  "mensagem": "150 registros inseridos"
}
GET /precos
Retorna todos os registros de preços de combustíveis atualmente armazenados no banco de dados.

Exemplo de Resposta:
```
JSON

{
  "status": "ok",
  "total": 2,
  "dados": [
    {
      "DATA INICIAL": "14-09-2025",
      "DATA FINAL": "20-09-2025",
      "ESTADO": "SAO PAULO",
      "PRODUTO": "GASOLINA COMUM",
      "PREÇO MÉDIO REVENDA": 5.75
    },
    {
      "DATA INICIAL": "14-09-2025",
      "DATA FINAL": "20-09-2025",
      "ESTADO": "SAO PAULO",
      "PRODUTO": "ETANOL HIDRATADO",
      "PREÇO MÉDIO REVENDA": 3.89
    }
  ]
}

⚙️ Como Executar o Projeto Localmente
Pré-requisitos:

Docker

Docker Compose

Passos para Execução:

Clone o repositório:

Bash```
git clone <url-do-seu-repositorio>
cd <nome-do-repositorio>
Inicie os containers com Docker Compose:
Este comando irá construir a imagem da API e iniciar os serviços da API e do banco de dados.
```

Bash```
docker-compose up --build
Acesse a API:
A API estará disponível em http://localhost:8000. Você pode acessar a documentação interativa (Swagger UI) em http://localhost:8000/docs.
```
