import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def exibir_mensagem():
    nome = entry_nome.get()
    estado = combo_estados.get()
    
    
    if not nome.strip() or not estado.strip():
        messagebox.showwarning("Aviso!", "Por favor não deixe nenhum campo vazio!")
    else:
        messagebox.showinfo("Sucesso!", f"ola! {nome}, é  muito bom saber que você veio de {estado}")
        
    
    # if nome.strip():
    #     messagebox.showinfo("Sucesso!", f"ola! {nome}, é  muito bom saber que você veio de {estado}")
    # elif not nome.strip():
    #     messagebox.showwarning("Aviso!", f"Porfavor digite seu nome!")
    # elif not estado.strip():
    #     messagebox.showwarning("Aviso!", f"selecio algum estado!")
        
        



root = tk.Tk()
root.title("Caixa Campestre")
root.geometry("640x480")
root.state("zoomed")
# root.eval('tk::PlaceWindow . center')

estilo= ttk.Style()

estilo.configure("bg1.TFrame", background="lightblue")
estilo.configure("bg2.TFrame", background="lightgreen")
estilo.configure("bg2.TLabel", background="lightgreen", foreground="black")



#Frame esquerdo
frame= ttk.Frame(root, padding="10", style="bg1.TFrame")
frame.pack(side="left", fill='both', padx="20", pady="20", expand=True)

label_titulo= ttk.Label(frame, text="Label do container", font=("Arial", 14, "bold"))
label_titulo.pack(pady=(2, 10))

ttk.Label(frame, text="Qual Seu nome?").pack(pady=(2, 10))
entry_nome = ttk.Entry(frame, width=45)
entry_nome.pack(pady=(2, 10))


estados = ["MG", "SP", "RJ", "ES", "PR", "SC", "RS", "Outro"]
ttk.Label(frame, text="Qual seu estado", font=("Arial", 14, "bold")).pack(pady=(2,10))
combo_estados = ttk.Combobox(frame, values=estados, state="readonly")
combo_estados.pack(pady=(2, 15))
btn_enviar = ttk.Button(frame, text="Enviar Saudação", command=exibir_mensagem).pack(fill='x')



#frame Direito
frame1= ttk.Frame(root, padding="10", style="bg2.TFrame")
frame1.pack(side="right", fill="both", padx="20", pady=(20, 240), expand=True)

label_Resumo = ttk.Label(frame1, text="Resumo", font=("Arial", 14, "bold"), style="bg2.TLabel")
label_Resumo.pack(pady=(2, 10), anchor="center")

colunas= ("nome", "preco", "peso")
tree_resumo = ttk.Treeview(frame1, columns=colunas, show="headings", height=10)

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
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Tomate", 6.00, 1.200),
        ("Feijão 1kg", 8.90, 1)
    ]

for i in dados_teste:
    nome= i[0]
    preco_formatado= f'R$ {i[1]:.2f}'
    peso_formatado= f"{i[2]:.2f} Kg"
    
    tree_resumo.insert("", "end", values=(nome, preco_formatado, peso_formatado))



root.mainloop()