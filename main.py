from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
from url import url_base
 
app = FastAPI()
 
async def buscar_dados():
    url = url_base
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
 
            links = soup.find_all('a', string=lambda s: s and "Preços médios semanais" in s)
            if not links:
                raise Exception("Nenhum link para a planilha 'Preços médios semanais' foi encontrado.")
 
            link_relativo = links[0]['href']
            link_full = httpx.URL(url).join(link_relativo)
 
            resp_xlsx = await client.get(str(link_full))
            resp_xlsx.raise_for_status()
 
        except httpx.RequestError as exc:
            raise Exception(f"Ocorreu um erro de rede ao tentar acessar {exc.request.url!r}.") from exc
 
    df = pd.read_excel(BytesIO(resp_xlsx.content), header=9)
 
    produtos_desejados = [
        'ETANOL HIDRATADO',
        'GASOLINA ADITIVADA',
        'GASOLINA COMUM',
        'GLP',
        'OLEO DIESEL',
        'OLEO DIESEL S10'
    ]

    estados_desejados = [
        'DISTRITO FEDERAL',
        'GOIAS'
    ]
 
    df_filtrado = df[
        df['PRODUTO'].isin(produtos_desejados) &
        df['ESTADO'].isin(estados_desejados)
    ].copy()
 
    df_filtrado['DATA INICIAL'] = pd.to_datetime(df_filtrado['DATA INICIAL']).dt.strftime('%d-%m-%Y')
    df_filtrado['DATA FINAL'] = pd.to_datetime(df_filtrado['DATA FINAL']).dt.strftime('%d-%m-%Y')
 
    colunas = ['DATA INICIAL', 'DATA FINAL', 'ESTADO', 'PRODUTO', 'PREÇO MÉDIO REVENDA']
    df_final = df_filtrado[colunas]
 
    return df_final.to_dict(orient="records")
 
@app.get("/precos", summary="Obter Preços de Combustíveis", description="Retorna uma lista com os preços médios semanais para os combustíveis selecionados.")
async def get_precos():
    try:
        dados = await buscar_dados()
        return {"status": "ok", "timestamp": pd.Timestamp.now().isoformat(), "dados": dados}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# from fastapi import FastAPI
# import httpx
# from bs4 import BeautifulSoup
# import pandas as pd
# from io import BytesIO
# from datetime import datetime
# import oracledb
# from url import url_base

# app = FastAPI()


# ORACLE_USER = "USUARIO"
# ORACLE_PASSWORD = "SENHA"
# ORACLE_DSN = "host:porta/servico"

# async def buscar_dados():
#     async with httpx.AsyncClient(timeout=60) as client:
#         resp = await client.get(url_base)
#         resp.raise_for_status()
#         soup = BeautifulSoup(resp.text, 'html.parser')

#         links = soup.find_all('a', string=lambda s: s and "Preços médios semanais" in s)
#         if not links:
#             raise Exception("Nenhum link encontrado.")

#         link_relativo = links[0]['href']
#         link_full = httpx.URL(url_base).join(link_relativo)

#         resp_xlsx = await client.get(str(link_full))
#         resp_xlsx.raise_for_status()

#     df = pd.read_excel(BytesIO(resp_xlsx.content), header=9)
#     df_filtrado = df[df['PRODUTO'].str.contains('Etanol|Gasolina', case=False, na=False)]

#     df_filtrado['DATA INICIAL'] = pd.to_datetime(df_filtrado['DATA INICIAL']).dt.date
#     df_filtrado['DATA FINAL'] = pd.to_datetime(df_filtrado['DATA FINAL']).dt.date

#     colunas = ['DATA INICIAL', 'DATA FINAL', 'ESTADO', 'PRODUTO', 'PREÇO MÉDIO REVENDA']
#     df_final = df_filtrado[colunas]

#     return df_final

# def inserir_no_oracle(df):
#     conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
#     cur = conn.cursor()

#     cur.execute("TRUNCATE TABLE PRECOS_COMBUSTIVEIS")

#     for _, row in df.iterrows():
#         cur.execute("""
#             INSERT INTO PRECOS_COMBUSTIVEIS (DATA_INICIAL, DATA_FINAL, ESTADO, PRODUTO, PRECO_MEDIO_REVENDA)
#             VALUES (:1, :2, :3, :4, :5)
#         """, (
#             row['DATA INICIAL'],
#             row['DATA FINAL'],
#             row['ESTADO'],
#             row['PRODUTO'],
#             float(row['PREÇO MÉDIO REVENDA'])
#         ))

#     conn.commit()
#     cur.close()
#     conn.close()

# def ler_do_oracle():
#     conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
#     cur = conn.cursor()
#     cur.execute("SELECT DATA_INICIAL, DATA_FINAL, ESTADO, PRODUTO, PRECO_MEDIO_REVENDA FROM PRECOS_COMBUSTIVEIS")
#     colunas = [c[0] for c in cur.description]
#     dados = [dict(zip(colunas, row)) for row in cur]
#     cur.close()
#     conn.close()
#     return dados

# @app.post("/atualizar")
# async def atualizar():
#     try:
#         df = await buscar_dados()
#         inserir_no_oracle(df)
#         return {"status": "ok", "mensagem": f"{len(df)} registros inseridos no Oracle"}
#     except Exception as e:
#         return {"status": "erro", "mensagem": str(e)}

# @app.get("/precos")
# def get_precos():
#     try:
#         dados = ler_do_oracle()
#         return {"status": "ok", "total": len(dados), "dados": dados}
#     except Exception as e:
#         return {"status": "erro", "mensagem": str(e)}
