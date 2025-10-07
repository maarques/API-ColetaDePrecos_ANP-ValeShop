from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
from url import url_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, text

app = FastAPI()

DATABASE_URL = "postgresql+asyncpg://admin:admin@postgres-local:5432/combustivel"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class PrecoCombustivel(Base):
    __tablename__ = "precos_combustiveis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data_inicial = Column(Date)
    data_final = Column(Date)
    estado = Column(String(50))
    produto = Column(String(100))
    preco_medio = Column(Float)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def buscar_dados():
    url = url_base
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        links = soup.find_all("a", string=lambda s: s and "Preços médios semanais" in s)
        if not links:
            raise Exception("Nenhum link encontrado.")

        link_relativo = links[0]["href"]
        link_full = httpx.URL(url).join(link_relativo)

        resp_xlsx = await client.get(str(link_full))
        resp_xlsx.raise_for_status()

    df = pd.read_excel(BytesIO(resp_xlsx.content), header=9)

    produtos_desejados = [
        "ETANOL HIDRATADO",
        "GASOLINA ADITIVADA",
        "GASOLINA COMUM",
        "GLP",
        "OLEO DIESEL",
        "OLEO DIESEL S10",
    ]

    estados_desejados = ["DISTRITO FEDERAL", "GOIAS"]

    df_filtrado = df[
        df["PRODUTO"].isin(produtos_desejados) & df["ESTADO"].isin(estados_desejados)
    ].copy()

    df_filtrado["DATA INICIAL"] = pd.to_datetime(df_filtrado["DATA INICIAL"]).dt.date
    df_filtrado["DATA FINAL"] = pd.to_datetime(df_filtrado["DATA FINAL"]).dt.date

    colunas = [
        "DATA INICIAL",
        "DATA FINAL",
        "ESTADO",
        "PRODUTO",
        "PREÇO MÉDIO REVENDA",
    ]
    df_final = df_filtrado[colunas]

    return df_final

@app.post("/atualizar")
async def atualizar():
    try:
        df = await buscar_dados()
        async with SessionLocal() as session:

            await session.execute(text("TRUNCATE TABLE precos_combustiveis RESTART IDENTITY"))

            for _, row in df.iterrows():
                registro = PrecoCombustivel(
                    data_inicial=row["DATA INICIAL"],
                    data_final=row["DATA FINAL"],
                    estado=row["ESTADO"],
                    produto=row["PRODUTO"],
                    preco_medio=float(row["PREÇO MÉDIO REVENDA"]),
                )
                session.add(registro)

            await session.commit()

        return {"status": "ok", "mensagem": f"{len(df)} registros inseridos"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/precos")
async def get_precos():
    try:
        async with SessionLocal() as session:
            result = await session.execute(
                text("SELECT data_inicial, data_final, estado, produto, preco_medio FROM precos_combustiveis")
            )
            rows = result.fetchall()
            dados = [
                {
                    "DATA INICIAL": r[0].strftime("%d-%m-%Y"),
                    "DATA FINAL": r[1].strftime("%d-%m-%Y"),
                    "ESTADO": r[2],
                    "PRODUTO": r[3],
                    "PREÇO MÉDIO REVENDA": r[4],
                }
                for r in rows
            ]
        return {"status": "ok", "total": len(dados), "dados": dados}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
