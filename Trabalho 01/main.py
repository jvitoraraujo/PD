import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import threading
import uvicorn

app = FastAPI(title="API CRUD de Produtos")

data_lock = threading.Lock()

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    categoria: str
    preco: float

class Estatisticas(BaseModel):
    produto_maior_preco: dict
    produto_menor_preco: dict
    media_precos: float
    produtos_acima_media: List[dict]
    produtos_abaixo_media: List[dict]


def carregar_dados() -> pd.DataFrame:
    try:
        return pd.read_csv("produtos_db.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "nome", "categoria", "preco"])

def salvar_dados(df: pd.DataFrame):
    df.to_csv("produtos_db.csv", index=False)

@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    df = carregar_dados()
    return df.to_dict(orient='records')

@app.get("/produtos/{id}", response_model=Produto)
def obter_produto(id: int):
    df = carregar_dados()
    produto = df[df['id'] == id]

    if produto.empty:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto.iloc[0].to_dict()

@app.post("/produtos", response_model=Produto)
def criar_produto(produto: Produto):
    with data_lock:
        df = carregar_dados()

        if not df.empty and produto.id in df['id'].values:
            raise HTTPException(status_code=400, detail="ID já existe")
        if produto.id is None:
            novo_id = df['id'].max() + 1 if not df.empty else 1
            produto.id = novo_id
        
        novo_df = pd.DataFrame([produto.dict()])
        df = pd.concat([df, novo_df], ignore_index=True)
        salvar_dados(df)
    
    return produto

@app.put("/produtos/{id}", response_model=Produto)
def atualizar_produto(id: int, produto: Produto):
    with data_lock:
        df = carregar_dados()

        if id not in df['id'].values:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        produto.id = id
        df.loc[df['id'] == id, ['nome', 'categoria', 'preco']] = [produto.nome, produto.categoria, produto.preco]
        salvar_dados(df)
    
    return produto

@app.delete("/produtos/{id}")
def deletar_produto(id: int):
    with data_lock:
        df = carregar_dados()

        if id not in df['id'].values:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    df = df[df['id'] != id]
    salvar_dados(df)

    return {"message": "Produto deletado com sucesso"}

@app.get("/estatisticas", response_model=Estatisticas)
def obter_estatisticas():
    df = carregar_dados()

    produto_maior_preco = df.loc[df['preco'].idxmax()].to_dict()
    produto_menor_preco = df.loc[df['preco'].idxmin()].to_dict()
    media_precos = df['preco'].mean()

    produtos_acima_media = df[df['preco'] > media_precos].to_dict(orient='records')
    produtos_abaixo_media = df[df['preco'] < media_precos].to_dict(orient='records')

    return Estatisticas(
        produto_maior_preco=produto_maior_preco,
        produto_menor_preco=produto_menor_preco,
        media_precos=round(media_precos, 2),
        produtos_acima_media=produtos_acima_media,
        produtos_abaixo_media=produtos_abaixo_media

    )

@app.get("/produtos/maior_preco", response_model=Produto)
def obter_produto_maior_preco():
    df = carregar_dados()

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")
    
    return df.loc[df['preco'].idxmax()].to_dict()

@app.get("/produtos/menor_preco", response_model=Produto)
def obter_produto_menor_preco():
    df = carregar_dados()

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")
    
    return df.loc[df['preco'].idxmin()].to_dict()

@app.get("/produtos/media_precos", response_model=float)
def obter_media_precos():
    df = carregar_dados()

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")
    
    return round(df['preco'].mean(), 2)

@app.get("/produtos/acima_media", response_model=List[Produto])
def obter_produtos_acima_media():
    df = carregar_dados()

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")
    
    media_precos = df['preco'].mean()
    return df[df['preco'] > media_precos].to_dict(orient='records')

@app.get("/produtos/abaixo_media", response_model=List[Produto])
def obter_produtos_abaixo_media():
    df = carregar_dados()

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")
    
    media_precos = df['preco'].mean()
    return df[df['preco'] < media_precos].to_dict(orient='records')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
