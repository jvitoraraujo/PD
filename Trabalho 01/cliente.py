import httpx
import asyncio
import time

BASE_URL = "http://localhost:8000"

class Cliente_Produtos:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def close(self):
        await self.client.aclose()

    async def testar_crud(self):
        
        print("=== Testando CRUD de Produtos ===\n")

        print("1. Listando todos os produtos: ")
        response = await self.client.get(f"{BASE_URL}/produtos")
        print(f"Status: {response.status_code}")
        produtos = response.json()
        print(f"Total de produtos: {len(produtos)}")

        print("\n2. Obtendo um produto específico pelo ID: ")
        produto_id = 1
        response = await self.client.get(f"{BASE_URL}/produtos/{produto_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            produto = response.json()
            print(f"Produto: {produto['nome']} - R$ {produto['preco']}")

        print("\n3. Criando um novo produto: ")
        novo_produto = {
            "nome": "Produto Teste",
            "categoria": "Categoria Teste",
            "preco": 19.99
        }
        response = await self.client.post(f"{BASE_URL}/produtos", json=novo_produto)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            produto_teste = response.json()
            print(f"Produto criado: {produto_teste['nome']} (ID: {produto_teste['id']})")
            novo_id = produto_teste['id']
        else:
            print("Erro ao criar produto")
            return
        
        print("\n4. Atualizando um produto existente: ")
        produto_atualizado = {
            "nome": "Produto Atualizado",
            "categoria": "Categoria Atualizada",
            "preco": 29.99
        }
        response = await self.client.put(f"{BASE_URL}/produtos/{novo_id}", json=produto_atualizado)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            produto_atualizado = response.json()
            print(f"Produto atualizado com sucesso")

        print("\n5. Deletando um produto: ")
        response = await self.client.delete(f"{BASE_URL}/produtos/{novo_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Produto deletado com sucesso")

    async def testar_estatisticas(self):

        print("\n=== Testando Estatísticas ===\n")

        response = await self.client.get(f"{BASE_URL}/estatisticas")
        if response.status_code == 200:
            stats = response.json()

            print("1. Produto com maior preço: ")
            print(f"Nome: {stats['produto_maior_preco']['nome']}")
            print(f"Preço: R$ {stats['produto_maior_preco']['preco']:.2f}")
            print(f"Categoria: {stats['produto_maior_preco']['categoria']}")

            print("\n2. Produto com menor preço: ")
            print(f"Nome: {stats['produto_menor_preco']['nome']}")
            print(f"Preço: R$ {stats['produto_menor_preco']['preco']:.2f}")
            print(f"Categoria: {stats['produto_menor_preco']['categoria']}")

            print("\n3. Média de preços dos produtos: ")
            print(f"R$ {stats['media_precos']:.2f}")

            print("\n4. Produtos com preço acima da média: ")
            for produto in stats['produtos_acima_media']:
                print(f"Nome: {produto['nome']}")
                print(f"Preço: R$ {produto['preco']:.2f}")
                print(f"Categoria: {produto['categoria']}")

            print("\n5. Produtos com preço abaixo da média: ")
            for produto in stats['produtos_abaixo_media']:
                print(f"Nome: {produto['nome']}")
                print(f"Preço: R$ {produto['preco']:.2f}")
                print(f"Categoria: {produto['categoria']}")
        else:
            print(f"Erro ao obter estatísticas: Status {response.status_code}")

    async def testar_estatisticas_individuais(self):

        print("\n=== Testando Estatísticas Individuais ===\n")

        print("1. Produto com maior preço: ")
        response = await self.client.get(f"{BASE_URL}/produtos/maior_preco")
        if response.status_code == 200:
            produto = response.json()
            print(f"Nome: {produto['nome']}")
            print(f"Preço: R$ {produto['preco']:.2f}")
            print(f"Categoria: {produto['categoria']}")
        else:
            print("Erro ao obter produto com maior preço")

        print("\n2. Produto com menor preço: ")
        response = await self.client.get(f"{BASE_URL}/produtos/menor_preco")
        if response.status_code == 200:
            produto = response.json()
            print(f"Nome: {produto['nome']}")
            print(f"Preço: R$ {produto['preco']:.2f}")
            print(f"Categoria: {produto['categoria']}")
        else:
            print("Erro ao obter produto com menor preço")
        
        print("\n3. Média de preços dos produtos: ")
        response = await self.client.get(f"{BASE_URL}/produtos/media_precos")
        if response.status_code == 200:
            media_precos = response.json()
            print(f"R$ {media_precos:.2f}")
        else:
            print("Erro ao obter média de preços")

        print("\n4. Produtos com preço acima da média: ")
        response = await self.client.get(f"{BASE_URL}/produtos/acima_media")
        if response.status_code == 200:
            produtos = response.json()
            for produto in produtos:
                print(f"Nome: {produto['nome']}")
                print(f"Preço: R$ {produto['preco']:.2f}")
                print(f"Categoria: {produto['categoria']}")
        else:
            print("Erro ao obter produtos com preço acima da média")

        print("\n5. Produtos com preço abaixo da média: ")
        response = await self.client.get(f"{BASE_URL}/produtos/abaixo_media")
        if response.status_code == 200:
            produtos = response.json()
            for produto in produtos:
                print(f"Nome: {produto['nome']}")
                print(f"Preço: R$ {produto['preco']:.2f}")
                print(f"Categoria: {produto['categoria']}")
        else:
            print("Erro ao obter produtos com preço abaixo da média")

async def testar_desempenho(client: httpx.AsyncClient):
    
    print("\n=== Testando Desempenho ===\n")

    endpoints = [
        "/produtos",
        "/estatisticas",
        "/produtos/maior_preco",
        "/produtos/menor_preco",
        "/produtos/media_precos",
    ]

    for endpoint in endpoints:
        start_time = time.time()
        response = await client.get(f"{BASE_URL}{endpoint}")
        end_time = time.time()

        if response.status_code == 200:
            tempo_resposta = (end_time - start_time) * 1000
            print(f"Endpoint: {endpoint}")
            print(f"Tempo de resposta: {tempo_resposta:.2f} ms")
        else:
            print(f"Erro ao acessar endpoint: {endpoint}")

async def main():
    cliente = Cliente_Produtos()

    try:
        
        await cliente.testar_crud()

        await cliente.testar_estatisticas()

        await cliente.testar_estatisticas_individuais()
        
        await testar_desempenho(cliente.client)

        print("\n" + "="*50)
        print("Testes concluídos com sucesso")
        print("\n" + "="*50)

    except Exception as e:
        print(f"Erro durante os testes: {e}")
        
    finally:
        await cliente.close()

if __name__ == "__main__":
    asyncio.run(main())
