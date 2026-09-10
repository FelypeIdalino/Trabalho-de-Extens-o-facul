import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#funções
def abrir_janela_Registro():
    print("Abrindo janela para registrar no db...")
    #inserir codigo acessando e registrando os itens no banco de dados local



def adicionar_carrinho():
    item_selecionado= frame.selection()
    
    if item_selecionado:
        valores = frame.item(item_selecionado, "values")
        print(f"adicionando {valores[1]} ao carrinho..")
        #colocar a logica que verificarar se precisa inserir peso ou não
    else:
        print("Por favor selecione um item na grade primeiro!")
        
        

def adicionar_ao_resumo(item, quantidade_ou_peso, valor_total):
        # Substitua este print pela inserção na sua tabela de Resumo do pedido/Nota Fiscal
        print(f"-> Adicionado ao resumo: {item['nome']} | Qtd/Peso: {quantidade_ou_peso} | Total: R$ {valor_total:.2f}")
        
        

        
def abrir_janela(item):
    janela_peso= tk.Toplevel(root)
    janela_peso.title(f"Peso - {item['nome']}")
    janela_peso.geometry('300x150')
    janela_peso.grab_set()
    
    label_peso= ttk.Label(janela_peso, text=f"Informe o peso em Kg de {item['nome']}:", font=("arial", 10)).pack(pady=10)

    entry_peso= ttk.Entry(janela_peso, justify="center")
    entry_peso.pack(pady=5)


    def confirmar_peso():
        try:
            peso_informado = float(entry_peso.get().replace(",", "."))
            valor_calculado= peso_informado * item['preco']
            
            adicionar_ao_resumo(item, f"{peso_informado:.3f}kg", valor_calculado)
            janela_peso.destroy()
        except ValueError:
            messagebox.showwarning("Erro", "Insira um valor numero valido!!")
            
    ttk.Button(janela_peso, text="Confirmar", command=confirmar_peso).pack(pady=10)

    
    
def processar_clique(item):
    print("foi?")
    if item['peso_variavel'].lower() == 'sim':
        abrir_janela(item)
    else:
        adicionar_ao_resumo(item, "1 un", item['preco'])
        
        
        

    
        
            
    


root = tk.Tk()
root.title("Caixa Campestre")
root.geometry("640x480")
root.state("zoomed")
# root.eval('tk::PlaceWindow . center')

estilo= ttk.Style()
estilo.theme_use('clam')


estilo.configure("Card.TFrame", background="white", relief="raised", borderwidth=2)
estilo.configure("Titulo.TLabel", background="lightblue", font=("Arial", 14, "bold"))
estilo.configure("Preco.TLabel", background="white", font=("Arial", 10))
estilo.configure("bg1.TFrame", background="lightblue")
estilo.configure("bg2.TFrame", background="lightgreen")
estilo.configure("bg2.TLabel", background="lightgreen", foreground="black")



#Frame esquerdo
frame= ttk.Frame(root, padding="10", style="bg1.TFrame")
frame.pack(side="left", fill='both', padx="20", pady="20", expand=True)

label_titulo= ttk.Label(frame, text="Produtos", style="Titulo.TLabel").pack(pady=(2, 10))

container_card = ttk.Frame(frame, style="Card.TFrame")
container_card.pack(fill="both", expand=True)

produtos = [
        {"id": 1, "nome": "Maçã", "preco": 5.50, "peso_variavel": "sim", "cor": "#ffcccc"},
        {"id": 2, "nome": "Refrigerante", "preco": 8.00, "peso_variavel": "não", "cor": "#cce5ff"},
        {"id": 3, "nome": "Pão de Queijo", "preco": 35.90, "peso_variavel": "sim", "cor": "#ffffcc"},
    ]

coluna=0
linha=0
max_colunas= 3

for produto in produtos:
    card= ttk.Frame(container_card, style="Card.TFrame", width=120, height=120)
    card.grid_propagate(False)
    card.grid(row=linha, column=coluna, padx=10, pady=10)
    
    card_nome = ttk.Label(card, text=produto["nome"], style="Titulo.TLabel")
    card_nome.pack(pady=(30, 5))
    
    card_preco = ttk.Label(card, text=f"R$ {produto['preco']:.2f}", style="Preco.TLabel")
    card_preco.pack()

    
    action= lambda event, p=produto: processar_clique(p)
    
    card.bind("<Button-1>", action)
    card_nome.bind("<Button-1>", action)
    card_preco.bind("<Button-1>", action)
        
    
    coluna +=1
    if coluna >= max_colunas:
        coluna = 0
        linha +=1

#botões do Frame Esquerdo

frame_button= ttk.Frame(frame, style="bg1.TFrame")
frame_button.pack(pady=20)

estilo.configure("btn.TButton", background="lightgreen", foreground="black")
estilo.map("btn.TButton", background=[('active', 'green')], )


btn_registro = ttk.Button(frame_button, text="Registrar novo item", command=abrir_janela_Registro, style="btn.TButton")
btn_registro.pack(side="left", padx=5, pady=5)

btn_adicionar = ttk.Button(frame_button, text="Adicionar ao carrinho", command=adicionar_carrinho, style="btn.TButton")
btn_adicionar.pack(side="left", padx=5, pady=5)



#frame Direito
frame1= ttk.Frame(root, padding="10", style="bg2.TFrame")
frame1.pack(side="right", fill="both", padx="20", pady="20", expand=True)

label_Resumo = ttk.Label(frame1, text="Resumo", font=("Arial", 14, "bold"), style="bg2.TLabel")
label_Resumo.pack(pady=(2, 10), anchor="center")

colunas= ("nome", "preco", "peso")
tree_resumo = ttk.Treeview(frame1, columns=colunas, show="headings", height=10)

#estilizando a tabela
estilo.configure("Treeview", font=("Arial", 12), rowheight=24)
estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"))


tree_resumo.heading("nome", text="Nome do item")
tree_resumo.heading("preco", text="Preço (R$)")
tree_resumo.heading("peso", text="Peso(Kg)/Quantidade")

tree_resumo.column("nome", width=200, anchor="w")
tree_resumo.column("preco", width=100, anchor="center")
tree_resumo.column("peso", width=100, anchor="center")

scrollbar= ttk.Scrollbar(frame1, orient="vertical", command=tree_resumo.yview)
tree_resumo.configure(yscrollcommand=scrollbar.set)

tree_resumo.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

dados_teste = [
        ("Maçã", 5.50, 1.25),
        ("Arroz 5kg", 25.00, 1),
        ("Pão Francês", 0.50, 0.880),
        ("Tomate", 6.00, 1.200),
        ("Feijão 1kg", 8.90, 1)
    ]

for i in dados_teste:
    nome= i[0]
    preco_formatado= f'R$ {i[1]:.2f}'
    peso_formatado= f"{i[2]:.2f} Kg"
    
    tree_resumo.insert("", "end", values=(nome, preco_formatado, peso_formatado))



root.mainloop()