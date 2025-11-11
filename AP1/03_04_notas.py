import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

colunas = ["Nome", "Nota"]

alunos_df = pd.DataFrame(columns=colunas).set_index("Nome")

app = FastAPI (
    title="Sistema de Notas",
    description="API para registro e consulta de notas de alunos."
)

class Aluno(BaseModel):
    nome: str
    nota: float

    
@app.post("/alunos", status_code=201)
def adicionar_aluno(aluno: Aluno):

    Nome = Aluno.Nome
    Nota = Aluno.Nota

    alunos_df.loc[Nome, 'Nota'] = Nota

    return{"Aluno '{Nome}' registrado, nota atualizada com sucesso.", 
            "nota_atual", Nota}


@app.get("/alunos/{Nome}")
def obter_nota(Nome: str):
    if Nome in alunos_df.index:
        Nota = alunos_df.loc[Nome, 'Nota']
        return{"Nome": Nome, "Nota": Nota}
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Aluno '{Nome}' não registrado no sistema."
        )

@app.get("/alunos")
def listar():
    dicionario = alunos_df.to_dict(orient='index')
    lista_alunos = [{"Nome": Nome, "Nota": dados['Nota']} for Nome, dados in dicionario.items()]
    return lista_alunos