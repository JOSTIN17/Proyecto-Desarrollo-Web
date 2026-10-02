from flask import Flask, render_template, request, redirect, url_for, flash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from models import Usuario
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion.conexion import obtener_conexion


app = Flask(__name__)


# ==================================================
# CONFIGURACIÓN DE FLASK-WTF Y PROTECCIÓN CSRF
# ==================================================

app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"

# ==================================================
# CONFIGURACIÓN DE FLASK-LOGIN
# ==================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."

# ==================================================
# CARGAR USUARIO PARA FLASK-LOGIN
# ==================================================

@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, usuario FROM usuarios WHERE id = %s",
        (user_id,)
    )

    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila:
        return Usuario(
            fila["id"],
            fila["usuario"]
        )

    return None
    
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
# REGISTRO DE USUARIOS
# ==================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash("El usuario ya existe.", "danger")

            cursor.close()
            conexion.close()

            return render_template(
                "registro.html",
                form=form
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
            """,
            (
                form.usuario.data,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )
    
# ==================================================
# INICIO DE SESIÓN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario_db = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario_db and check_password_hash(
            usuario_db["password"],
            form.password.data
        ):

            usuario = Usuario(
                usuario_db["id"],
                usuario_db["usuario"]
            )

            login_user(usuario)

            return redirect(url_for("dashboard"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )

# ==================================================
# CERRAR SESIÓN
# ==================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))

# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        usuario=current_user
    )
    
# ==================================================
# OBTENER PROVEEDORES DESDE MYSQL
# ==================================================

def obtener_proveedores():

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return proveedores
def obtener_clientes():

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_cliente,
            nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return clientes

# ==================================================
# CONFIGURAR PROVEEDORES EN EL FORMULARIO
# ==================================================

def configurar_proveedores(form):

    proveedores = obtener_proveedores()

    form.proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]
    
def configurar_clientes(form):

    clientes = obtener_clientes()

    form.cliente.choices = [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

# ==================================================
# PRODUCTOS - LISTAR
# SELECT + JOIN
# ==================================================

@app.route("/productos")
@login_required
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
@login_required
def nuevo_producto():

    form = ProductoForm()

    configurar_proveedores(form)

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
            form.precio.data,
            form.stock.data,
            form.proveedor.data
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
@login_required
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

    configurar_proveedores(form)

    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.proveedor.data = producto["id_proveedor"]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.proveedor.data,
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
@login_required
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
@login_required
def clientes():

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )
    

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# ==================================================
# PROVEEDORES
# ==================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

# ==================================================
# FACTURACIÓN
# ==================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero_factura,
            c.nombre AS cliente,
            f.fecha,
            f.total
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura DESC
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )

@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    configurar_clientes(form)

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas (
                numero_factura,
                id_cliente,
                fecha,
                total
            )
            VALUES (%s, %s, CURDATE(), %s)
        """, (
            form.numero_factura.data,
            form.cliente.data,
            form.total.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==================================================
# EJECUCIÓN DE LA APLICACIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)
