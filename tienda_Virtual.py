" El  módulo datetime nos  permite trabajar con fechas y horas"
from datetime import date 
"El  módulo tkinter nos  permite crear ventanas y aplicaciones gráficas"
import tkinter as tk
"EL modulo ttk nos permite crear widgets con estilo moderno y messagebox para mostrar mensajes"
from tkinter import ttk, messagebox

# Clase Padre: Producto
class Producto:
    def __init__(self, name, price, stock, base_discount=0):
        self.nombre = name
        self.precio = price
        self.stock = stock
        self.descuento_base = base_discount

    def descripcion(self):
        return (
            f"Product: {self.nombre} | Price: ${self.precio:,.2f} | "
            f"Stock: {self.stock}"
        )

    def calcular_descuento(self, porcentaje, cupon=0, cliente_premium=False):
        
        porcentaje_total = porcentaje + cupon
        if cliente_premium:
            porcentaje_total += 5
        porcentaje_total = min(max(porcentaje_total, 0), 100)
        return self.precio * porcentaje_total / 100

    def calcular_precio_final(self):
        return self.precio - self.calcular_descuento(self.descuento_base)

# Clase Hija: ProductoElectronico
class ProductoElectronico(Producto):
    def __init__(self, name, price, stock, antiquity_years=0, base_discount=0):
        super().__init__(name, price, stock, base_discount)
        self.antiguedad_anos = antiquity_years

    def descripcion(self):
        return (
            f"[Electronics] {self.nombre} | Precio: ${self.precio:,.2f} | "
            f"Antique: {self.antiguedad_anos} año(s) | Stock: {self.stock}"
        )

    def calcular_descuento(self, porcentaje, cupon=0, cliente_premium=False):
        # Electrónicos: depreciación del 2 % por año; descuento máximo del 30 %.
        total = porcentaje + self.antiguedad_anos * 2 + cupon
        if cliente_premium:
            total += 5
        total = min(max(total, 0), 30)
        return self.precio * total / 100

# Clase Hija: ProductoAlimento
class ProductoAlimento(Producto):
    def __init__(self, name, price, stock, expiration_date, base_discount=0):
        super().__init__(name, price, stock, base_discount)
        self.fecha_vencimiento = expiration_date

    def descripcion(self):
        return (
            f"[Food] {self.nombre} | Precio: ${self.precio:,.2f} | "
            f"Expiration Date: {self.fecha_vencimiento} | Stock: {self.stock}"
        )

    def calcular_descuento(self, porcentaje, cupon=0, cliente_premium=False):
        # Alimentos: el descuento acumulado no puede superar el 10 %.
        total = porcentaje + cupon + (5 if cliente_premium else 0)
        total = min(max(total, 0), 10)
        return self.precio * total / 100

# Clase Hija: ProductoRopa
class ProductoRopa(Producto):
    def __init__(self, name, price, stock, size, base_discount=0):
        # Llamada al constructor de la clase padre
        super().__init__(name, price, stock, base_discount)
        self.talla = size

    def descripcion(self):
        return (
            f"[Clothing] {self.nombre} | Precio: ${self.precio:,.2f} | "
            f"Size: {self.talla} | Stock: {self.stock}"
        )

    def calcular_descuento(self, porcentaje, cupon=0, cliente_premium=False):
        # Ropa: los descuentos se acumulan, con un límite del 40 %.
        total = porcentaje + cupon + (5 if cliente_premium else 0)
        total = min(max(total, 0), 40)
        return self.precio * total / 100

#Clase carrito de compras
class CarritoDeCompras:
    def __init__(self):
        # Cada elemento guarda (producto, cantidad).
        self.productos = []

    def agregar_producto(self, producto, cantidad=1):
        if not isinstance(producto, Producto):
            raise TypeError("Only Product type objects can be added.")
        if cantidad <= 0:
            raise ValueError("The quantity must be greater than zero.")
        if cantidad > producto.stock:
            raise ValueError(
                f"Insufficient stock for {producto.nombre}. "
                f"Available: {producto.stock}"
            )

        # Si ya está en el carrito, aumentamos la cantidad.
        for indice, (producto_carrito, cantidad_actual) in enumerate(self.productos):
            if producto_carrito is producto:
                self.productos[indice] = (producto, cantidad_actual + cantidad)
                producto.stock -= cantidad
                return

        self.productos.append((producto, cantidad))
        producto.stock -= cantidad

    def quitar_producto(self, indice):
        producto, cantidad = self.productos.pop(indice)
        producto.stock += cantidad

    def calcular_total(self):
        return sum(
            producto.calcular_precio_final() * cantidad
            for producto, cantidad in self.productos
        )

# Configuración de la pantalla

class TiendaApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Online Store - Product and Purchasing System")
        self.ventana.state("zoomed")  # Inicia la ventana maximizada
        self.ventana.minsize(1050, 760) #Aqui bloqueamos para que la ventana no se pueda redimensionar

        self.ventana.configure(bg="#F4F6F8")

        self.productos = []
        self.carrito = CarritoDeCompras()
        self.campos_extra = {}

        
        self.crear_interfaz()
        self.actualizar_listas()

    def configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TLabel", font=("Arial", 10))
        estilo.configure("TButton", font=("Arial", 10, "bold"), padding=7)
        estilo.configure("TCombobox", padding=5)
        estilo.configure("Treeview", rowheight=27, font=("Arial", 9))
        estilo.configure("Treeview.Heading", font=("Arial", 9, "bold"))

    def crear_interfaz(self):
        encabezado = tk.Frame(self.ventana, bg="#F28C28", height=5)
        encabezado.pack(fill="x")
        tk.Label(
            encabezado,
            text="PRODUCTS AND PURCHASES",
            bg="#F28C28",
            fg="white",
            font=("Arial", 19, "bold"),
        ).pack(pady=10)

        principal = ttk.Frame(self.ventana, padding=12)
        principal.pack(fill="both", expand=True)

        #Botones de registro de productos
        registro = ttk.LabelFrame(principal, text=" Register product ", padding=10)
        registro.pack(fill="x", pady=(0, 10))

        ttk.Label(registro, text="Product Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tipo_var = tk.StringVar(value=" Select Products   ")
        self.combo_tipo = ttk.Combobox(
            registro, textvariable=self.tipo_var,
            values=["Electronics", "Food", "Clothing"],
            state="readonly", width=22
        )
        self.combo_tipo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_campos_extra)

        ttk.Label(registro, text="Name:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(registro, textvariable=self.nombre_var, width=25).grid(
            row=0, column=3, sticky="ew", padx=5, pady=5
        )

        ttk.Label(registro, text="Price ($):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.precio_var = tk.StringVar()
        ttk.Entry(registro, textvariable=self.precio_var, width=25).grid(
            row=1, column=1, sticky="ew", padx=5, pady=5
        )

        ttk.Label(registro, text="Initial Stock:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.stock_var = tk.StringVar()
        ttk.Entry(registro, textvariable=self.stock_var, width=25).grid(
            row=1, column=3, sticky="ew", padx=5, pady=5
        )

        ttk.Label(registro, text="Base Discount (%):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.descuento_var = tk.StringVar(value="0")
        ttk.Entry(registro, textvariable=self.descuento_var, width=25).grid(
            row=2, column=1, sticky="ew", padx=5, pady=5
        )

        self.extra_frame = ttk.Frame(registro)
        self.extra_frame.grid(row=2, column=2, columnspan=2, sticky="ew", padx=5, pady=5)
        for columna in range(4):
            registro.columnconfigure(columna, weight=1)

        ttk.Button(registro, text="Register product", command=self.registrar_producto).grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(8, 3)
        )
        ttk.Button(registro, text="Clear fields", command=self.limpiar_formulario).grid(
            row=3, column=2, columnspan=2, sticky="ew", padx=5, pady=(8, 3)
        )
        self.actualizar_campos_extra()

        # Inventario
        inventario = ttk.LabelFrame(principal, text=" Inventory", padding=8)
        inventario.pack(fill="both", expand=True, pady=(0, 10))

        columnas = ("type", "name", "price", "stock", "detail", "final_price")
        self.tabla_inventario = ttk.Treeview(
            inventario, columns=columnas, show="headings", height=4
        )
        encabezados = {
            "type": "Type", "name": "Name", "price": "Price",
            "stock": "Stock", "detail": "Description", "final_price": "Final Price"
        }
        anchos = {"type": 110, "name": 180, "price": 105, "stock": 65, "detail": 180, "final_price": 115}
        for columna in columnas:
            self.tabla_inventario.heading(columna, text=encabezados[columna])
            self.tabla_inventario.column(columna, width=anchos[columna], anchor="center")
        self.tabla_inventario.pack(fill="both", expand=True)

        # Panel del carrito
        zona_carrito = ttk.LabelFrame(principal, text=" Shopping Cart ", padding=5)
        zona_carrito.pack(fill="both", expand=True)

        fila = ttk.Frame(zona_carrito)
        fila.pack(fill="x", pady=(0, 8))
        ttk.Label(fila, text="Producto:").pack(side="left", padx=(0, 5))
        self.producto_carrito_var = tk.StringVar()
        self.combo_productos = ttk.Combobox(
            fila, textvariable=self.producto_carrito_var, state="readonly", width=38
        )
        self.combo_productos.pack(side="left", padx=(0, 12))

        ttk.Label(fila, text="Cantidad:").pack(side="left", padx=(0, 5))
        self.cantidad_var = tk.StringVar(value="1")
        self.combo_cantidad = ttk.Combobox(
            fila, textvariable=self.cantidad_var, state="readonly", width=7,
            values=[str(i) for i in range(1, 101)]
        )
        self.combo_cantidad.pack(side="left", padx=(0, 12))
        ttk.Button(fila, text="Add to cart", command=self.agregar_al_carrito).pack(side="left")

        columnas_carrito = ("name", "quantity", "unit", "subtotal")
        self.tabla_carrito = ttk.Treeview(
            zona_carrito, columns=columnas_carrito, show="headings", height=4
        )
        for col, titulo, ancho in [
            ("name", "Product", 350),
            ("quantity", "Quantity", 100),
            ("unit", "Final Unit Price", 180),
            ("subtotal", "Subtotal", 180),
        ]:
            self.tabla_carrito.heading(col, text=titulo)
            self.tabla_carrito.column(col, width=ancho, anchor="center")
        self.tabla_carrito.pack(fill="both", expand=True)

      
        # Parte inferior del carrito
        pie = ttk.Frame(zona_carrito)
        pie.pack(fill="x", pady=(8, 5))

        ttk.Button(
            pie,
            text="Remove selected product",
            command=self.quitar_del_carrito
        ).pack(side="left")

        ttk.Button(
            pie,
            text="Finalize purchase",
            command=self.finalizar_compra
        ).pack(side="left", padx=8)

        # Total del carrito
        self.total_var = tk.StringVar(
            value="GRAND TOTAL: $0.00"
        )

        tk.Label(
            pie,
            textvariable=self.total_var,
            fg="white",
            bg="#1976D2",
            font=("Arial", 15, "bold"),
            padx=12,
            pady=6
        ).pack(side="right", padx=8)


        self.estado_var = tk.StringVar(value="Register a product to get started.")
        tk.Label(
            self.ventana, textvariable=self.estado_var, anchor="w",
            bg="#E8EDF2", fg="#444444", padx=12, pady=7
        ).pack(fill="x", side="bottom")

    def actualizar_campos_extra(self, event=None):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()
        self.campos_extra.clear()

        tipo = self.tipo_var.get()
        if tipo == "Electronics":
            etiqueta, clave, valor = "Antique (años):", "Antique", "0"
        elif tipo == "Food":
            etiqueta, clave, valor = "Maturity (AAAA-MM-DD):", "Maturity", ""
        else:
            etiqueta, clave, valor = "Size", "talla", "M"

        ttk.Label(self.extra_frame, text=etiqueta).grid(row=0, column=0, sticky="w", padx=3)
        variable = tk.StringVar(value=valor)
        if clave == "talla":
            widget = ttk.Combobox(
                self.extra_frame, textvariable=variable,
                values=["XS", "S", "M", "L", "XL", "XXL"], state="readonly", width=12
            )
        else:
            widget = ttk.Entry(self.extra_frame, textvariable=variable, width=16)
        widget.grid(row=0, column=1, sticky="ew", padx=3)
        self.campos_extra[clave] = variable

    def registrar_producto(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showerror("Required information", "Write the product name.")
            return

        try:
            precio = float(self.precio_var.get().replace(",", "").strip())
            stock = int(self.stock_var.get().strip())
            descuento = float(self.descuento_var.get().strip())
            if precio < 0 or stock < 0 or not 0 <= descuento <= 100:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid data",
                "Price and stock must be valid non-negative numbers. "
                "The discount must be between 0 and 100."
            )
            return

        tipo = self.tipo_var.get()
        try:
            if tipo == "Electronics":
                antiguedad = int(self.campos_extra["Antique"].get().strip())
                if antiguedad < 0:
                    raise ValueError
                producto = ProductoElectronico(nombre, precio, stock, antiguedad, descuento)
            elif tipo == "Food":
                vencimiento = self.campos_extra["Maturity"].get().strip()
                date.fromisoformat(vencimiento)
                producto = ProductoAlimento(nombre, precio, stock, vencimiento, descuento)
            else:
                talla = self.campos_extra["talla"].get().strip()
                if not talla:
                    raise ValueError
                producto = ProductoRopa(nombre, precio, stock, talla, descuento)
        except ValueError:
            mensaje = (
                "The age must be a non-negative integer."
                if tipo == "Electronics"
                else "The date must exist and be in the correct format. AAAA-MM-DD."
                if tipo == "Food"
                else "Select a suitable size."
            )
            messagebox.showerror("Invalid additional information", mensaje)
            return

        self.productos.append(producto)
        self.actualizar_listas()
        self.limpiar_formulario()
        self.estado_var.set(f"Product «{nombre}» registered successfully.")

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")
        self.descuento_var.set("0")
        self.actualizar_campos_extra()

    def actualizar_listas(self):
        for elemento in self.tabla_inventario.get_children():
            self.tabla_inventario.delete(elemento)

        for indice, producto in enumerate(self.productos):
            # POLIMORFISMO: cada clase hija entrega su propia descripcion().
            if isinstance(producto, ProductoElectronico):
                tipo = "Electronics"
            elif isinstance(producto, ProductoAlimento):
                tipo = "Food"
            else:
                tipo = "Clothing"

            self.tabla_inventario.insert(
                "", "end", iid=str(indice),
                values=(
                    tipo, producto.nombre, f"${producto.precio:,.2f}",
                    producto.stock, producto.descripcion(),
                    f"${producto.calcular_precio_final():,.2f}"
                )
            )

        valores = [
            f"{i} - {p.nombre} (stock: {p.stock})"
            for i, p in enumerate(self.productos) if p.stock > 0
        ]
        self.combo_productos["values"] = valores
        if self.producto_carrito_var.get() not in valores:
            self.producto_carrito_var.set(valores[0] if valores else "")
        self.actualizar_tabla_carrito()

    def agregar_al_carrito(self):
        seleccion = self.producto_carrito_var.get()
        if not seleccion:
            messagebox.showwarning("Select a product", "Register and select a product with available stock.")
            return

        try:
            indice = int(seleccion.split(" - ", 1)[0])
            cantidad = int(self.cantidad_var.get())
            producto = self.productos[indice]
            self.carrito.agregar_producto(producto, cantidad)
        except (ValueError, IndexError) as error:
            messagebox.showerror("Could not add product", str(error) or "Select a valid quantity.")
            return

        self.actualizar_listas()
        self.estado_var.set(f"Added {cantidad} unit(s) of «{producto.nombre}» to the cart.")

    def actualizar_tabla_carrito(self):
        for elemento in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(elemento)

        for indice, (producto, cantidad) in enumerate(self.carrito.productos):
            unitario = producto.calcular_precio_final()
            self.tabla_carrito.insert(
                "", "end", iid=str(indice),
                values=(
                    producto.nombre, cantidad, f"${unitario:,.2f}",
                    f"${unitario * cantidad:,.2f}"
                )
            )
        self.total_var.set(f"Total: ${self.carrito.calcular_total():,.2f}")

    def quitar_del_carrito(self):
        seleccion = self.tabla_carrito.selection()
        if not seleccion:
            messagebox.showinfo("Select a product", "Select a row from the cart to remove it.")
            return
        indice = int(seleccion[0])
        producto, _ = self.carrito.productos[indice]
        self.carrito.quitar_producto(indice)
        self.actualizar_listas()
        self.estado_var.set(f"Product «{producto.nombre}» returned to inventory." )

    def finalizar_compra(self):
        if not self.carrito.productos:
            messagebox.showwarning("Cart is empty", "Add at least one product before finalizing.")
            return

        lineas = []
        for producto, cantidad in self.carrito.productos:
            subtotal = producto.calcular_precio_final() * cantidad
            lineas.append(f"{producto.nombre} x {cantidad}: ${subtotal:,.2f}")
        total = self.carrito.calcular_total()
        mensaje = "\n".join(lineas) + f"\n\nTOTAL TO PAY: ${total:,.2f}"

        if messagebox.askyesno("Purchase summary", mensaje + "\n\n¿Confirm the purchase?"):
            nombres = ", ".join(p.nombre for p, _ in self.carrito.productos)
            self.carrito.productos.clear()
            self.actualizar_listas()
            self.estado_var.set(f"Purchase completed. Total paid: ${total:,.2f}.")
            messagebox.showinfo("Purchase completed", f"Purchase registered successfully.\nProducts: {nombres}\nTotal: ${total:,.2f}")


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = TiendaApp(ventana)
    ventana.mainloop()
