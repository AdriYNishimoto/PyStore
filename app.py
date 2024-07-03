import json
import time
import os

USUARIOS_JSON = 'usuarios.json'
PRODUTOS_JSON = 'produtos.json'
CARRINHO_JSON = 'carrinho.json'
HISTORICO_JSON = 'historico_compras.json'

# Funções para leitura e escrita em arquivos JSON
def ler_json(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escrever_json(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# Dados iniciais
usuarios_iniciais = [
    {"nome": "Adriano Nishimoto", "email": "admin@pystore.com", "senha": "admin123", "admin": True}
]

produtos_iniciais = [
    {"nome": "Camiseta", "preco": 29.99, "descricao": "Camiseta de algodão", "quantidade": 50},
    {"nome": "Calça Jeans", "preco": 79.90, "descricao": "Calça jeans masculina", "quantidade": 30},
    {"nome": "Tênis Esportivo", "preco": 149.99, "descricao": "Tênis para corrida", "quantidade": 20}
]

# Inicializa usuários e produtos se não existirem
if not os.path.exists(USUARIOS_JSON):
    escrever_json(USUARIOS_JSON, usuarios_iniciais)

if not os.path.exists(PRODUTOS_JSON):
    escrever_json(PRODUTOS_JSON, produtos_iniciais)

# Funções de Interface e Menu
def titulo():
    print("""\n
██████╗░██╗░░░██╗░██████╗████████╗░█████╗░██████╗░███████╗
██╔══██╗╚██╗░██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
██████╔╝░╚████╔╝░╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░
██╔═══╝░░░╚██╔╝░░░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░
██║░░░░░░░░██║░░░██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗
╚═╝░░░░░░░░╚═╝░░░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝""")
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
    print("\n1. Cadastro de Usuário")
    print("2. Login de Usuário")
    print("3. Catálogo de Produtos")
    print("4. Adicionar Produto ao Carrinho")
    print("5. Remover Produto do Carrinho")
    print("6. Visualizar Carrinho")
    print("7. Finalizar Compra")
    print("8. Histórico de Compras")
    print("9. Adicionar Produto ao Catálogo (Admin)")
    print("10. Remover Produto do Catálogo (Admin)")
    print("0. Sair do Sistema")

# Funções para manipulação de usuários
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

# Funções para manipulação de produtos e carrinho
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

def mostrar_carrinho():
    os.system('cls')
    carrinho = ler_json(CARRINHO_JSON)
    if not carrinho:
        print('Carrinho vazio.')
    else:
        print('\nProdutos no carrinho:')
        for item in carrinho:
            print(f' - {item["produto"]["nome"]}: {item["quantidade"]} unidades')
    input("\nPressione Enter para voltar ao menu...")

def calcular_total_carrinho():
    carrinho = ler_json(CARRINHO_JSON)
    total = sum(item["produto"]["preco"] * item["quantidade"] for item in carrinho)
    return total

def finalizar_compra():
    os.system('cls')
    mostrar_carrinho()
    total = calcular_total_carrinho()
    if total == 0:
        print('\nCarrinho vazio. Não é possível finalizar a compra.')
    else:
        print(f'\nTotal da compra: R${total:.2f}')
        print("\nSelecione o método de pagamento:")
        print("1. Cartão de Crédito")
        print("2. Boleto Bancário")
        opcao_pagamento = input("\nDigite o número do método de pagamento desejado: ")
        metodo_pagamento = "Cartão de Crédito" if opcao_pagamento == '1' else "Boleto Bancário"

        confirmacao = input(f"Deseja realmente finalizar a compra com {metodo_pagamento}? (s/n): ")
        if confirmacao.lower() == 's':
            historico_compras = ler_json(HISTORICO_JSON)
            carrinho = ler_json(CARRINHO_JSON)
            historico_compras.append({
                "produtos": carrinho,
                "total": total,
                "metodo_pagamento": metodo_pagamento
            })
            escrever_json(HISTORICO_JSON, historico_compras)
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

# Funções de manipulação de catálogo (admin)
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
    usuario_logado = None
    while True:
        mostrar_menu()
        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            usuario_logado = autenticar_usuario()
        elif opcao == '3':
            exibir_catalogo()
        elif opcao == '4':
            if usuario_logado:
                adicionar_produto_carrinho()
            else:
                print("Faça login primeiro.")
        elif opcao == '5':
            if usuario_logado:
                remover_produto_carrinho()
            else:
                print("Faça login primeiro.")
        elif opcao == '6':
            if usuario_logado:
                mostrar_carrinho()
            else:
                print("Faça login primeiro.")
        elif opcao == '7':
            if usuario_logado:
                finalizar_compra()
            else:
                print("Faça login primeiro.")
        elif opcao == '8':
            if usuario_logado:
                mostrar_historico_compras()
            else:
                print("Faça login primeiro.")
        elif opcao == '9':
            if usuario_logado:
                adicionar_produto_catalogo(usuario_logado)
            else:
                print("Faça login primeiro.")
        elif opcao == '10':
            if usuario_logado:
                remover_produto_catalogo(usuario_logado)
            else:
                print("Faça login primeiro.")
        elif opcao == '0':
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == '__main__':
    main()
