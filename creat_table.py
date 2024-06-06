import psycopg2
from psycopg2 import sql

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="works",
        user="nome do ususario",
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

def main():
    conn = connect_db()
    create_table(conn)
    conn.close()

if __name__ == "__main__":
    main()

