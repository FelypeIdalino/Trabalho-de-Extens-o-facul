import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


#classe para os Produtos
class Produto:
    def __init__(self, id, nome, preco, peso):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.peso = bool(peso)


#Banco De Dados
def buscar_produtos():
    try:
        #criando cursor
        conexao= sqlite3.connect("campestre.bd")
        cursor= conexao.cursor()
        cursor.execute("SELECT * FROM Produtos")
        reg_produtos= cursor.fetchall()
        produtos_bd=[]
        
        for i in reg_produtos:
            produto= Produto(*i)
            produtos_bd.append(produto)
        
        conexao.close()
        return produtos_bd
    except sqlite3.Error as e:
        print(f"Não foi possivel se conectar ao banco de dados! Erro:{e}")
        return []
     


#funções
def abrir_janela_Registro():
        
    #Criando a Janela para Registro
    janela_reg = tk.Toplevel(root)
    janela_reg.title("Novo Registro")
    janela_reg.geometry("350x300")
    janela_reg.grab_set()
    
    janela_reg.configure(bg="lightblue")
    
    ttk.Label(janela_reg, text="Nome do Produto:", style="Titulo.TLabel").pack(pady=(15, 0))
    entry_nome= ttk.Entry(janela_reg, width=30, font=("arial", 10))
    entry_nome.pack(pady=5)
    
    ttk.Label(janela_reg, text="Preço:", style="Titulo.TLabel").pack(pady=(15, 0))
    entry_preco= ttk.Entry(janela_reg, width=30, font=("arial", 10))
    entry_preco.pack(pady=5)
    
    #radio-Button para o peso
    var_peso = tk.IntVar(value=0)
    
    frame_radio = tk.Frame(janela_reg, bg="lightblue")
    frame_radio.pack(pady=15)
    
    ttk.Label(frame_radio, text="Vendido no peso?", style="Titulo.TLabel").pack(side="left", padx=10)
    
    ttk.Radiobutton(frame_radio, text="Nâo", variable=var_peso, value=0).pack(side="left", padx=5)
    ttk.Radiobutton(frame_radio, text="Sim", variable=var_peso, value=1).pack(side="left", padx=5)
    
    def salvar_bd():
        nome = entry_nome.get().strip().capitalize()
        preco_str = entry_preco.get().strip().replace(",", ".")
        peso_bool = var_peso.get()
        
        if not nome or not preco_str:
            messagebox.showwarning("Aviso!", "Por Favor, Preencha todos os campos!!")
            return
        
    
        try:
            
            preco_float = float(preco_str)
            
            conexao= sqlite3.connect("campestre.bd")
            cursor= conexao.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE,
                preco REAL,
                peso INTEGER);''')
            cursor.execute("INSERT INTO Produtos (nome, preco, peso) Values (?, ?, ?)", (nome, preco_float, peso_bool))
            conexao.commit()
            #fechando a conexão
            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso!", f"{nome}, foi Registrado com Sucesso!")
            carregar_produto()
            janela_reg.destroy()
            
        except ValueError:
            messagebox.showwarning("Erro!", f"O Preço deve ser um numero valido! Ex: 5.50")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Erro!", f"Não se pode registrar um item que ja existe na tabela! {nome} Já foi Registrado!!")
        except sqlite3.Error as e:
            messagebox.showwarning("Erro!", f"Erro no banco de dados! Erro: {e}")
            
    ttk.Button(janela_reg, text="Salvar Produto!", command=salvar_bd ,style="btn.TButton").pack(pady=10)


def carregar_produto():
    
    for wid in container_card.winfo_children():
        wid.destroy()
    
    coluna=0
    linha=0
    max_colunas= 5
    
    produtos_cadastro= buscar_produtos()
    
    for produto in produtos_cadastro:
        cor_fundo = "#cce5ff"
        
        card= tk.Frame(container_card, bg=cor_fundo, width=120, height=120)
        card.grid_propagate(False)
        card.grid(row=linha, column=coluna, padx=10, pady=10)
        
        card_nome = tk.Label(card, text=produto.nome, bg=cor_fundo, font=("Arial", 14, "bold"))
        card_nome.pack(pady=(30, 5))
        
        card_preco = tk.Label(card, text=f"R$ {produto.preco:.2f}", font=("Arial", 14, "bold"), bg=cor_fundo)
        card_preco.pack()

        
        action= lambda event, p=produto: processar_clique(p)
        
        card.bind("<Button-1>", action)
        card_nome.bind("<Button-1>", action)
        card_preco.bind("<Button-1>", action)
            
        
        coluna +=1
        if coluna >= max_colunas:
            coluna = 0
            linha +=1


        
def calculo_troco():
    valor_recebido = float(entry_valorpago.get().replace(",", "."))
    
    try:
        if valor_recebido < preco_total_resumo:
            messagebox.showwarning("Aviso!", "O Valor Recebido é menor que o Valor Total da compra!")
        else:
            troco = valor_recebido - preco_total_resumo
            label_troco.config(text=f"Troco: R$ {troco:.2f}")
    except ValueError:
        messagebox.showwarning("Aviso!", "Insira um valor numérico válido para o pagamento!!")
    

def adicionar_ao_resumo(item, quantidade_ou_peso, valor_total):
    
    global preco_total_resumo

    nome= item.nome
    preco_formatado= f"R$ {valor_total:.2f}"
    preco_total_resumo += float(valor_total)
    tree_resumo.insert("", "end", values=(nome, preco_formatado, quantidade_ou_peso))
    
    label_total.config(text=f"Total: R$ {preco_total_resumo:.2f}")
        
        
        
def abrir_janela(item):
    janela_peso= tk.Toplevel(root)
    janela_peso.title(f"Peso - {item.nome}")
    janela_peso.geometry('300x150')
    janela_peso.grab_set()
    
    label_peso= ttk.Label(janela_peso, text=f"Informe o peso em Kg de {item.nome}:", font=("arial", 10)).pack(pady=10)

    entry_peso= ttk.Entry(janela_peso, justify="center")
    entry_peso.pack(pady=5)


    def confirmar_peso():
        try:
            peso_informado = float(entry_peso.get().replace(",", "."))
            valor_calculado= peso_informado * item.preco
            
            adicionar_ao_resumo(item, f"{peso_informado:.2f}kg", valor_calculado)
            janela_peso.destroy()
        except ValueError:
            messagebox.showwarning("Erro", "Insira um valor numero valido!!")
            
    ttk.Button(janela_peso, text="Confirmar", command=confirmar_peso).pack(pady=10)

    
    
def processar_clique(item):
    print("foi?")
    if item.peso:
        abrir_janela(item)
    else:
        adicionar_ao_resumo(item, "1 un", item.preco)    
    


def nova_venda():
    global preco_total_resumo
    
    preco_total_resumo= 0.0
    
    for i in tree_resumo.get_children():
        tree_resumo.delete(i)
        
    entry_valorpago.delete(0, tk.END)
    
    label_troco.configure(text="Troco: R$ 0.00")
    label_total.configure(text="Total: R$ 0.00")


preco_total_resumo= 0

#Criação da Janela Principal
root = tk.Tk()
root.title("Caixa Campestre")
root.geometry("640x480")
root.state("zoomed")
# root.eval('tk::PlaceWindow . center')


#Estilos
estilo= ttk.Style()
estilo.theme_use('clam')


estilo.configure("Card.TFrame", background="white", relief="raised", borderwidth=2)
estilo.configure("Titulo.TLabel", background="lightblue", font=("Arial", 14, "bold"))
estilo.configure("Preco.TLabel", background="white", font=("Arial", 10))
estilo.configure("bg1.TFrame", background="lightblue")
estilo.configure("bg2.TFrame", background="lightgreen")
estilo.configure("bg2.TLabel", background="lightgreen", foreground="black")
estilo.configure("btn.TButton", background="lightgreen", foreground="black", font=("Arial", 12, "bold",))
estilo.map("btn.TButton", background=[('active', 'green')] )



#Frame esquerdo
frame= ttk.Frame(root, padding="10", style="bg1.TFrame")
frame.pack(side="left", fill='both', padx="20", pady="20")

label_titulo= ttk.Label(frame, text="Produtos", style="Titulo.TLabel").pack(pady=(2, 10))

#container contendo os "cards"
container_card = ttk.Frame(frame, style="Card.TFrame")
container_card.pack(fill="both", expand=True)


#botões do Frame Esquerdo
frame_button= ttk.Frame(frame, style="bg1.TFrame")
frame_button.pack(pady=20)




btn_registro = ttk.Button(frame_button, text="Registrar novo item", command=abrir_janela_Registro, style="btn.TButton")
btn_registro.pack(side="left", padx=5, pady=5)

btn_nova_venda= ttk.Button(frame_button, text="Nova Venda", command=nova_venda, style="btn.TButton")
btn_nova_venda.pack(side="left", padx=5, pady=5)


#frame Direito / Resumo
frame1= ttk.Frame(root, padding="10", style="bg2.TFrame")
frame1.pack(side="right", fill="both", padx="20", pady="20", expand=True)

label_Resumo = ttk.Label(frame1, text="Resumo", font=("Arial", 14, "bold"), style="bg2.TLabel")
label_Resumo.pack(pady=(2, 10), anchor="center")

frame_tabela= ttk.Frame(frame1, style="bg2.TFrame")
frame_tabela.pack(fill="both", expand=True)

colunas= ("nome", "preco", "peso")
tree_resumo = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)

#estilizando a tabela
estilo.configure("Treeview", font=("Arial", 12), rowheight=24)
estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"))


tree_resumo.heading("nome", text="Nome do item")
tree_resumo.heading("preco", text="Preço (R$)")
tree_resumo.heading("peso", text="Peso(Kg)/Quantidade")

tree_resumo.column("nome", width=200, anchor="w")
tree_resumo.column("preco", width=100, anchor="center")
tree_resumo.column("peso", width=150, anchor="center")

scrollbar= ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_resumo.yview)
tree_resumo.configure(yscrollcommand=scrollbar.set)

tree_resumo.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_totais= ttk.Frame(frame1, style="bg2.TFrame")
frame_totais.pack(pady=20, fill="x")

label_total= ttk.Label(frame_totais, text="Total: R$ 0,00", font=("Arial", 16, "bold"), style="bg2.TFrame")
label_total.pack(side="bottom", pady=5)

frame_pagamento = ttk.Frame(frame_totais, style="bg2.TFrame")
frame_pagamento.pack(pady=10)

ttk.Label(frame_pagamento, text="Valor recebido (R$):", font=("Arial", 12), style="bg2.TLabel").pack(side="left", padx=5)
entry_valorpago = ttk.Entry(frame_pagamento, width=10, font=("Arial", 12), justify="center")
entry_valorpago.pack(side="left", padx=5)

label_troco = ttk.Label(frame_totais, text="Troco: R$ 0.00", font=("Arial", 16, "bold"), foreground="darkred", background="lightgreen")
label_troco.pack(pady=10)

btn_calculo= ttk.Button(frame_totais, text="Calcular Troco", command=calculo_troco, style="btn.TButton")
btn_calculo.pack(pady=5)


carregar_produto()

root.mainloop()
