from flask import Flask, render_template, request
import sqlite3
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# Configuración de Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"
# ==================================================
# CONFIGURACIÓN DE SQLITE
# ==================================================

DATABASE = "data/ferreteria.db"


def conectar_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_db():
    conn = conectar_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    
# ==================================================
# DATOS DE EJEMPLO DEL PROYECTO
# ==================================================

nombre_proyecto = "Desarrollo Web"

informacion_proyecto = {
    "curso": "Desarrollo de Aplicaciones Web",
    "anio": 2026,
    "estado": "En desarrollo"
}

clientes_lista = [
    {
        "id": "001",
        "nombre": "Ana López",
        "correo": "ana@example.com",
        "estado": "Activo"
    },
    {
        "id": "002",
        "nombre": "Carlos Pérez",
        "correo": "carlos@example.com",
        "estado": "Activo"
    },
    {
        "id": "003",
        "nombre": "María González",
        "correo": "maria@example.com",
        "estado": "Inactivo"
    }
]


proveedores_lista = [
    {
        "id": "001",
        "empresa": "Tecnología Digital S.A.",
        "servicio": "Equipos tecnológicos",
        "contacto": "contacto@tecnologiadigital.com",
        "estado": "Activo"
    },
    {
        "id": "002",
        "empresa": "Servicios Web Ecuador",
        "servicio": "Servicios de hosting",
        "contacto": "info@serviciosweb.com",
        "estado": "Activo"
    },
    {
        "id": "003",
        "empresa": "Diseño Creativo",
        "servicio": "Recursos gráficos",
        "contacto": "contacto@disenocreativo.com",
        "estado": "Inactivo"
    },
    {
        "id": "004",
        "empresa": "Soluciones Informáticas",
        "servicio": "Soporte tecnológico",
        "contacto": "soporte@soluciones.com",
        "estado": "Activo"
    }
]


facturas_lista = [
    {
        "numero": "FAC-001",
        "cliente": "Ana López",
        "servicio": "Diseño Web",
        "fecha": "10/08/2026",
        "total": 150.00,
        "estado": "Pagada"
    },
    {
        "numero": "FAC-002",
        "cliente": "Carlos Pérez",
        "servicio": "Desarrollo Web",
        "fecha": "12/08/2026",
        "total": 300.00,
        "estado": "Pendiente"
    },
    {
        "numero": "FAC-003",
        "cliente": "María González",
        "servicio": "Diseño Responsivo",
        "fecha": "14/08/2026",
        "total": 200.00,
        "estado": "Pagada"
    }
]


# ==================================================
# RUTAS DE LA APLICACIÓN
# ==================================================

# Ruta principal
@app.route("/")
def index():
    return render_template(
        "index.html",
        nombre_proyecto=nombre_proyecto,
        informacion=informacion_proyecto
    )


# Ruta de productos
@app.route("/productos")
def productos():
    conn = conectar_db()

    productos = conn.execute("""
        SELECT id, nombre, descripcion, categoria, precio, stock
        FROM productos
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )
    
# Formulario de productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()

    if form.validate_on_submit():
        conn = conectar_db()

        conn.execute("""
            INSERT INTO productos (
                nombre,
                descripcion,
                categoria,
                precio,
                stock
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.categoria.data,
            0.00,
            0
        ))

        conn.commit()

        productos = conn.execute("""
            SELECT id, nombre, descripcion, categoria, precio, stock
            FROM productos
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        return render_template(
            "productos.html",
            productos=productos,
            mensaje="Producto registrado correctamente."
        )

    return render_template(
        "formulario_producto.html",
        form=form
    )
    
# Ruta de clientes
@app.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )
# Formulario de clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    form = ClienteForm()

    if form.validate_on_submit():
        nuevo = {
            "id": str(len(clientes_lista) + 1).zfill(3),
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "estado": "Activo"
        }

        clientes_lista.append(nuevo)

        return render_template(
            "clientes.html",
            clientes=clientes_lista,
            mensaje="Cliente registrado correctamente."
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# Ruta de proveedores
@app.route("/proveedores")
def proveedores():
    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )
# Formulario de proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    form = ProveedorForm()

    if form.validate_on_submit():
        nuevo = {
            "id": str(len(proveedores_lista) + 1).zfill(3),
            "empresa": form.empresa.data,
            "servicio": "Servicio general",
            "contacto": form.correo.data,
            "estado": "Activo"
        }

        proveedores_lista.append(nuevo)

        return render_template(
            "proveedores.html",
            proveedores=proveedores_lista,
            mensaje="Proveedor registrado correctamente."
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

# Ruta de facturación
@app.route("/facturacion")
def facturacion():
    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )
    
# Formulario de facturación
@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():
    form = FacturacionForm()

    if form.validate_on_submit():
        nueva = {
            "numero": form.numero_factura.data,
            "cliente": form.cliente.data,
            "servicio": "Servicio general",
            "fecha": "06/09/2026",
            "total": form.total.data,
            "estado": "Pendiente"
        }

        facturas_lista.append(nueva)

        return render_template(
            "facturacion.html",
            facturas=facturas_lista,
            mensaje="Factura registrada correctamente."
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )

# ==================================================
# EJECUCIÓN DE LA APLICACIÓN
# ==================================================

if __name__ == "__main__":
    inicializar_db()
    app.run(debug=True)
