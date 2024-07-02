import time
import os
 
usuarios = []
produtos_disponiveis = [
    {"nome": "Camiseta", "preco": 29.99, "descricao": "Camiseta de algodão", "quantidade": 50},
    {"nome": "Calça Jeans", "preco": 79.90, "descricao": "Calça jeans masculina", "quantidade": 30},
    {"nome": "Tênis Esportivo", "preco": 149.99, "descricao": "Tênis para corrida", "quantidade": 20}
]
carrinho = []
historico_compras = []
 
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
    print("9. Administração de Estoque (somente para administradores)")
    print("0. Sair do Sistema")
 
def cadastrar_usuario():
    os.system('cls')
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    senha = input("Digite a senha do usuário: ")
    usuarios.append({"nome": nome, "email": email, "senha": senha})
    print(f'\nUsuário {nome} cadastrado com sucesso!')
    input("\nPressione Enter para voltar ao menu...")
 
def autenticar_usuario():
    os.system('cls')
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            print("\nAutenticado com sucesso!")
            time.sleep(2)
            return True
    print("Falha na autenticação.")
    time.sleep(2)
    return False
 
def exibir_catalogo(controle):
    os.system('cls')
    print('\nProdutos disponíveis:')
    for produto in produtos_disponiveis:
        print(f' - {produto["nome"]}: R${produto["preco"]} - {produto["descricao"]}')
       
    if controle:
        input("\nPressione Enter para voltar ao menu...")
 
def adicionar_produto_carrinho():
    os.system('cls')
    exibir_catalogo(False)
    nome_produto = input("\nDigite o nome do produto que deseja adicionar ao carrinho: ")
    for produto in produtos_disponiveis:
        if produto["nome"] == nome_produto:
            carrinho.append(produto.copy())
            print(f'\n{produto["nome"]} adicionado ao carrinho.')
            time.sleep(2)
            return
    print('Produto não encontrado no catálogo.')
    input("\nPressione Enter para voltar ao menu...")
 
def remover_produto_carrinho():
    os.system('cls')
    if not carrinho:
        print('Carrinho vazio.')
    else:
        print('\nProdutos no carrinho:')
        for produto in carrinho:
            print(f' - {produto["nome"]}: R${produto["preco"]}')
        nome_produto = input("\nDigite o nome do produto que deseja remover do carrinho: ")
        for produto in carrinho:
            if produto["nome"] == nome_produto:
                carrinho.remove(produto)
                print(f'\n{nome_produto} removido do carrinho.')
                time.sleep(2)
                return
        print('\nProduto não encontrado no carrinho.')
    input("\nPressione Enter para voltar ao menu...")
 
def mostrar_carrinho():
    os.system('cls')
    if not carrinho:
        print('Carrinho vazio.')
    else:
        print('\nProdutos no carrinho:')
        for produto in carrinho:
            print(f' - {produto["nome"]}: R${produto["preco"]}')
    input("\nPressione Enter para voltar ao menu...")
 
def calcular_total_carrinho():
    total = sum(produto["preco"] for produto in carrinho)
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
 
        if opcao_pagamento == '1':
            metodo_pagamento = "Cartão de Crédito"
        elif opcao_pagamento == '2':
            metodo_pagamento = "Boleto Bancário"
        else:
            print("Opção inválida de pagamento. Compra cancelada.")
            input("\nPressione Enter para voltar ao menu...")
            return
 
        confirmacao = input(f"Deseja realmente finalizar a compra com {metodo_pagamento}? (s/n): ")
        if confirmacao.lower() == 's':
            historico_compras.append({
                "produtos": carrinho.copy(),
                "total": total,
                "metodo_pagamento": metodo_pagamento
            })
            print('\nCompra finalizada com sucesso!')
            carrinho.clear()
        else:
            print('Compra cancelada.')
    input("\nPressione Enter para voltar ao menu...")
 
def mostrar_historico_compras():
    os.system('cls')
    titulo()
    if not historico_compras:
        print('\nHistórico de compras vazio.')
    else:
        print('\nHistórico de compras:')
        for idx, compra in enumerate(historico_compras, 1):
            print(f'Compra {idx}:')
            for produto in compra:
                print(f' - {produto["nome"]}: R${produto["preco"]}')
    input("\nPressione Enter para voltar ao menu...")
 
def administrar_estoque():
    os.system('cls')
    titulo()
    print("\nFunção de administração de estoque não implementada.")
    input("\nPressione Enter para voltar ao menu...")
 
def main():
    while True:
        mostrar_menu()
        opcao = input("\nDigite o número da opção desejada: ")
 
        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            autenticar_usuario()
        elif opcao == '3':
            exibir_catalogo()
        elif opcao == '4':
            adicionar_produto_carrinho()
        elif opcao == '5':
            remover_produto_carrinho()
        elif opcao == '6':
            mostrar_carrinho()
        elif opcao == '7':
            finalizar_compra()
        elif opcao == '8':
            mostrar_historico_compras()
        elif opcao == '9':
            administrar_estoque()
        elif opcao == '0':
            print('Saindo do sistema. Até mais!')
            break
        else:
            print('Opção inválida. Por favor, digite uma opção válida.')
 
if __name__ == "__main__":
    main()