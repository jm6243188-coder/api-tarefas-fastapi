import sqlite3

def conectar_banco():
    return sqlite3.connect("BancoTarefas.db")

def criar_tabela_tarefas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    concluido INTEGER
    )
    """)

    conexao.commit()
    conexao.close()


criar_tabela_tarefas()