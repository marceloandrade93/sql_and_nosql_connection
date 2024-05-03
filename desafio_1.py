"""Definir esquema do database, inserir dados e recuperar valores.

origem: Código para o desafio de código da Formação Python Developer.
data: 23/04/2024
autor: Marcelo Andrade
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float


Base = declarative_base()
engine = create_engine("sqlite:///Desafio de Código/database.db")


class Cliente(Base):
    __tablename__ = "client_account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    cpf = Column(String(9))
    address = Column(String(50))

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
        )

    def __repr__(self):
        return f"""Client(id={self.id},
        name={self.name},
        cpf={self.cpf},
        address={self.address})"""

    @property
    def new_client():
        pass

    def delete_table_main(self):
        name = self.__tablename__
        print(name)
        return f"Table {name} deleted!"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_type = Column(String(20))
    agency = Column(String(4))
    digit = Column(Integer)
    balance = Column(Float(20))
    id_client = Column(Integer,
                       ForeignKey("client_account.id"),
                       nullable=False)

    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return f"""Conta(id={self.id},
        account_type={self.account_type},
        agency={self.agency},
        digit={self.digit},
        balance={self.balance})"""


Base.metadata.create_all(engine)


def menu():
    printed_text = ("\n***************** MENU *****************"
                    "\n[1]\tNew Client"
                    "\n[2]\tNew Account"
                    "\n[3]\tList Clients"
                    "\n[4]\tList Accounts"
                    "\n[5]\tDelete Table"
                    "\n[6]\tExit"
                    "\n=> "
                    )
    return input(printed_text)


def new_account():
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

        set_id_client = filter_client(cpf)[0]
        set_agencia = input("Enter the agency number: \n=> ")
        set_num = input("Enter the digit account: \n=> ")

        # Inserting new Account with Session
        with Session(engine) as session:
            var_new_account = Conta(
                account_type=set_tipo,
                agency=set_agencia,
                digit=set_num,
                balance=0,
                id_client=set_id_client
            )

            # Sending to DB (data persistence)
            session.add_all([var_new_account])
            session.commit()

        print("\n---------------- RETURN ----------------",
              "\n| Account registered                   |",
              "\n----------------------------------------")


def list_account():
    # Retriving client by exactly name variable
    print("\n---------------- RETURN ----------------")
    sql_select = text("SELECT * FROM conta")
    connection = engine.connect()
    result = connection.execute(sql_select)
    verify_row = [row for row in result if Cliente.id != 0]
    connection.close()

    if verify_row != []:
        connection = engine.connect()
        result = connection.execute(sql_select)

        for row in result:
            print(f"| ID: {row[0]}",
                  f"\n| Account type: {row[1]}",
                  f"\n| Agency: {row[2]}",
                  f"\n| Digit: {row[3]}",
                  f"\n| Balance: {row[4]}",
                  f"\n| ID_REF: {row[5]}",
                  "\n----------------------------------------")

    else:
        print("| Empty table.                         |"
              "\n----------------------------------------")

    connection.close()


def new_client():
    cpf = input("Informe o CPF (somente número): ")

    if filter_client(cpf):
        print("\n---------------- RETURN ----------------",
              f"\n| O CPF {cpf} já existe.         |",
              "\n----------------------------------------")
        return

    else:
        # Get variables
        new_name = input("Informe o nome: ")
        new_cpf = cpf
        new_address = input("Informe o endereço: ")

        # Inserting new Cliente with Session
        with Session(engine) as session:
            var_client_name = Cliente(
                name=new_name,
                cpf=new_cpf,
                address=new_address
            )

            # Sending to DB (data persistence)
            session.add_all([var_client_name])
            session.commit()

        print("\n---------------- RETURN ----------------",
              f"\n| CPF {cpf} registered           |",
              "\n----------------------------------------")


def filter_client(cpf):
    # Listing all clients
    sql = text("SELECT * FROM client_account")
    connection = engine.connect()
    clients = connection.execute(sql)

    # Check is there is cpf
    clients_filtered = [client for client in clients
                        if client.cpf == cpf]

    connection.close()

    return clients_filtered[0] if clients_filtered else None


def list_clients():
    # Retriving client by exactly name variable
    print("\n---------------- RETURN ----------------")
    sql_select = text("SELECT * FROM client_account")
    connection = engine.connect()
    result = connection.execute(sql_select)
    verify_row = [row for row in result if Cliente.id != 0]
    connection.close()

    if verify_row != []:
        connection = engine.connect()
        result = connection.execute(sql_select)

        for row in result:
            print(f"| ID: {row[0]}",
                  f"\n| Nome: {row[1]}",
                  f"\n| CPF: {row[2]}",
                  f"\n| Endereço: {row[3]}",
                  "\n----------------------------------------")

    else:
        print("| Empty table.                         |"
              "\n----------------------------------------")

    connection.close()


def delete_table():
    # Get the table name to delete
    print("\nWhich table do yo want to delete?"
          "\n[1] Cliente"
          "\n[2] Conta")

    table_to_delete = input("=> ")

    # Deleteing the table defined
    connection = engine.connect()

    if table_to_delete == "1":
        Cliente.__table__.drop(connection)
        Base.metadata.create_all(engine)
        connection.close()
        print("\n---------------- RETURN ----------------")
        print("| Deleted records from Cliente table   |")
        print("----------------------------------------")

    elif table_to_delete == "2":
        Conta.__table__.drop(connection)
        Base.metadata.create_all(engine)
        connection.close()
        print("\n---------------- RETURN ----------------")
        print("| Deleted records from Conta table     |")
        print("----------------------------------------")

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
            # Delete Table
            delete_table()

        elif opcao == "6":
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
