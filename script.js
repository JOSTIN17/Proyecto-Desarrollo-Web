const formulario = document.getElementById("formRegistro");
const lista = document.getElementById("listaRegistros");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

let total = 0;
let servicios = [];

function mostrarServicios(){

    lista.innerHTML = "";

    servicios.forEach(function(servicio){

        const tarjeta = document.createElement("div");

        tarjeta.className = "card shadow p-3 mt-3";

        tarjeta.innerHTML = `
            <h5>${servicio.nombre}</h5>
            <p>${servicio.descripcion}</p>
            <span class="badge bg-primary">${servicio.categoria}</span>

            <br><br>

            <button class="btn btn-danger eliminar">
                Eliminar
            </button>
        `;

        lista.appendChild(tarjeta);

        tarjeta.querySelector(".eliminar").addEventListener("click", function(){

            const posicion = servicios.indexOf(servicio);

            servicios.splice(posicion, 1);

            total--;

            contador.textContent = total;

            mostrarServicios();

        });

    });

}
function validarNombre() {

    if (nombre.value.trim().length < 3) {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");
        errorNombre.textContent = "El nombre debe tener al menos 3 caracteres.";
        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");
    errorNombre.textContent = "";
    return true;
}

function validarDescripcion() {

    if (descripcion.value.trim().length < 10) {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");
        errorDescripcion.textContent = "La descripción debe tener al menos 10 caracteres.";
        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");
    errorDescripcion.textContent = "";
    return true;
}

function validarCategoria() {

    if (categoria.value === "") {

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");
        errorCategoria.textContent = "Seleccione una categoría.";
        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");
    errorCategoria.textContent = "";
    return true;
}

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if(!(nombreValido && descripcionValida && categoriaValida)){

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Corrija los errores antes de registrar.
        </div>
        `;
        return;
    }

    mensaje.innerHTML = `
    <div class="alert alert-success">
        Registro agregado correctamente.
    </div>
    `;
const servicio = {
    nombre: nombre.value,
    descripcion: descripcion.value,
    categoria: categoria.value
};

servicios.push(servicio);

    mostrarServicios();

    total++;
    contador.textContent = total;

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

});
