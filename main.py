from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
from datetime import datetime
from url import url_base

app = FastAPI()

async def buscar_dados():
    url = url_base
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        links = soup.find_all('a', string=lambda s: s and "Preços médios semanais" in s)
        if not links:
            raise Exception("Nenhum link encontrado.")

        link_relativo = links[0]['href']
        link_full = httpx.URL(url).join(link_relativo)

        resp_xlsx = await client.get(str(link_full))
        resp_xlsx.raise_for_status()

    df = pd.read_excel(BytesIO(resp_xlsx.content), header=9)
    df_filtrado = df[df['PRODUTO'].str.contains('Etanol|Gasolina', case=False, na=False)]

    df_filtrado['DATA INICIAL'] = pd.to_datetime(df_filtrado['DATA INICIAL']).dt.strftime('%d-%m-%Y')
    df_filtrado['DATA FINAL'] = pd.to_datetime(df_filtrado['DATA FINAL']).dt.strftime('%d-%m-%Y')

    colunas = ['DATA INICIAL', 'DATA FINAL', 'ESTADO', 'PRODUTO', 'PREÇO MÉDIO REVENDA']
    df_final = df_filtrado[colunas]

    return df_final.to_dict(orient="records")

@app.get("/precos")
async def get_precos():
    try:
        dados = await buscar_dados()
        return {"status": "ok", "dados": dados}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
