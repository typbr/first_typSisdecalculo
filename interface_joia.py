from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from customtkinter import *
from requests_html import HTMLSession
import lxml
from bs4 import BeautifulSoup
import sqlite3

class signupwindow:

    def entry_userpas(self):
        self.user = self.user_entry.get()
        self.password = self.password_entry.get()

        self.cursor.execute("""
            INSERT INTO users (username,password)
            VALUES (?,?)
            """, (self.user, self.password))
        self.conn.commit()
        self.conn.close()
        

    def __init__(self):

        self.signup_window = Tk()
        self.signup_window.title("Cadastrar")
        self.signup_window.resizable(False,False)
        self.signup_window.iconbitmap("teste\\login.ico")

        self.conn = sqlite3.connect('teste\\banco_de_dados_teste.db')
        self.cursor = self.conn.cursor()

        self.user_name = Label(self.signup_window, text="Login:", font="20")
        self.user_name.grid(column=0,row=0, padx=20)
        self.user_entry = Entry(self.signup_window)
        self.user_entry.grid(column=1, row=0, padx=20)

        self.user_password = Label(self.signup_window, text="Senha:", font="20")
        self.user_password.grid(column=0,row=1, padx=20)
        self.password_entry = Entry(self.signup_window, show="*")
        self.password_entry.grid(column=1, row=1, padx=20)



        self.button_show = Button(self.signup_window,text="Cadastrar", command=self.entry_userpas)
        self.button_show.grid(column=2, row=1, padx=20)

        self.signup_window.mainloop()

        

class workwindow:

    def destroy_grama(self):
        self.label.destroy()
        self.label_dois.destroy()
        self.label_tres.destroy()


    def calculo_grama(self):
        self.grama = self.calculo.get()
        self.valor = float(self.grama)
        self.calculo_um = (self.final * 1.55) * self.valor # Cálculo Sem Taxa do seu fornecedor
        self.calculo_dois = ((self.final * 1.55) * self.valor) * 1.20 # Cálculo com Taxa do seu Fornecedor
        self.calculo_tres = (((self.final * 1.55) * self.valor) * 1.20) * 1.26 # Cáculo de acordo com a taxa da máquininha
        self.calculo_final_um = self.calculo_um
        self.calculo_final_dois = self.calculo_dois
        self.calculo_final_tres = self.calculo_tres



        self.label = Label(self.work_window, text=f"Valor SEM Taxa: R${self.calculo_final_um:.2f}", font="Arial,20")
        self.label.grid(column=0,row=5)
        self.label_dois = Label(self.work_window, text=f"Valor COM Taxa: R${self.calculo_final_dois:.2f}", font="Arial,20")
        self.label_dois.grid(column=0,row=6)
        self.label_tres = Label(self.work_window, text=f"Valor em 10X SEM JUROS: R${self.calculo_final_tres:.2f}", font="Arial,20")
        self.label_tres.grid(column=0,row=7)

        self.destroy_button = Button(self.work_window, text="Limpar", command=self.destroy_grama)
        self.destroy_button.grid(column=0,row=9, padx=9, pady=9)
        



    def __init__(self):
        self.work_window = Tk()
        self.work_window.title("Loja")
        self.work_window.resizable(False,False)
        self.work_window.iconbitmap("teste\\login.ico")

        self.acesso = HTMLSession()
        self.link = self.acesso.get("https://goldrate.com/pt-br/grama-do-ouro-preco-cotacao-valor/")
        self.html = BeautifulSoup(self.link.text, 'lxml')
        self.valor = self.html.find('em', class_="price-value")
        self.valor_exato = float(self.valor.text)
        self.final = self.valor_exato

        Label(self.work_window, text=f"Olá Faça seu Calculo:").grid(column=0,row=0,columnspan=1,sticky=W+E)

        self.calculo_label = Label(self.work_window, text="Grama:", foreground="black")
        self.calculo_label.grid(column=0, row=2)
        self.calculo = Entry(self.work_window)
        self.calculo.grid(column=0,row=3)

        self.calculo_button = Button(self.work_window, text="Calcular", command=self.calculo_grama)
        self.calculo_button.grid(column=0,row=4, padx=9, pady=9)


        Label(self.work_window, text=f"Cotação do dia: {self.final}", font="Arial,17", foreground="blue").grid(column=0, row=10, sticky=W+E)


        self.work_window.mainloop()




class loginwindow:

    def logar(self):

        self.table_users = "users"
        self.user = self.user_entry.get()
        self.password = self.password_entry.get()
        self.cursor.execute("""
        SELECT * FROM users;
        """)

        for i in self.cursor.fetchall():
            if self.user in i and self.password in i:
                try:
                    workwindow()
                except:
                    raise Exception("Não foi possível logar")

        


    def __init__(self):


        self.login_window = Toplevel()
        self.login_window.title("Login")
        self.login_window.resizable(False,False)
        self.login_window.iconbitmap("teste\\login.ico")

        self.conn = sqlite3.connect('teste\\banco_de_dados_teste.db')
        self.cursor = self.conn.cursor()


        self.user_name = Label(self.login_window, text="Login:", font="20")
        self.user_name.grid(column=0,row=0, padx=20)
        self.user_entry = Entry(self.login_window)
        self.user_entry.grid(column=1, row=0, padx=20)
        self.user_final = self.user_entry.get()

        self.user_password = Label(self.login_window, text="Senha:", font="20")
        self.user_password.grid(column=0,row=1, padx=20)
        self.password_entry = Entry(self.login_window, show="*")
        self.password_entry.grid(column=1, row=1, padx=20)

        self.button_show = Button(self.login_window,text="Logar", command=self.logar)
        self.button_show.grid(column=2, row=1, padx=20)

        self.login_window.mainloop()


class mainwindow:

    def signup_window(self):
        try:
            signupwindow()

        except:
            raise Exception("Não foi possível abrir Cadastro.")

    def login_window(self):
        try:
            loginwindow()
        except:
            raise Exception("Não foi possível abrir o Login.")

    def quit_window(self):
        if messagebox.askokcancel("Desenvolvido por TyP","Você deseja sair?"):
            self.main_window.destroy()

    def __init__(self):
        self.main_window = Tk()
        self.main_window.title("Venda de Jóias")
        self.main_window.resizable(False,False)
        self.main_window.protocol("WM_DELETE_WINDOW")
        self.main_window.iconbitmap("teste\\login.ico")
        self.img_window = ImageTk.PhotoImage(Image.open("teste\\login.png").resize((50,50)))
        self.img_label = Label(self.main_window, image=self.img_window)
        self.img_label.grid(column=0,row=0)

        self.acesso = HTMLSession()
        self.link = self.acesso.get("https://goldrate.com/pt-br/grama-do-ouro-preco-cotacao-valor/")
        self.html = BeautifulSoup(self.link.text, 'lxml')
        self.valor = self.html.find('em', class_="price-value")
        self.valor_exato = float(self.valor.text)
        self.final = self.valor_exato

        Label(self.main_window, text="Bem Vindo", font="Arial, 20").grid(column=0, row=1)
        Label(self.main_window, text=f"Cotação do dia: {self.final}", font="Arial,17", foreground="blue").grid(column=0, row=4, sticky=W+E)

        self.button_login = Button(self.main_window, text="Entrar", foreground="White", font="Arial", command=self.login_window)
        self.button_login.configure(width=18, height=2, foreground="white", background="black", borderwidth=2)
        self.button_login.grid(row=2, column=0,rowspan=2, columnspan=2, sticky=N, padx=2,pady=2)



        self.menu_bar = Menu(self.main_window)
        self.menu_bar.add_separator()

        self.button_menu = Menu(self.menu_bar, tearoff=0)
        self.button_menu.add_command(label="Cadastrar", command=self.signup_window)
        self.menu_bar.add_separator()
        self.button_menu.add_command(label="Sair", command=self.quit_window)
        self.menu_bar.add_cascade(label="Arquivos", menu=self.button_menu)

        self.menu_bar.add_separator()


        self.main_window.configure(menu=self.menu_bar)
        self.main_window.mainloop()


try:
    mainwindow()
except:
    raise Exception("Erro ao Abrir.")