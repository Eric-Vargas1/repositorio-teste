import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_NEWS")
LIMIT_MAX = 10

def buscar_noticias(tema, quantidade):
    """
    Busca notícias de um tema específico usando a API da NewsAPI.

    Parâmetros:
    tema (str): O tema ou palavra-chave para buscar notícias.
    quantidade (int): O número de notícias a serem retornadas (máximo definido por LIMIT_MAX).

    Retorna:
    list of tuple: Lista de tuplas contendo título, fonte e autor de cada notícia.
    """
    url = f"https://newsapi.org/v2/everything?q={tema}&pageSize={quantidade}&sortBy=publishedAt&language=pt&apiKey={API_KEY}"
    resposta = requests.get(url)
    dados = resposta.json()
    print(dados)

    noticias = dados.get("articles", [])
    resultado = []

    for noticia in noticias:
        titulo = noticia.get("title", "Sem título")
        fonte = noticia.get("source", {}).get("name", "Fonte desconhecida")
        autor = noticia.get("author", "Autor desconhecido")
        resultado.append((titulo, fonte, autor))

    return resultado

def menu():
    """
    Exibe o menu principal do programa, permitindo ao usuário buscar notícias ou sair.

    Armazena um histórico das buscas feitas durante a execução
    e exibe o total de notícias buscadas ao final.
    """
    historico = []
    total_noticias = 0

    while True:
        print("\n=== MENU DE NOTÍCIAS ===")
        print("1. Buscar notícias")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            tema = input("Digite o tema da notícia: ").strip()
            try:
                quantidade = int(input(f"Quantas notícias deseja buscar? (1 a {LIMIT_MAX}): "))
                if quantidade < 1 or quantidade > LIMIT_MAX:
                    print(f"Por favor, digite um número entre 1 e {LIMIT_MAX}.")
                    continue
            except ValueError:
                print("Entrada inválida. Digite um número.")
                continue

            noticias = buscar_noticias(tema, quantidade)

            print(f"\n--- {len(noticias)} Notícias sobre '{tema}' ---")
            for idx, (titulo, fonte, autor) in enumerate(noticias, start=1):
                print(f"{idx}. {titulo}\n   Fonte: {fonte} | Autor: {autor}\n")

            historico.append((tema, quantidade))
            total_noticias += quantidade

        elif opcao == '2':
            print("\n=== HISTÓRICO DE BUSCAS ===")
            for idx, (tema, qtd) in enumerate(historico, start=1):
                print(f"{idx}. Tema: {tema} | Notícias buscadas: {qtd}")
            print(f"\nTotal de notícias buscadas: {total_noticias}")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()