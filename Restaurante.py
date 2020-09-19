import pymysql.cursors
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import random




class JanelaDeLogin():

    def __init__(self):
        self.root = Tk()
        self.root.title('Pizzaria')
        Label(self.root, text='Faça seu Login').grid(row=0, column=0, columnspan=2)
        Label(self.root, text='Usuário').grid(row=1, column=0)
        self.usuario = Entry(self.root)
        self.usuario.grid(row=1, column=1, padx=5, pady=5)
        Label(self.root, text='Senha').grid(row=2, column=0)
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)
        Button(self.root, text='Login', bg='green3', command=self.verificaLogin).grid(row=3, column=0, padx=5, pady=5)
        Button(self.root, text='Cadastro', bg='yellow', command=self.destroiTela).grid(row=3, column=1, padx=5, pady=5)
        self.root.mainloop()

    def verificaLogin(self):
        global conexao
        autenticado = False
        usuarioMaster = False
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='restaurante',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_01', 'Erro no Banco de Dados')
        usuario = self.usuario.get()
        senha = self.senha.get()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultadoCadastro = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_02', 'Erro no Banco de Dados')
        for linha in resultadoCadastro:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1 or linha['nivel'] == 3:
                    usuarioMaster = False
                else:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:
            messagebox.showinfo('Login', 'Usuário ou Senha Inválidos')
        else:
            self.root.destroy()
            if usuarioMaster:
                JanelaAdministração()
            else:
                JanelaCliente()

    def destroiTela(self):
        self.root.destroy()
        Cadastro()

class Cadastro():

    def __init__(self):
        self.root = Tk()
        self.x = random.randrange(0, 1000000)
        self.root.title('Cadastro')
        Label(self.root, text='Cadastro').grid(row=0, column=0, columnspan=2)
        Label(self.root, text='Usuário').grid(row=1, column=0)
        Label(self.root, text='Senha').grid(row=2, column=0)
        Label(self.root, text='Repetir Senha').grid(row=3, column=0)
        Label(self.root, text='Digite os Números Abaixo:').grid(row=4, column=0, columnspan=2)
        Label(self.root, text=self.x).grid(row=5, column=0, columnspan=2)
        self.numero = Entry(self.root)
        self.numero.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.usuario = Entry(self.root)
        self.usuario.grid(row=1, column=1, padx=5, pady=5)
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)
        self.repetirSenha = Entry(self.root, show='*')
        self.repetirSenha.grid(row=3, column=1, padx=5, pady=5)
        Button(self.root, text='Cadastrar', bg='orange', command=self.cadastro).grid(row=7,column=1, padx=5, pady=5)
        Button(self.root, text='Voltar para\n Login', bg='green3', command=self.DestroiJnaelaCadastro).grid(row=7, column=0, padx=5, pady=5)
        self.root.mainloop()

    def cadastro(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='restaurante',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_01', 'Erro no Banco de Dados')
        usuarioExistente = 0
        repetirSenha= self.repetirSenha.get()
        numero = self.numero.get()
        usuario = self.usuario.get()
        senha = self.senha.get()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultadoCadastro = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_03', 'Erro no Banco de Dados')
        for linha in resultadoCadastro:
            if linha['nome'] == usuario:
                usuarioExistente = 1
        if usuarioExistente == 1:
            messagebox.showinfo('Erro_04','Usuário Existente\nTente Novamente')
        elif usuarioExistente == 0:
            if usuario != '':
                if senha == repetirSenha:
                    if numero == str(self.x):
                        try:
                            with conexao.cursor() as cursor:
                                cursor.execute('insert into cadastros(nome, senha, nivel) values(%s, %s, %s)',(usuario, senha, 1))
                                conexao.commit()
                                messagebox.showinfo('Sucesso','Cadastro Concluido com Sucesso')
                                self.root.destroy()
                                JanelaDeLogin()
                        except:
                            messagebox.showinfo('Erro_05','Erro ao Cadastrar!')
                    else:
                        messagebox.showinfo('Erro_07','Os Números foram Digitados Incorretamente')

                else:
                    messagebox.showinfo('Erro_06','As Senhas Devem ser Iguais')
            else:
                messagebox.showinfo('Erro_12', 'O campo Usuário deve ser Preenchido')

    def DestroiJnaelaCadastro(self):
        self.root.destroy()
        JanelaDeLogin()

class JanelaAdministração():

    def __init__(self):
        self.root = Tk()
        self.root.title('Administração')
        Button(self.root, text='Pedidos', bg='orange', command=self.destruidoDeTelaAdministraçãoPedido).grid(row=0, column=0, padx=5, pady=5)
        Button(self.root, text='Cadastrar Produtos', bg='orange',command=self.destruidoDeTelaAdministraçãoCadastroProduto).grid(row=1, column=0, padx=5, pady=5)
        Button(self.root, text='Funcionários', bg='orange', command=self.destruidoDeTelaAdministraçãoFuncionario).grid(row=2, column=0, padx=5, pady=5)
        Button(self.root, text='Sair', bg='red', command=self.sair).grid(row=4, column=0, padx=5, pady=5)
        Button(self.root, text='Estatítica de Vendas', bg='orange', command=self.destruidoDeTelaAdministraçãoEstatistica).grid(row=3, column=0, padx=5, pady=5)

        self.root.mainloop()

    def destruidoDeTelaAdministraçãoFuncionario(self):
        self.root.destroy()
        Funcionarios()

    def destruidoDeTelaAdministraçãoCadastroProduto(self):
        self.root.destroy()
        CadastraProdutos()

    def destruidoDeTelaAdministraçãoPedido(self):
        self.root.destroy()
        Pedidos()

    def destruidoDeTelaAdministraçãoEstatistica(self):
        self.root.destroy()
        JanelaEstatistica()

    def sair(self):
        self.root.destroy()
        JanelaDeLogin()

class Pedidos():

    def __init__(self):
        self.root = Tk()
        self.root.title('Pedidos')
        Button(self.root, text='Concluir Pedido', bg='orange', command=self.concluirPedido).grid(row=0, column=0, padx=5, pady=5)
        Button(self.root, text='Atualizar', bg='orange', command=self.atualiza).grid(row=1, column=0, padx=5, pady=5)
        Button(self.root, text='Sair', bg='red', command=self.voltar).grid(row=2, column=0, padx=5, pady=5)
        self.atualiza()
        self.root.mainloop()

    def concluirPedido(self):
        idComprar = self.tree.selection()[0]
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_', 'Erro no Banco de Dados')
        for i in resultado:
            if i['id'] == int(idComprar):
                try:
                    with conexao.cursor() as cursor:
                        cursor.execute('delete from pedidos where id = {}'.format(idComprar))
                        conexao.commit()
                        messagebox.showinfo('Sucesso', 'Produto Concluido!')
                        self.atualiza()


                except:
                    messagebox.showinfo('Erro_7478', 'Erro no Banco de Dados')

    def voltar(self):
        self.root.destroy()
        JanelaAdministração()

    def atualiza(self):
        self.tree = ttk.Treeview(self.root, selectmode='browse', column=('column1', 'column2', 'column3', 'column4', 'column5'), show='headings')
        self.tree.column('column1', width=110, stretch=NO)
        self.tree.heading('#1', text='Nome')
        self.tree.column('column2', width=350, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        self.tree.column('column3', width=100, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        self.tree.column('column4', width=110, stretch=NO)
        self.tree.heading('#4', text='Endereço')
        self.tree.column('column5', width=90, stretch=NO)
        self.tree.heading('#5', text='Observações')
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='restaurante',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_24', 'Erro no Banco de Dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                self.resultado = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_25', 'Erro no Banco de Dados')
        for i in self.resultado:
                lis = []
                print(i)
                lis.append(i['nome'])
                lis.append(i['ingredientes'])
                lis.append(i['grupo'])
                lis.append(i['localEntrega'])
                lis.append(i['observacoes'])
                self.tree.insert('', END, values=lis, iid=i['id'], tag='1')
        self.tree.grid(row=0, column=1, padx=10, pady=10, columnspan=5, rowspan=3)

class CadastraProdutos():

    def __init__(self):
        self.root = Tk()
        self.root.title('Cadastro de Produtos')
        Label(self.root, text='Cadastar Produtos').grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        Label(self.root, text='Nome').grid(row=1, column=0, padx=5, pady=5)
        self.nome = Entry(self.root)
        self.nome.grid(row=1, column=1, padx=5, pady=5)
        Label(self.root, text='Ingredientes').grid(row=2, column=0, padx=5, pady=5)
        self.ingredientes = Entry(self.root)
        self.ingredientes.grid(row=2, column=1, padx=5, pady=5)
        Label(self.root, text='Grupo').grid(row=3, column=0, padx=5, pady=5)
        self.grupo = Entry(self.root)
        self.grupo.grid(row=3, column=1, padx=5, pady=5)
        Label(self.root, text='Preço').grid(row=4, column=0, padx=5, pady=5)
        self.preco = Entry(self.root)
        self.preco.grid(row=4, column=1, padx=5, pady=5)
        Button(self.root, text='Cadastrar', bg='orange', command=self.cadastrarProduto).grid(row=5, column=0, padx=5, pady=5)
        Button(self.root, text='Excluir', bg='orange', command=self.Excluir).grid(row=5, column=1, padx=5, pady=5)
        Button(self.root, text='Atualizar', bg='orange', command=self.atualiza).grid(row=6, column=0, padx=5, pady=5)
        Button(self.root, text='Voltar', bg='orange', command=self.voltar).grid(row=6, column=1, padx=5, pady=5)
        self.atualiza()
        self.root.mainloop()

    def cadastrarProduto(self):
        if self.nome.get() != '':
            if self.ingredientes.get() != '':
                if self.grupo.get() != '':
                    if self.preco.get() != '':
                        try:
                            with conexao.cursor() as cursor:
                                cursor.execute('insert into produtos(nome, ingredientes, grupo, preco) values(%s, %s, %s, %s)',(self.nome.get(), self.ingredientes.get(), self.grupo.get(), int(self.preco.get())))
                                conexao.commit()
                                self.atualiza()
                        except:
                            messagebox.showinfo('Erro_23', 'Erro no Banco de Dados')

                    else:
                        messagebox.showinfo('Erro_22', 'Campo Preço em Braco')

                else:
                    messagebox.showinfo('Erro_21', 'Campo grupo em Braco')

            else:
                messagebox.showinfo('Erro_20', 'Campo Ingredientes em Braco')

        else:
            messagebox.showinfo('Erro_19', 'Campo Nome em Braco')

    def Excluir(self):
        idDeletar = int(self.tree.selection()[0])
        try:
            with conexao.cursor() as cursor:
                cursor.execute('delete from produtos where id = {}'.format(idDeletar))
                conexao.commit()
                self.atualiza()


        except:
                messagebox.showinfo('Erro_18', 'Erro no Banco de Dados')

    def atualiza(self):
        self.tree = ttk.Treeview(self.root, selectmode='browse', column=('column1', 'column2', 'column3', 'column4'), show='headings')
        self.tree.column('column1', width=110, stretch=NO)
        self.tree.heading('#1', text='Nome')
        self.tree.column('column2', width=350, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        self.tree.column('column3', width=100, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        self.tree.column('column4', width=40, stretch=NO)
        self.tree.heading('#4', text='Preço')
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='restaurante',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_16', 'Erro no Banco de Dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                self.resultado = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_17', 'Erro no Banco de Dados')
        for i in self.resultado:
                lis = []
                print(i)
                lis.append(i['nome'])
                lis.append(i['ingredientes'])
                lis.append(i['grupo'])
                lis.append(i['preco'])
                self.tree.insert('', END, values=lis, iid=i['id'], tag='1')
        self.tree.grid(row=0, column=2, padx=10, pady=10, columnspan=4, rowspan=7)

    def voltar(self):
        self.root.destroy()
        JanelaAdministração()

class Funcionarios():

    def __init__(self):
        self.root = Tk()
        self.root.title('Funcionários')
        Label(self.root, text='Contratar Funcionários').grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        Label(self.root, text='Usuário').grid(row=1, column=0, padx=5, pady=5)
        self.usuario = Entry(self.root)
        self.usuario.grid(row=1, column=1, padx=5, pady=5)
        Label(self.root, text='Senha').grid(row=2, column=0, padx=5, pady=5)
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)
        Label(self.root, text='Nivel').grid(row=3, column=0, padx=5, pady=5)
        self.nivel = Entry(self.root)
        self.nivel.grid(row=3, column=1, padx=5, pady=5)
        Button(self.root, text='Contratar', bg='orange', command=self.contratar).grid(row=4, column=0, padx=5, pady=5)
        Button(self.root, text='Demitir', bg='orange', command=self.demitir).grid(row=4, column=1, padx=5, pady=5)
        Button(self.root, text='Atualizar', bg='orange', command=self.atualiza).grid(row=5, column=0, padx=5, pady=5)
        Button(self.root, text='Voltar', bg='orange', command=self.voltar).grid(row=5, column=1, padx=5, pady=5)
        self.atualiza()
        self.root.mainloop()

    def atualiza(self):
        self.tree = ttk.Treeview(self.root, selectmode='browse', column=('column1', 'column2'), show='headings')
        self.tree.column('column1', width=100, stretch=NO)
        self.tree.heading('#1', text='Nome')
        self.tree.column('column2', width=40, stretch=NO)
        self.tree.heading('#2', text='Nível')
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='restaurante',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_08', 'Erro no Banco de Dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                self.resultado = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_09', 'Erro no Banco de Dados')
        for i in self.resultado:
            if i['nivel'] == 2 or i['nivel'] == 3:
                lis = []
                print(i)
                lis.append(i['nome'])
                lis.append(i['nivel'])
                self.tree.insert('', END, values=lis, iid=i['id'], tag='1')
        self.tree.grid(row=0, column=2, padx=10, pady=10, columnspan=3, rowspan=6)

    def contratar(self):
        usuario = self.usuario.get()
        senha = self.senha.get()
        nivel = self.nivel.get()
        if usuario != '':
            if nivel == '2' or nivel == '3':
                try:
                    with conexao.cursor() as cursor:
                        cursor.execute('insert into cadastros(nome, senha, nivel) values(%s, %s, %s)',(usuario, senha, int(nivel)))
                        conexao.commit()
                        self.atualiza()


                except:
                    messagebox.showinfo('Erro_10', 'Erro no Banco de Dados')
            else:
                messagebox.showinfo('Erro_11','Digite 2 para Administrador\n Digite 3 para Funcionário')

        else:
            messagebox.showinfo('Erro_13', 'O campo Usuário deve ser Preenchido')

    def voltar(self):
        self.root.destroy()
        JanelaAdministração()

    def demitir(self):
        idDeletar = int(self.tree.selection()[0])
        try:
            with conexao.cursor() as cursor:
                cursor.execute('delete from cadastros where id = {}'.format(idDeletar))
                conexao.commit()
                self.atualiza()


        except:
                messagebox.showinfo('Erro_14', 'Erro no Banco de Dados')

class JanelaCliente():
    def __init__(self):
        self.root = Tk()
        self.root.title('Cliente')
        self.atualiza()
        Button(self.root, text='Comprar Produto', bg='orange', command=self.comprarProduto).grid(row=6, column=0, padx=5, pady=5)
        Button(self.root, text='Atualizar', bg='orange', command=self.atualiza).grid(row=6, column=2, padx=5, pady=5)
        Button(self.root, text='Sair', bg='red', command=self.sair).grid(row=7, column=1, padx=5, pady=5)
        Label(self.root, text='Endereço').grid(row=5, column=0, pady=5)
        self.endereco = Entry(self.root)
        self.endereco.grid(row=5, column=1, pady=5)
        Label(self.root, text='Observação').grid(row=5, column=2, pady=5)
        self.observacao = Entry(self.root)
        self.observacao.grid(row=5, column=3,pady=5)

        self.root.mainloop()

    def sair(self):
        self.root.destroy()
        JanelaDeLogin()

    def atualiza(self):
        self.tree = ttk.Treeview(self.root, selectmode='browse', column=('column1', 'column2', 'column3', 'column4'), show='headings')
        self.tree.column('column1', width=110, stretch=NO)
        self.tree.heading('#1', text='Nome')
        self.tree.column('column2', width=350, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        self.tree.column('column3', width=100, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        self.tree.column('column4', width=40, stretch=NO)
        self.tree.heading('#4', text='Preço')
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='restaurante',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_24', 'Erro no Banco de Dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                self.resultado = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_25', 'Erro no Banco de Dados')
        for i in self.resultado:
                lis = []
                print(i)
                lis.append(i['nome'])
                lis.append(i['ingredientes'])
                lis.append(i['grupo'])
                lis.append(i['preco'])
                self.tree.insert('', END, values=lis, iid=i['id'], tag='1')
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=4, rowspan=5)

    def comprarProduto(self):
        idComprar = self.tree.selection()[0]
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_', 'Erro no Banco de Dados')

        for i in resultado:
            if i['id'] == int(idComprar):
                if self.endereco.get() != '':
                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute('insert into pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values(%s,%s,%s,%s,%s)',(i['nome'], i['ingredientes'], i['grupo'], self.endereco.get(), self.observacao.get()))
                            cursor.execute('insert into estatisticavendido (nome, grupo, preco) values(%s,%s,%s)',(i['nome'], i['grupo'], i['preco']))
                            conexao.commit()
                            messagebox.showinfo('Sucesso', 'Produto Comprado com Sucesso!')
                            self.atualiza()


                    except:
                        messagebox.showinfo('Erro_7478', 'Erro no Banco de Dados')
                else:
                    messagebox.showinfo('Erro_','O campo Endereço etá em Branco')

class JanelaEstatistica():

    def __init__(self):

        self.root = Tk()
        self.root.title("Estatística")
        Button(self.root, text='Dinheiro', bg='orange', width=50, command=self.produtoDinheiro).grid(row=0, column=0, padx=5, pady=5)
        Button(self.root, text='Unidade', width=50, bg='orange', command=self.produtoUnidade).grid(row=1, column=0, padx=5, pady=5)
        Button(self.root, text='Voltar', width=50, bg='red', command=self.voltar).grid(row=2, column=0, padx=5, pady=5)
        self.root.mainloop()

    def produtoDinheiro(self):
        NomeProduto = []
        NomeProduto.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                produtos = cursor.fetchall()
        except:
            messagebox.showinfo('Erro','Erro ao Acessar o Banco de Dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select *  from estatisticavendido')
                estatistica = cursor.fetchall()
        except:
            messagebox.showinfo('Erro', 'Erro ao Acessar o Banco de Dados')
        for i in produtos:
            NomeProduto.append(i['nome'])
        listaPreco = []
        listaPreco.clear()
        for i in NomeProduto:
            valor = 0
            for k in estatistica:
                if i == k['nome']:
                    valor += k['preco']
                else:
                    valor += 0
            listaPreco.append(valor)
        plt.plot(NomeProduto, listaPreco)
        plt.xlabel("Produto")
        plt.ylabel("Quantidade Vendida em Reais")
        plt.show()

    def produtoUnidade(self):
        NomeProduto = []
        NomeProduto.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                produtos = cursor.fetchall()
        except:
            messagebox.showinfo('Erro', 'Erro ao Acessar o Banco de Dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select *  from estatisticavendido')
                estatistica = cursor.fetchall()
        except:
            messagebox.showinfo('Erro', 'Erro ao Acessar o Banco de Dados')
        for i in produtos:
            NomeProduto.append(i['nome'])
        listaQt = []
        listaQt.clear()
        for i in NomeProduto:
            valor = 0
            for k in estatistica:
                if i == k['nome']:
                    valor += 1
                else:
                    valor += 0
            listaQt.append(valor)
        plt.plot(NomeProduto, listaQt)
        plt.xlabel("Produto")
        plt.ylabel("Quantidade Vendida")
        plt.show()

    def voltar(self):
        self.root.destroy()
        JanelaAdministração()

JanelaDeLogin()
