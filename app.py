from flask import Flask, render_template, request, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import obtener_conexion

app = Flask(__name__)

# Configuración de Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"


# ==================================================
# DATOS GENERALES DEL PROYECTO
# ==================================================

nombre_proyecto = "Desarrollo Web"

informacion_proyecto = {
    "curso": "Desarrollo de Aplicaciones Web",
    "anio": 2026,
    "estado": "En desarrollo"
}


# ==================================================
# DATOS TEMPORALES DE CLIENTES
# ==================================================

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


# ==================================================
# DATOS TEMPORALES DE PROVEEDORES
# ==================================================

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


# ==================================================
# DATOS TEMPORALES DE FACTURACIÓN
# ==================================================

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
# RUTA PRINCIPAL
# ==================================================

@app.route("/")
def index():
    return render_template(
        "index.html",
        nombre_proyecto=nombre_proyecto,
        informacion=informacion_proyecto
    )


# ==================================================
# PRODUCTOS - LISTAR
# SELECT + JOIN
# ==================================================

@app.route("/productos")
def productos():

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.categoria,
            p.precio,
            p.stock,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==================================================
# PRODUCTOS - AGREGAR
# INSERT
# ==================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (
                nombre,
                descripcion,
                categoria,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.categoria.data,
            0.00,
            0,
            None
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==================================================
# PRODUCTOS - MODIFICAR
# UPDATE
# ==================================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            descripcion,
            categoria,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id,))

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:
        return redirect(url_for("productos"))

    form = ProductoForm()

    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.categoria.data = producto["categoria"]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                categoria = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.categoria.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=True,
        producto=producto
    )


# ==================================================
# PRODUCTOS - ELIMINAR
# DELETE
# ==================================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("productos"))


# ==================================================
# CLIENTES
# ==================================================

@app.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


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


# ==================================================
# PROVEEDORES
# ==================================================

@app.route("/proveedores")
def proveedores():
    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


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


# ==================================================
# FACTURACIÓN
# ==================================================

@app.route("/facturacion")
def facturacion():
    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


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
    app.run(debug=True)
