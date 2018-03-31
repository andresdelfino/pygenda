import shelve
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.ttk as ttk

class InformacionPersonal(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.nombre = tk.StringVar()
        self.direccion = tk.StringVar()
        self.telefono = tk.StringVar()
        self.correo = tk.StringVar()

        ttk.Label(self, text='Nombre:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.nombre).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='Dirección:').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.direccion).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='Teléfono:').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.telefono).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Correo electrónico:').grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.correo).grid(row=3, column=1, padx=5, pady=5)

    def validar(self):
        return self.nombre.get() and (self.direccion.get() or self.telefono.get() or self.correo.get())

class CrearContacto(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.user_info = InformacionPersonal(self)
        self.user_info.grid(row=0, column=0)

        ttk.Button(self, text='Guardar', command=self.guardar).grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

    def guardar(self):
        if not self.user_info.validar():
            tkmsgbox.showerror('Error', 'El contacto debe tener un nombre y al menos una forma de contacto')
            return

        valores = (
            self.user_info.direccion.get(),
            self.user_info.telefono.get(),
            self.user_info.correo.get(),
        )

        self.master.master.treeview.insert('', tk.END, text=self.user_info.nombre.get(), values=valores)

        self.master.destroy()

class ModificarContacto(ttk.Frame):
    def __init__(self, master, item):
        super().__init__(master)

        self.item = item

        self.user_info = InformacionPersonal(self)
        self.user_info.grid(row=0, column=0)

        ttk.Button(self, text='Guardar', command=self.guardar).grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

        self.cargar()

    def cargar(self):
        item_data = self.master.master.treeview.item(self.item)

        self.user_info.nombre.set(item_data['text'])
        self.user_info.direccion.set(item_data['values'][0])
        self.user_info.telefono.set(item_data['values'][1])
        self.user_info.correo.set(item_data['values'][2])

    def guardar(self):
        if not self.user_info.validar():
            tkmsgbox.showerror('Error', 'El contacto debe tener nombre y al menos una forma de contacto.')
            return

        valores = (
            self.user_info.direccion.get(),
            self.user_info.telefono.get(),
            self.user_info.correo.get(),
        )

        self.master.master.treeview.item(self.item, text=self.user_info.nombre.get(), values=valores)

        self.master.destroy()

class Pygenda(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title('Pygenda 2018 Home & Business - UNREGISTERED VERSION')
        self.master.protocol('WM_DELETE_WINDOW', self.salir)
        self.master.resizable(0, 0)
        self.master['padx'] = 10
        self.master['pady'] = 10

        ttk.Button(self, text='Crear', command=self.crear).grid(row=0, column=0, padx=5, pady=5)

        self.boton_modificar = ttk.Button(self, text='Modificar', command=self.modificar_button, state=tk.DISABLED)
        self.boton_modificar.grid(row=0, column=1, padx=5, pady=5)

        self.boton_eliminar = ttk.Button(self, text='Eliminar', command=self.eliminar, state=tk.DISABLED)
        self.boton_eliminar.grid(row=0, column=2, padx=5, pady=5)

        self.treeview = ttk.Treeview(self, columns=('Dirección', 'Teléfono', 'Correo'), selectmode=tk.BROWSE)
        self.treeview.heading('#0', text='Nombre')
        self.treeview.heading('Dirección', text='Dirección')
        self.treeview.heading('Teléfono', text='Teléfono')
        self.treeview.heading('Correo', text='Correo electrónico')
        self.treeview.bind('<Button-1>', self.item_seleccionado)
        self.treeview.bind('<Double-Button-1>', self.modificar_dobleclick)
        self.treeview.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.cargar()

    def cargar(self):
        if 'contactos' in agenda:
            for contacto in agenda['contactos']:
                self.treeview.insert('', tk.END, text=contacto[0], values=contacto[1:])

    def crear(self):
        toplevel = tk.Toplevel(self, padx=10, pady=10)
        toplevel.resizable(0, 0)
        toplevel.title('Crear contacto')

        CrearContacto(toplevel).pack()

        toplevel.grab_set()
        toplevel.focus_set()
        self.wait_window(toplevel)

    def eliminar(self):
        focused_item = self.treeview.focus()
        if focused_item and tkmsgbox.askyesno(title='Eliminar contacto', message='¿Está seguro que desea eliminar el contacto?'):
            self.treeview.delete(focused_item)
            self.boton_modificar['state'] = tk.DISABLED
            self.boton_eliminar['state'] = tk.DISABLED

    def item_seleccionado(self, event):
        if self.treeview.identify('region', event.x, event.y) in ('cell', 'tree'):
            self.boton_modificar['state'] = tk.NORMAL
            self.boton_eliminar['state'] = tk.NORMAL

    def modificar(self, item):
        toplevel = tk.Toplevel(self, padx=10, pady=10)
        toplevel.resizable(0, 0)
        toplevel.title('Modificar contacto')

        ModificarContacto(toplevel, item).pack()

        toplevel.grab_set()
        toplevel.focus_set()
        self.wait_window(toplevel)

    def modificar_button(self):
        focused_item = self.treeview.focus()
        if focused_item:
            self.modificar(focused_item)

    def modificar_dobleclick(self, event):
        if self.treeview.identify('region', event.x, event.y) in ('cell', 'tree'):
            self.modificar(self.treeview.identify_row(event.y))

    def salir(self):
        contactos = []
        for item in self.treeview.get_children():
            item_data = self.treeview.item(item)
            contactos.append((item_data['text'], *item_data['values']))
        agenda['contactos'] = contactos

        self.master.destroy()

with shelve.open('agenda') as agenda:
    root = tk.Tk()
    Pygenda(root).pack()
    root.mainloop()
