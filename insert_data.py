import psycopg2
from psycopg2 import sql
from base64 import b64encode
import bcrypt

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="works",
        user="bruna_kali",
        password="bruna@141521_"
    )

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

def main():
    conn = connect_db()

    while True:
        username = input("Digite o username: ")
        email = input("Digite o email: ")
        password = input("Digite a senha: ")
        url = input("Digite a URL: ")
        obs = input("Digite observações: ")

        insert_admin(conn, username, email, password, url, obs)

        continuar = input("Deseja inserir outro admin? (s/n): ")
        if continuar.lower() != 's':
            break

    conn.close()

if __name__ == "__main__":
    main()

