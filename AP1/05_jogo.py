from bs4 import BeautifulSoup
import os

def vitoria(jogada1, jogada2):
    if jogada1 == jogada2:
        return 0
    elif (jogada1 == 'pedra' and jogada2 == 'tesoura') or \
         (jogada1 == 'tesoura' and jogada2 == 'papel') or \
         (jogada1 == 'papel' and jogada2 == 'pedra'):
        return 1
    else:
        return -1

vitorias_jogador_1 = 0
nome_arquivo = "jogadas.html"

try:
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        conteudo_html = f.read()
except FileNotFoundError:
    print("O arquivo '{nome_arquivo}' não foi encontrado.")
    exit()

soup = BeautifulSoup(conteudo_html, 'lxml')

tabela_linhas = soup.find('tbody').find_all('tr')

for linha in tabela_linhas:
    jogadas = linha.find_all('td')
    
    jogada_p1 = jogadas[0].text.strip().lower()
    jogada_p2 = jogadas[1].text.strip().lower()
    
    resultado = verifica_vitoria(jogada_p1, jogada_p2)
    
    if resultado == 1:
        vitorias_jogador_1 += 1

print("Vitórias do Jogador 1: ", {vitorias_jogador_1})