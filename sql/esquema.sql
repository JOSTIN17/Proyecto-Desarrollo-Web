CREATE DATABASE IF NOT EXISTS ferreteria;

USE ferreteria;

-- ==========================================
-- TABLA: usuarios
-- ==========================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


-- ==========================================
-- TABLA: proveedores
-- ==========================================

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);


-- ==========================================
-- TABLA: productos
-- ==========================================

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,

    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);


-- ==========================================
-- TABLA: clientes
-- ==========================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);


-- ==========================================
-- TABLA: facturas
-- ==========================================

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);

-- ==========================================
-- DATOS INICIALES DE PROVEEDORES
-- ==========================================

INSERT INTO proveedores (nombre, telefono, correo)
SELECT 'Tecnología Digital S.A.', '0991111111', 'contacto@tecnologiadigital.com'
WHERE NOT EXISTS (
    SELECT 1
    FROM proveedores
    WHERE nombre = 'Tecnología Digital S.A.'
);


INSERT INTO proveedores (nombre, telefono, correo)
SELECT 'Servicios Web Ecuador', '0992222222', 'info@serviciosweb.com'
WHERE NOT EXISTS (
    SELECT 1
    FROM proveedores
    WHERE nombre = 'Servicios Web Ecuador'
);


INSERT INTO proveedores (nombre, telefono, correo)
SELECT 'Diseño Creativo', '0993333333', 'contacto@disenocreativo.com'
WHERE NOT EXISTS (
    SELECT 1
    FROM proveedores
    WHERE nombre = 'Diseño Creativo'
);


INSERT INTO proveedores (nombre, telefono, correo)
SELECT 'Soluciones Informáticas', '0994444444', 'soporte@soluciones.com'
WHERE NOT EXISTS (
    SELECT 1
    FROM proveedores
    WHERE nombre = 'Soluciones Informáticas'
);
