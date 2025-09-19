API de Preços de Combustíveis da ANP
Este projeto consiste em uma API desenvolvida em Python com o framework FastAPI. Sua principal função é extrair, tratar e disponibilizar os dados mais recentes sobre os preços de combustíveis (Etanol e Gasolina) diretamente do site da Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP).

A aplicação é containerizada com Docker, facilitando sua execução e deployment.

Como Funciona
O fluxo de operação da API é o seguinte:

Acesso à Página da ANP: A aplicação acessa a página pública da ANP que lista os levantamentos de preços de combustíveis .

Web Scraping: Utilizando httpx e BeautifulSoup, o código faz o scraping do conteúdo HTML da página para encontrar o link da planilha de "Preços médios semanais" mais recente.

Download e Leitura da Planilha: Após encontrar o link, a API faz o download do arquivo Excel (.xlsx) em memória.

Processamento com Pandas: A planilha é lida com a biblioteca pandas . Os dados são então filtrados para exibir apenas as informações referentes a Etanol e Gasolina .

Estruturação dos Dados: As colunas de interesse são selecionadas (DATA INICIAL, DATA FINAL, ESTADO, PRODUTO, PREÇO MÉDIO REVENDA) e as datas são formatadas para o padrão dd-mm-AAAA .

Disponibilização via API: Os dados tratados são expostos através de um endpoint no formato JSON.

Endpoint da API
GET /precos
Este endpoint aciona o processo de busca e tratamento dos dados e retorna as informações em formato JSON.

Resposta em caso de sucesso:

JSON

{
  "status": "ok",
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
Resposta em caso de erro (ex: link não encontrado):

JSON

{
  "status": "erro",
  "mensagem": "Nenhum link encontrado."
}
Tecnologias Utilizadas
Backend: Python 3.13 , FastAPI .

Servidor ASGI: Uvicorn .

Requisições HTTP: httpx .

Web Scraping: BeautifulSoup4 .

Manipulação de Dados: Pandas, openpyxl .

Containerização: Docker.

Como Executar o Projeto
Pré-requisitos
Docker e Docker Compose instalados.

Execução com Docker
Clone o repositório:

Bash

git clone <url-do-seu-repositorio>
cd <nome-do-repositorio>
Construa a imagem Docker:

Bash

docker build -t anp-fuel-api .
Execute o container:

Bash

docker run -p 8000:8000 anp-fuel-api
A API estará disponível no endereço: http://localhost:8000/precos