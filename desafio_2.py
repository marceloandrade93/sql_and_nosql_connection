"""Connect with MongoDB, create collections and documents.

origin: Code for the Python Developer Training code challenge.
date: 03/05/2024
author: Marcelo Andrade
"""

import pymongo as pyM

# Creating MongoDB connection
"""replace the value of url_mongo with your connection."""
url_mongo = ("mongodb+srv://adm:modeANI35!@pymongo.u5uw9ub.mongodb.net/",
             "?retryWrites=true&w=majority&appName=pymongo")
client = pyM.MongoClient(url_mongo)

# Creating/Connecting with Database and Collection
db = client.test


class Cliente:
    posts_profile_user = db.profile_user


class Conta:
    posts_account_user = db.client_account


def menu():
    printed_text = ("\n***************** MENU *****************"
                    "\n[1]\tNew Client"
                    "\n[2]\tNew Account"
                    "\n[3]\tList Clients"
                    "\n[4]\tList Accounts"
                    "\n[5]\tSearch Client"
                    "\n[6]\tDelete Table"
                    "\n[7]\tExit"
                    "\n=> "
                    )
    return input(printed_text)


def new_account():  # OK
    cpf = input("Informe o CPF (somente número): ")

    if filter_client(cpf) is None:
        print("\n---------------- RETURN ----------------",
              f"\n| CPF {cpf} not found.           |",
              "\n----------------------------------------")
        return

    else:
        # Get variables
        # 1 = Conta Corrente; 2 = Conta Poupança
        existents_accounts = [1, 2]
        set_tipo = 0

        while set_tipo not in existents_accounts:
            print("\nWhich type account?"
                  "\n[1] Conta Corrente"
                  "\n[2] Conta Poupança")
            set_tipo = int(input("=> "))

        if set_tipo == 1:
            set_tipo = "Conta Corrente"
        elif set_tipo == 2:
            set_tipo = "Conta Poupança"

        # Set variables with account values
        set_id_client = ""

        if filter_client(cpf):
            for post in Cliente().posts_profile_user.find({'cpf': cpf}):
                if post['_id']:
                    set_id_client = post['_id']
                else:
                    pass

        set_agencia = input("Enter the agency number: \n=> ")
        set_num = input("Enter the digit account: \n=> ")

        account_client = [
            {'account_type': set_tipo, 'agency': set_agencia,
             'digit': set_num, 'balance': 0,
             'id_client': set_id_client},
            ]

        # Creating data profiles or insert in mongodb with above list
        db.client_account.insert_many(account_client)

        print("\n---------------- RETURN ----------------",
              "\n| Account registered                   |",
              "\n----------------------------------------")


def new_client():  # OK
    cpf = input("Informe o CPF (somente número): ")

    if filter_client(cpf):
        print("\n---------------- RETURN ----------------",
              f"\n| CPF {cpf} already exists.      |",
              "\n----------------------------------------")
        return

    else:
        new_name = input("Informe o nome: ")
        new_cpf = cpf
        new_address = input("Informe o endereço: ")

        user_profile = [
            {'cpf': new_cpf, 'name': new_name, 'endereco': new_address},
            ]

        # 2º creating data profiles or insert in mongodb with above list
        db.profile_user.insert_many(user_profile)

        print("\n---------------- RETURN ----------------",
              f"\n| CPF {cpf} registered           |",
              "\n----------------------------------------")


def list_account():  # OK
    # for post in Cliente().posts_profile_user.find({'name': 'Lyza'}):
    #     pprint.pprint(post)
    #     print('------------------------------------')

    cpf = input("Informe o CPF (somente número): ")
    print("\n---------------- RETURN ----------------")

    if filter_client(cpf):
        id_client = ""

        # Get id_client from Cliente
        for post in Cliente().posts_profile_user.find({'cpf': cpf}):
            if post['_id']:
                id_client = post['_id']
            else:
                pass

        # Get details account by id_client
        ver_id_in_conta = Conta().posts_account_user.find(
            {'id_client': id_client})
        ver_if_empty = str(Conta.posts_account_user.count_documents(
            {'id_client': id_client}))

        if ver_if_empty == '0':
            print("| This client haven't account.         |",
                  "\n----------------------------------------")

        else:
            for post in ver_id_in_conta:
                print(f"| ID: {post['_id']}",
                      f"\n| Account Type: {post['account_type']}",
                      f"\n| Agency: {post['agency']}",
                      f"\n| Digit: {post['digit']}",
                      f"\n| Balance: {post['balance']}",
                      f"\n| ID Client: {post['id_client']}",
                      "\n----------------------------------------")

    else:
        print(f"| CPF {cpf} not found.           |"
              "\n----------------------------------------")


def search_client():  # OK
    cpf = input("Informe o CPF (somente número): ")
    print("\n---------------- RETURN ----------------")

    if filter_client(cpf):
        for post in Cliente().posts_profile_user.find({'cpf': cpf}):
            print(f"| ID: {post['_id']}",
                  f"\n| Nome: {post['name']}",
                  f"\n| CPF: {post['cpf']}",
                  f"\n| Endereço: {post['endereco']}",
                  "\n----------------------------------------")

    else:
        print(f"| CPF {cpf} not found.           |"
              "\n----------------------------------------")


def filter_client(cpf):  # OK
    # Check is there is cpf
    clients = Cliente().posts_profile_user.find({'cpf': cpf})

    clients_filtered = [client for client in clients
                        if client is not None]

    return 'cadastrado' if clients_filtered else None


def list_clients():  # OK
    # Retrieving documents from collection
    print("\n---------------- RETURN ----------------")
    clients = Cliente().posts_profile_user.find()
    clients_checked = [client for client in clients
                       if client is not None]

    if clients_checked != []:
        for post in Cliente().posts_profile_user.find({}):
            print(f"| ID: {post['_id']}",
                  f"\n| Nome: {post['name']}",
                  f"\n| CPF: {post['cpf']}",
                  f"\n| Endereço: {post['endereco']}",
                  "\n----------------------------------------")

    else:
        print("| Empty table.                         |"
              "\n----------------------------------------")


def delete_table():  # OK
    # Get the table name to delete
    print("\nWhich table do yo want to delete?"
          "\n[1] Cliente"
          "\n[2] Conta")

    table_to_delete = input("=> ")

    if table_to_delete == "1":
        db['profile_user'].drop()
        print("\n---------------- RETURN ----------------")
        print("| Deleted records from Cliente table   |")
        print("----------------------------------------")
        db.create_collection("profile_user")

    elif table_to_delete == "2":
        db['client_account'].drop()
        print("\n---------------- RETURN ----------------")
        print("| Deleted records from Conta table     |")
        print("----------------------------------------")
        db.create_collection("client_account")

    else:
        print("\n---------------- RETURN ----------------")
        print("| There aren't this table.             |")
        print("----------------------------------------")


def main():
    # clientes = []
    # contas = []
    while True:
        opcao = menu()

        if opcao == "1":
            # New Client
            new_client()

        elif opcao == "2":
            # New Account
            new_account()

        elif opcao == "3":
            # List Clients
            list_clients()

        elif opcao == "4":
            # List Accounts
            list_account()

        elif opcao == "5":
            # Search Client
            search_client()

        elif opcao == "6":
            # Delete Table
            delete_table()

        elif opcao == "7":
            # Exit
            print("\n---------------- RETURN ----------------",
                  "\n| Closing the application.             |",
                  "\n----------------------------------------")
            break

        else:
            # Invalid Input
            print("\n---------------- RETURN ----------------",
                  "\n| Invalid input! Please select again a |",
                  "\n| valid option.                        |",
                  "\n----------------------------------------")


main()
