import json
import time
import os

USUARIOS_JSON = 'usuarios.json'
PRODUTOS_JSON = 'produtos.json'
CARRINHO_JSON = 'carrinho.json'
HISTORICO_JSON = 'historico_compras.json'

def ler_json(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escrever_json(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

usuarios_iniciais = [
    {"nome": "Adriano Nishimoto", "email": "admin@pystore.com", "senha": "admin123", "admin": True}
]

produtos_iniciais = [
    {"nome": "Camiseta", "preco": 29.99, "descricao": "Camiseta de algodão", "quantidade": 50},
    {"nome": "Calça Jeans", "preco": 79.90, "descricao": "Calça jeans masculina", "quantidade": 30},
    {"nome": "Tênis Esportivo", "preco": 149.99, "descricao": "Tênis para corrida", "quantidade": 20}
]

if not os.path.exists(USUARIOS_JSON):
    escrever_json(USUARIOS_JSON, usuarios_iniciais)

if not os.path.exists(PRODUTOS_JSON):
    escrever_json(PRODUTOS_JSON, produtos_iniciais)

def print_titulo():
    print("""\n
██████╗░██╗░░░██╗░██████╗████████╗░█████╗░██████╗░███████╗
██╔══██╗╚██╗░██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
██████╔╝░╚████╔╝░╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░
██╔═══╝░░░╚██╔╝░░░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░
██║░░░░░░░░██║░░░██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗
╚═╝░░░░░░░░╚═╝░░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝""")

def titulo():
    print_titulo()
    subtitulo()

def subtitulo():
    input("\nPressione Enter para continuar...")
    time.sleep(2)
    os.system('cls')

def mostrar_menu():
    os.system('cls')
    titulo()
    print("""
█▀▄▀█ █▀▀ █▄░█ █░█
█░▀░█ ██▄ █░▀█ █▄█""")
    print("\n1. Catálogo de Produtos")
    print("2. Adicionar Produto ao Carrinho")
    print("3. Remover Produto do Carrinho")
    print("4. Visualizar Carrinho")
    print("5. Finalizar Compra")
    print("6. Histórico de Compras")
    print("7. Adicionar Produto ao Catálogo (Admin)")
    print("8. Remover Produto do Catálogo (Admin)")
    print("0. Logout")

def cadastrar_usuario():
    os.system('cls')
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    senha = input("Digite a senha do usuário: ")
    usuarios = ler_json(USUARIOS_JSON)
    if any(usuario['email'] == email for usuario in usuarios):
        print('Erro: E-mail já cadastrado.')
    else:
        usuarios.append({"nome": nome, "email": email, "senha": senha, "admin": False})
        escrever_json(USUARIOS_JSON, usuarios)
        print(f'\nUsuário {nome} cadastrado com sucesso!')
    input("\nPressione Enter para voltar ao menu...")

def autenticar_usuario():
    os.system('cls')
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")
    usuarios = ler_json(USUARIOS_JSON)
    usuario = next((u for u in usuarios if u['email'] == email and u['senha'] == senha), None)
    if usuario:
        print("\nAutenticado com sucesso!")
        time.sleep(2)
        return usuario
    print("Falha na autenticação.")
    time.sleep(2)
    return None

def exibir_catalogo(controle=True):
    os.system('cls')
    produtos = ler_json(PRODUTOS_JSON)
    print('\nProdutos disponíveis:')
    for produto in produtos:
        print(f' - {produto["nome"]}: R${produto["preco"]:.2f} - {produto["descricao"]}')
    if controle:
        input("\nPressione Enter para voltar ao menu...")

def adicionar_produto_carrinho():
    os.system('cls')
    exibir_catalogo(False)
    nome_produto = input("\nDigite o nome do produto que deseja adicionar ao carrinho: ")
    produtos = ler_json(PRODUTOS_JSON)
    produto = next((p for p in produtos if p['nome'] == nome_produto), None)
    if produto:
        carrinho = ler_json(CARRINHO_JSON)
        quantidade = int(input("Digite a quantidade: "))
        if quantidade > produto['quantidade']:
            print(f'Erro: Quantidade solicitada ({quantidade}) é maior que o disponível em estoque ({produto["quantidade"]}).')
        else:
            carrinho.append({"produto": produto, "quantidade": quantidade})
            escrever_json(CARRINHO_JSON, carrinho)
            print(f'\n{nome_produto} adicionado ao carrinho.')
    else:
        print('Produto não encontrado no catálogo.')
    input("\nPressione Enter para voltar ao menu...")

def remover_produto_carrinho():
    os.system('cls')
    carrinho = ler_json(CARRINHO_JSON)
    if not carrinho:
        print('Carrinho vazio.')
    else:
        print('\nProdutos no carrinho:')
        for idx, item in enumerate(carrinho, 1):
            print(f'{idx}. {item["produto"]["nome"]}: {item["quantidade"]} unidades')
        idx_produto = int(input("\nDigite o número do produto que deseja remover do carrinho: "))
        if 0 < idx_produto <= len(carrinho):
            produto_removido = carrinho.pop(idx_produto - 1)
            escrever_json(CARRINHO_JSON, carrinho)
            print(f'{produto_removido["produto"]["nome"]} removido do carrinho.')
        else:
            print('Número inválido.')
    input("\nPressione Enter para voltar ao menu...")

def mostrar_carrinho(finalizando_compra=False):
    os.system('cls')
    carrinho = ler_json(CARRINHO_JSON)
    if not carrinho:
        print('Carrinho vazio.')
    else:
        print('\nProdutos no carrinho:')
        for item in carrinho:
            print(f' - {item["produto"]["nome"]}: {item["quantidade"]} unidades')

    if finalizando_compra:
        input("\nPressione Enter para prosseguir na finalização da compra...")
    else:
        input("\nPressione Enter para voltar ao menu...")

def calcular_total_carrinho():
    carrinho = ler_json(CARRINHO_JSON)
    total = sum(item["produto"]["preco"] * item["quantidade"] for item in carrinho)
    return total

def atualizar_estoque():
    produtos = ler_json(PRODUTOS_JSON)
    carrinho = ler_json(CARRINHO_JSON)
    for item_carrinho in carrinho:
        for produto in produtos:
            if produto['nome'] == item_carrinho['produto']['nome']:
                produto['quantidade'] -= item_carrinho['quantidade']
    escrever_json(PRODUTOS_JSON, produtos)

def finalizar_compra():
    os.system('cls')
    mostrar_carrinho(finalizando_compra=True)
    total = calcular_total_carrinho()
    if total == 0:
        print('\nCarrinho vazio. Não é possível finalizar a compra.')
    else:
        print(f'\nTotal da compra: R${total:.2f}')
        print("\nSelecione o método de pagamento:")
        print("1. Cartão de Crédito")
        print("2. Boleto Bancário")
        opcao_pagamento = input("\nDigite o número do método de pagamento desejado: ")
        metodo_pagamento = "Cartão de Crédito" if opcao_pagamento == '1' else "Boleto Bancário" if opcao_pagamento == '2' else None

        if metodo_pagamento:
            carrinho = ler_json(CARRINHO_JSON)
            historico_compras = ler_json(HISTORICO_JSON)
            historico_compras.append({"produtos": carrinho, "total": total, "metodo_pagamento": metodo_pagamento})
            escrever_json(HISTORICO_JSON, historico_compras)
            atualizar_estoque()
            escrever_json(CARRINHO_JSON, [])
            print('\nCompra finalizada com sucesso!')
        else:
            print('Compra cancelada.')
    input("\nPressione Enter para voltar ao menu...")

def mostrar_historico_compras():
    os.system('cls')
    titulo()
    historico_compras = ler_json(HISTORICO_JSON)
    if not historico_compras:
        print('Histórico de compras vazio.')
    else:
        print('\nHistórico de Compras:')
        for idx, compra in enumerate(historico_compras, 1):
            print(f'\nCompra {idx}:')
            for item in compra["produtos"]:
                print(f' - {item["produto"]["nome"]}: {item["quantidade"]} unidades')
            print(f'Total: R${compra["total"]:.2f}')
            print(f'Método de Pagamento: {compra["metodo_pagamento"]}')
    input("\nPressione Enter para voltar ao menu...")

def adicionar_produto_catalogo(usuario):
    if not usuario['admin']:
        print('Acesso negado: Apenas administradores podem adicionar produtos ao catálogo.')
        time.sleep(2)
        return
    os.system('cls')
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    descricao = input("Digite a descrição do produto: ")
    quantidade = int(input("Digite a quantidade em estoque: "))
    produtos = ler_json(PRODUTOS_JSON)
    produtos.append({"nome": nome, "preco": preco, "descricao": descricao, "quantidade": quantidade})
    escrever_json(PRODUTOS_JSON, produtos)
    print(f'\nProduto {nome} adicionado ao catálogo com sucesso!')
    input("\nPressione Enter para voltar ao menu...")

def remover_produto_catalogo(usuario):
    if not usuario['admin']:
        print('Acesso negado: Apenas administradores podem remover produtos do catálogo.')
        time.sleep(2)
        return
    os.system('cls')
    exibir_catalogo(False)
    nome_produto = input("\nDigite o nome do produto que deseja remover do catálogo: ")
    produtos = ler_json(PRODUTOS_JSON)
    produto = next((p for p in produtos if p['nome'] == nome_produto), None)
    if produto:
        produtos.remove(produto)
        escrever_json(PRODUTOS_JSON, produtos)
        print(f'\nProduto {nome_produto} removido do catálogo.')
    else:
        print('Produto não encontrado no catálogo.')
    input("\nPressione Enter para voltar ao menu...")

def main():
    while True:
        usuario_logado = None
        while usuario_logado is None:
            os.system('cls')
            print_titulo()
            print("1. Cadastro de Usuário")
            print("2. Login de Usuário")
            opcao = input("\nDigite o número da opção desejada: ")

            if opcao == '1':
                cadastrar_usuario()
            elif opcao == '2':
                usuario_logado = autenticar_usuario()
            else:
                print('Opção inválida. Tente novamente.')

        while usuario_logado:
            mostrar_menu()
            opcao = input("\nDigite o número da opção desejada: ")

            if opcao == '1':
                exibir_catalogo()
            elif opcao == '2':
                adicionar_produto_carrinho()
            elif opcao == '3':
                remover_produto_carrinho()
            elif opcao == '4':
                mostrar_carrinho()
            elif opcao == '5':
                finalizar_compra()
            elif opcao == '6':
                mostrar_historico_compras()
            elif opcao == '7':
                adicionar_produto_catalogo(usuario_logado)
            elif opcao == '8':
                remover_produto_catalogo(usuario_logado)
            elif opcao == '0':
                usuario_logado = None
                break
            else:
                print('Opção inválida. Tente novamente.')

if __name__ == '__main__':
    main()
