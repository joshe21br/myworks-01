import psycopg2
from psycopg2 import sql
from base64 import b64encode
import bcrypt

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="nome do banco de dados",
        user="nome do usuario",
        password="senha do usuario"
    )

def create_table(conn):
    cursor = conn.cursor()
    create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table} (
        username VARCHAR(255) PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        url TEXT,
        obs VARCHAR(1000)
    );
    """).format(table=sql.Identifier('admins'))
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return b64encode(salt + hashed_password).decode('latin1')

def insert_admin(conn, username, email, password, url, obs):
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    insert_query = sql.SQL("""
    INSERT INTO {table} (username, email, password, url, obs) 
    VALUES (%s, %s, %s, %s, %s)
    """).format(table=sql.Identifier('admins'))
    cursor.execute(insert_query, (username, email, hashed_pw, url, obs))
    conn.commit()
    cursor.close()

def display_admins(conn):
    cursor = conn.cursor()
    select_query = sql.SQL("""
    SELECT username, email, obs FROM {table}
    """).format(table=sql.Identifier('admins'))
    cursor.execute(select_query)
    rows = cursor.fetchall()
    cursor.close()

    if rows:
        print("\nAdmins:")
        print(f"{'Username':<20} {'Email':<30} {'Observações'}")
        print("-" * 70)
        for row in rows:
            print(f"{row[0]:<20} {row[1]:<30} {row[2]}")
    else:
        print("\nNenhum dado encontrado.")

def menu():
    while True:
        print("\n" + "="*40)
        print(" Menu de Administração ".center(40, "="))
        print("="*40)
        print("1. Criar tabela")
        print("2. Inserir dados")
        print("3. Exibir dados")
        print("4. Sair")
        print("="*40)
        choice = input("Escolha uma opção: ")

        if choice == '1':
            conn = connect_db()
            create_table(conn)
            conn.close()
            print("\nTabela criada com sucesso!")
        elif choice == '2':
            conn = connect_db()
            while True:
                print("\nInserir novo admin:")
                username = input("Digite o username: ")
                email = input("Digite o email: ")
                password = input("Digite a senha: ")
                url = input("Digite a URL: ")
                obs = input("Digite observações: ")

                insert_admin(conn, username, email, password, url, obs)

                print("\nAdmin inserido com sucesso!")
                continuar = input("Deseja inserir outro admin? (s/n): ")
                if continuar.lower() != 's':
                    break
            conn.close()
        elif choice == '3':
            conn = connect_db()
            display_admins(conn)
            conn.close()
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()


