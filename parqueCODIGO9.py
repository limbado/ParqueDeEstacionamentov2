import mysql.connector
import tkinter as tk
from tkinter import messagebox

def ligar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="parque",
        password="parque123",
        database="parque_db"
    )

def criar_utilizador(nome, senha):
    ligacao = ligar_bd()
    cursor = ligacao.cursor()
    cursor.execute("SELECT * FROM utilizadores WHERE nome=%s", (nome,))
    if cursor.fetchone():
        messagebox.showinfo("Info", "Utilizador já existe!")
    else:
        cursor.execute("INSERT INTO utilizadores (nome, senha) VALUES (%s, %s)", (nome, senha))
        ligacao.commit()
        messagebox.showinfo("Info", "Utilizador criado com sucesso!")
    ligacao.close()

def validar_login(nome, senha):
    ligacao = ligar_bd()
    cursor = ligacao.cursor()
    cursor.execute("SELECT * FROM utilizadores WHERE nome=%s AND senha=%s", (nome, senha))
    if cursor.fetchone():
        messagebox.showinfo("Login", "Login efetuado com sucesso!")
    else:
        messagebox.showerror("Login", "Nome ou senha incorretos!")
    ligacao.close()

root = tk.Tk()
root.title("Login Parque DB")
root.geometry("300x200")

tk.Label(root, text="Nome").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Senha").pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

tk.Button(root, text="Login", command=lambda: validar_login(entry_nome.get(), entry_senha.get())).pack(pady=5)
tk.Button(root, text="Criar Conta", command=lambda: criar_utilizador(entry_nome.get(), entry_senha.get())).pack(pady=5)

root.mainloop()
