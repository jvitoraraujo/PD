import pandas as pd

dados = {
    "Sonny Corleone": 15000.50,
    "Fredo Corleone": 7500.25,
    "Tom Hagen": 5000.00,
    "Peter Clemenza": 22000.75,
    "Sal Tessio": 18000.00,
    "Rocco Lampone": 11000.50
}

receita_semanal = pd.Series(dados)

print("Receita semanal:  ", receita_semanal.to_string())

total = receita_semanal.sum()

media = receita_semanal.mean()

maior_receita = receita_semanal.idxmax()

print("Maior receita: ", maior_receita)

acima_media = receita_semanal > media

associados_acima_media = receita_semanal[acima_media]

print("Associados acima da média: ", associados_acima_media)