import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x150")

# 1. Botão Tkinter Clássico (Customização direta)
btn_classico = tk.Button(root, text="Botão Clássico", bg="blue", fg="white")
btn_classico.pack(pady=10)

# 2. Botão TTK Temático (Customização via Estilo)
style = ttk.Style()
style.configure("TButton", foreground="blue") # Estilizando todos os botões TTK

btn_ttk = ttk.Button(root, text="Botão TTK")
btn_ttk.pack(pady=10)

root.mainloop()