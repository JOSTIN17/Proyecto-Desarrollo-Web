from flask import Flask, render_template

app = Flask(__name__)


# ==================================================
# DATOS DE EJEMPLO DEL PROYECTO
# ==================================================

nombre_proyecto = "Desarrollo Web"

informacion_proyecto = {
    "curso": "Desarrollo de Aplicaciones Web",
    "anio": 2026,
    "estado": "En desarrollo"
}


productos_lista = [
    {
        "nombre": "Diseño Web",
        "descripcion": "Creación de páginas web modernas y atractivas.",
        "precio": 150.00,
        "stock": 5
    },
    {
        "nombre": "Desarrollo Web",
        "descripcion": "Implementación de aplicaciones web dinámicas.",
        "precio": 300.00,
        "stock": 3
    },
    {
        "nombre": "Diseño Responsivo",
        "descripcion": "Adaptación de sitios web para dispositivos móviles.",
        "precio": 200.00,
        "stock": 0
    }
]


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
    return render_template(
        "productos.html",
        productos=productos_lista
    )


# Ruta de clientes
@app.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


# Ruta de proveedores
@app.route("/proveedores")
def proveedores():
    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


# Ruta de facturación
@app.route("/facturacion")
def facturacion():
    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


# ==================================================
# EJECUCIÓN DE LA APLICACIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)
