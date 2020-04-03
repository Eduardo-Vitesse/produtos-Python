from tkinter import *
from tkinter import ttk
from dbConfig import run_query

# Função para Listar os Produtos
def get_products():
    # Limpando a tabela
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    # Consultando os dados
    query = 'SELECT * FROM product ORDER BY name DESC'
    db_rows = run_query(query)
    for row in db_rows:
        tree.insert('', 0, text=row[1], values=row[2])

def validation():
    return len(name.get()) != 0 and len(price.get()) != 0

# Função para Adicionar um Produto
def add_product():
    if validation() == True:
        query = 'INSERT INTO product VALUES(NULL, ?, ?)'
        parameters = (name.get(), price.get())
        run_query(query, parameters)
        msg['text'] = f'Produto {name.get()} adicionado!'
        name.delete(0, END)
        price.delete(0, END)
    else:
        msg['text'] = 'FALHA... Preencha todos os campos'
    get_products()

# Função para Deletar um Produto
def dlelete_product():
    msg['text'] = ''
    try:
        tree.item(tree.selection())['text'][0]
    except IndexError as e:
        msg['text'] = 'Selecione algum produto'
        return
    msg['text'] = ''
    produto = tree.item(tree.selection())['text']
    query = 'DELETE FROM product WHERE name = ?'
    run_query(query, (produto, ))#Adicionar uma virgula e um espaço para reconhecer como tupla
    msg['text'] = f'Produto {produto} foi DELETADO'
    get_products()

# Função para Editar os Produto
def edit_product():
    msg['text'] = ''
    try:
        tree.item(tree.selection())['text'][0]
    except IndexError as e:
        msg['text'] = 'Selecione algum produto'
        return
    old_name = tree.item(tree.selection())['text']
    old_price = tree.item(tree.selection())['values'][0]
    #Criando uma nova janela para editar
    edit_wind = Toplevel()
    edit_wind.title("Editar produtos")

    Label(edit_wind, text="Name: ").grid(row=1, column=0)
    new_name = Entry(edit_wind, textvariable= StringVar(edit_wind, value=old_name))# ,state='readonly'
    new_name.grid(row=1, column=1, pady=2)

    Label(edit_wind, text="Price: ").grid(row=2, column=0)
    new_price = Entry(edit_wind, textvariable= StringVar(edit_wind, value=old_price))
    new_price.grid(row=2, column=1, pady=2)

    ttk.Button(edit_wind, text="UPDATE", command=lambda:updat_product(new_name.get(), old_name, new_price.get(), old_price)).grid(row=3, columnspan=2, sticky=W + E, pady=5)

    def updat_product(new_name, old_name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, old_name, old_price)
        run_query(query, parameters)
        edit_wind.destroy()
        msg['text'] = f'Produto {old_name} Atualizado'
        get_products()

wind = Tk()
wind.title("Products Aplications")


# Create a Frame (div)
frame = LabelFrame(wind, text="Add New Product")
frame.grid(row=0, column=0, columnspan=3, pady=20)

# Name Input
Label(frame, text="Name: ").grid(row=1, column=0)
name = Entry(frame)
name.focus()
name.grid(row=1, column=1)

# Price Input
Label(frame, text="Price: ").grid(row=2, column=0)
price = Entry(frame)
price.grid(row=2, column=1)

# Button add product
ttk.Button(frame, text="Save Product", command=add_product).grid(row=3, columnspan=2, sticky=W + E)

msg = Label(wind, text="", fg='red')
msg.grid(row=3, column=0, columnspan=2, sticky=W + E)

# Table
tree = ttk.Treeview(wind, height=10, columns=2)
tree.grid(row=4, column=0, columnspan=2)
tree.heading('#0', text="Name", anchor=CENTER)
tree.heading('#1', text="Price", anchor=CENTER)

# Buttons de DELETE e UPDATE
ttk.Button(wind, text='DELETE', command=dlelete_product).grid(row=5, column=0, sticky=W + E)
ttk.Button(wind, text='EDIT', command=edit_product).grid(row=5, column=1, sticky=W + E)


get_products()

wind.mainloop()