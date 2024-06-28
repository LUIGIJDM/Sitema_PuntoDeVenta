from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk

# Conexión a la base de datos (¡Asegúrate de tener XAMPP corriendo!)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="tienda",  # Nombre de tu base de datos
    password=""
)
mycursor = mydb.cursor()

# --- Ventana principal ---
root = tk.Tk()
root.title("TECNOLJDM")
root.geometry("450x580")

# --- Cargar y mostrar el logo ---
try:
    logo_img = Image.open("logoft.png") 
    logo_img = logo_img.resize((230, 230)) 
    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(root, image=logo_photo)
    logo_label.pack(pady=2) 
except FileNotFoundError:
    messagebox.showwarning("Advertencia", "No se encontró el archivo del logo.")

# --- Variables globales ---
carrito = {}  
total = 0

# --- Funciones principales ---
def login():
    login_window = tk.Toplevel(root)
    login_window.title("Inicio de sesión")
    login_window.geometry("300x300")

    # --- Campos de entrada ---
    tk.Label(login_window, text="Usuario:").grid(row=0, column=0, padx=20, pady=10)
    usuario_entry = tk.Entry(login_window)
    usuario_entry.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(login_window, text="Contraseña:").grid(row=1, column=0, padx=20, pady=10)
    contrasena_entry = tk.Entry(login_window, show="*")  # Ocultar la contraseña
    contrasena_entry.grid(row=1, column=1, padx=20, pady=10)

    # --- Funciones de inicio de sesión ---
    def iniciar_sesion_administrador():
        usuario = usuario_entry.get()
        contrasena = contrasena_entry.get()

        if usuario == "admin" and contrasena == "admin":
            login_window.destroy()  # Cerrar la ventana de inicio de sesión
            ventana_administrador()  # Abrir la ventana del administrador
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def iniciar_sesion_cliente():
        usuario = usuario_entry.get()
        contrasena = contrasena_entry.get()

        if usuario == "cliente" and contrasena == "cliente":
            login_window.destroy()  # Cerrar la ventana de inicio de sesión
            ventana_cliente()  # Abrir la ventana del cliente
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # --- Botones ---
    tk.Button(login_window, text="Iniciar sesión como administrador", command=iniciar_sesion_administrador).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(login_window, text="Iniciar sesión como cliente", command=iniciar_sesion_cliente).grid(row=3, column=0, columnspan=2, pady=10)

# --- Funciones del administrados ---
def ventana_administrador():
    admin_window = tk.Toplevel(root)
    admin_window.title("Panel de Administración")

    # --- Campos de entrada ---
    tk.Label(admin_window, text="Nombre del producto:").grid(row=0, column=0, padx=20, pady=20)
    nombre_entry = tk.Entry(admin_window)
    nombre_entry.grid(row=0, column=1, padx=25, pady=20)

    tk.Label(admin_window, text="Serie del producto:").grid(row=1, column=0, padx=20, pady=20)
    serie_entry = tk.Entry(admin_window)
    serie_entry.grid(row=1, column=1, padx=25, pady=20)

    tk.Label(admin_window, text="Cantidad del producto:").grid(row=2, column=0, padx=20, pady=20)
    cantidad_entry = tk.Entry(admin_window)
    cantidad_entry.grid(row=2, column=1, padx=25, pady=20)

    tk.Label(admin_window, text="Precio del producto:").grid(row=3, column=0, padx=20, pady=20)
    precio_entry = tk.Entry(admin_window)
    precio_entry.grid(row=3, column=1, padx=25, pady=20)

    # --- Funciones ---
    def agregar_producto():
        nombre = nombre_entry.get()
        serie = serie_entry.get()
        precio = precio_entry.get()
        cantidad = cantidad_entry.get()

        # --- Validación de datos ---
        if not nombre or not precio or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser números")
            return

        # --- Insertar en la base de datos ---
        sql = f"INSERT INTO productos (nombre, serie, cantidad, precio) VALUES (%s, %s, %s, %s)"
        val = (nombre, serie, cantidad, precio)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        limpiar_campos()

    def buscar_producto():
        nombre_a_buscar = nombre_entry.get()

        # --- Buscar el producto en la base de datos ---
        sql = f"SELECT * FROM productos WHERE nombre = %s"
        val = (nombre_a_buscar,)
        mycursor.execute(sql, val)
        producto = mycursor.fetchone()

        if producto:
            # --- Rellenar los campos con los datos del producto encontrado ---
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, producto[1])  # Nombre
            serie_entry.delete(0, tk.END)
            serie_entry.insert(0, producto[2])  # Serie
            cantidad_entry.delete(0, tk.END)
            cantidad_entry.insert(0, str(producto[3]))  # Cantidad
            precio_entry.delete(0, tk.END)
            precio_entry.insert(0, str(producto[4]))  # Precio
        else:
            messagebox.showerror("Error", "Producto no encontrado")

    def eliminar_producto():
        nombre_a_eliminar = nombre_entry.get()
        if not nombre_a_eliminar:
            messagebox.showerror("Error", "Ingresa el nombre del producto a eliminar")
            return

        # --- Confirmación antes de eliminar ---
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar el producto '{nombre_a_eliminar}'?")
        if confirmacion:
            # Eliminar de la base de datos
            sql = f"DELETE FROM productos WHERE nombre = %s"
            val = (nombre_a_eliminar,)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            limpiar_campos()
        else:
            messagebox.showinfo("Cancelado", "Eliminación cancelada")

    def limpiar_campos():
        nombre_entry.delete(0, tk.END)
        serie_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)

    def mostrar_inventario():
        inventario_window = tk.Toplevel(admin_window)
        inventario_window.title("Inventario")

        # --- Crear la tabla ---
        tree = ttk.Treeview(inventario_window, columns=("Nombre", "Serie", "Cantidad", "Precio"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Serie", text="Serie")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Precio", text="Precio")
        tree.pack()

        # --- Cargar datos desde la base de datos ---
        mycursor.execute("SELECT nombre, serie, cantidad, precio FROM productos")
        for row in mycursor:
            tree.insert("", tk.END, values=row)

        # --- Botón para volver al panel de administración ---
        tk.Button(inventario_window, text="Volver", command=inventario_window.destroy).pack()

    def editar_producto():
        nombre_a_editar = nombre_entry.get()
        if not nombre_a_editar:
            messagebox.showerror("Error", "Ingresa el nombre del producto a editar")
            return

        # --- Obtener datos actuales del producto ---
        sql = f"SELECT * FROM productos WHERE nombre = %s"
        val = (nombre_a_editar,)
        mycursor.execute(sql, val)
        producto = mycursor.fetchone()

        if producto:
            # --- Ventana de edición ---
            editar_window = tk.Toplevel(admin_window)
            editar_window.title(f"Editar: {nombre_a_editar}")
            editar_window.geometry("300x250")

            # --- Campos de entrada (prellenados con datos actuales) ---
            for i, label_text in enumerate(["Nombre:", "Serie:", "Cantidad:", "Precio:"]):
                tk.Label(editar_window, text=label_text).grid(row=i, column=0, padx=20, pady=10)
                entry = tk.Entry(editar_window)
                entry.insert(0, producto[i + 1])  # +1 para omitir el ID en la tupla
                entry.grid(row=i, column=1, padx=20, pady=10)

            # --- Función para guardar cambios ---
            def guardar_cambios(entries):
                nuevos_valores = [entry.get() for entry in entries]
                try:
                    nuevos_valores[2] = int(nuevos_valores[2])  # Cantidad debe ser entero
                    nuevos_valores[3] = float(nuevos_valores[3])  # Precio debe ser float
                except ValueError:
                    messagebox.showerror("Error", "Cantidad y precio deben ser números válidos")
                    return

                sql = f"UPDATE productos SET nombre=%s, serie=%s, cantidad=%s, precio=%s WHERE nombre=%s"
                val = (*nuevos_valores, nombre_a_editar) 
                mycursor.execute(sql, val)
                mydb.commit()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                editar_window.destroy()
                limpiar_campos()

            # --- Botón para guardar cambios ---
            tk.Button(editar_window, text="Guardar Cambios", command=lambda: guardar_cambios(editar_window.winfo_children()[1::2])).grid(row=4, column=0, columnspan=2, pady=10)  
        else:
            messagebox.showerror("Error", "Producto no encontrado")

    # --- Botones ---
    tk.Button(admin_window, text="Agregar producto", command=agregar_producto).grid(row=4, column=0, columnspan=2, pady=10)  # Botón de agregar productos
    tk.Button(admin_window, text="Buscar producto", command=buscar_producto).grid(row=5, column=0, columnspan=2, pady=5)  # Botón de buscar productos
    tk.Button(admin_window, text="Eliminar producto", command=eliminar_producto).grid(row=6, column=0, columnspan=2, pady=5)  # Botón de eliminar productos
    tk.Button(admin_window, text="Mostrar Inventario", command=mostrar_inventario).grid(row=7, column=0, columnspan=2, pady=5)  # Botón de mostrar inventario
    tk.Button(admin_window, text="Editar Producto", command=editar_producto).grid(row=8, column=0, columnspan=2, pady=5)  # Nuevo botón

def ventana_cliente():
    client_window = tk.Toplevel(root)
    client_window.title("Panel del Cliente")

    # --- Cargar productos y cantidades desde la base de datos ---
    mycursor.execute("SELECT nombre, serie, cantidad, precio FROM productos")
    productos = mycursor.fetchall()

    # --- Frame para el carrito ---
    carrito_frame = tk.LabelFrame(client_window, text="Carrito de compras")
    carrito_frame.pack(pady=10, padx=10)

    # --- Variables globales de la ventana del cliente ---
    carrito = {}
    total = 0

    # --- Funciones internas de ventana_cliente() ---
    def agregar_al_carrito(producto, serie, precio, cantidad_solicitada):
        nonlocal carrito, total  # Usar nonlocal para modificar variables externas

        # Validar stock
        mycursor.execute("SELECT cantidad FROM productos WHERE nombre = %s", (producto,))
        resultado = mycursor.fetchone()
        if resultado:
            cantidad_disponible = int(resultado[0])

            if producto in carrito:
                cantidad_en_carrito = carrito[producto]["cantidad"]
            else:
                cantidad_en_carrito = 0

            if cantidad_solicitada + cantidad_en_carrito > cantidad_disponible:
                messagebox.showerror("Error", f"No hay suficiente stock de {producto}. Disponibles: {cantidad_disponible}")
            elif cantidad_solicitada <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a cero")
            else:
                if producto in carrito:
                    carrito[producto]["cantidad"] += cantidad_solicitada
                else:
                    carrito[producto] = {"serie": serie, "precio": precio, "cantidad": cantidad_solicitada}
                total += precio * cantidad_solicitada
                actualizar_carrito()
        else:
            messagebox.showerror("Error", f"El producto {producto} no se encuentra en la base de datos.")

    def actualizar_carrito():
        # Limpiar la visualización anterior del carrito
        for widget in carrito_frame.winfo_children():
            widget.destroy()

        # Mostrar los productos en el carrito
        if carrito:
            tk.Label(carrito_frame, text="Carrito de compras:").pack()
            for producto, detalles in carrito.items():
                subtotal = detalles["precio"] * detalles["cantidad"]
                tk.Label(carrito_frame, text=f"{producto} (Serie: {detalles['serie']}) x {detalles['cantidad']} = ${subtotal:.2f}").pack()
            tk.Label(carrito_frame, text=f"Total a pagar: ${total:.2f}").pack()
        else:
            tk.Label(carrito_frame, text="Tu carrito está vacío").pack()

    def finalizar_compra():
        if not carrito:
            messagebox.showinfo("Carrito vacío", "No tienes productos en el carrito")
            return

        resumen_window = tk.Toplevel(client_window)
        resumen_window.title("Factura de la compra")
        resumen_window.geometry("300x200")

        total = 0
        for producto, detalles in carrito.items():
            subtotal = detalles["precio"] * detalles["cantidad"]
            total += subtotal
            tk.Label(resumen_window, text=f"{producto} (Serie: {detalles['serie']}) x {detalles['cantidad']} = ${subtotal:.2f}").pack()

        tk.Label(resumen_window, text=f"Total a pagar: ${total:.2f}").pack(pady=10)

        def confirmar_compra():
            # Confirmar la compra con el usuario (puedes agregar aquí una interfaz de pago, etc.)
            confirmacion = messagebox.askyesno("Confirmar compra", "¿Estás seguro de que deseas confirmar la compra?")
            if not confirmacion:
                return  # Si el usuario cancela, no hacer nada

            # Actualizar el inventario en la base de datos
            for producto, detalles in carrito.items():
                cantidad_comprada = detalles["cantidad"]
                sql = "UPDATE productos SET cantidad = cantidad - %s WHERE nombre = %s"
                val = (cantidad_comprada, producto)
                mycursor.execute(sql, val)

            mydb.commit()  # Guardar los cambios en la base de datos

            # Mostrar mensaje de éxito y cerrar ventanas
            messagebox.showinfo("Compra realizada", "¡Gracias por tu compra!")
            resumen_window.destroy()
            client_window.destroy()  

        def cancelar_compra():
            messagebox.showinfo("Compra cancelada", "La compra ha sido cancelada.")
            resumen_window.destroy()
            ventana_cliente()  # Volver a la ventana de productos

        tk.Button(resumen_window, text="Confirmar compra", command=confirmar_compra).pack()
        tk.Button(resumen_window, text="Cancelar compra", command=cancelar_compra).pack()

    # --- Creación de la interfaz de ventana_cliente() ---
    for producto, serie, cantidad, precio in productos:
        producto_frame = tk.Frame(client_window)
        producto_frame.pack(pady=5)

        tk.Label(producto_frame, text=f"{producto} - ${precio:.2f} (Serie: {serie}, Stock: {cantidad})").pack(side=tk.LEFT)

        cantidad_var = tk.IntVar(value=1)
        cantidad_entry = tk.Entry(producto_frame, textvariable=cantidad_var, width=5)

        # Validación de entrada para la cantidad
        def validate_cantidad(new_value):
            try:
                value = int(new_value)
                return 0 <= value <= cantidad_var.get()
            except ValueError:
                return False
        
        validate_cmd = cantidad_entry.register(validate_cantidad)
        cantidad_entry.config(validate="key", validatecommand=(validate_cmd, '%P'))

        # --- Función para agregar el producto actual al carrito (corregida) ---
        def agregar_este_producto(p=producto, s=serie, pr=precio, c=cantidad):
            def _agregar():
                try:
                    cantidad_solicitada = int(cantidad_var.get())
                    if cantidad_solicitada > 0:  # Solo agregar si la cantidad es positiva
                        agregar_al_carrito(p, s, pr, cantidad_solicitada)
                        cantidad_var.set(1)  # Restablecer la cantidad en el Entry a 1
                except ValueError:
                    messagebox.showerror("Error", "Ingrese una cantidad válida (número entero).")

            return _agregar

        tk.Button(producto_frame, text="Agregar al carrito", command=agregar_este_producto(c=cantidad)).pack(side=tk.LEFT)
    tk.Button(client_window, text="Finalizar compra", command=finalizar_compra).pack()

    actualizar_carrito()

# --- Botones de inicio de sesión ---
tk.Button(root, text="Administrador", command=login).pack(pady=20)

root.mainloop()