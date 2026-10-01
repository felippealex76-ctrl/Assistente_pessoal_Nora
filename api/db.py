import pyodbc

CONEXAO = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=BURNHIGHIST\\SQLEXPRESS02;"
    "DATABASE=nora;"
    "Trusted_Connection=yes;"
)

def conectar():
    return pyodbc.connect(CONEXAO)