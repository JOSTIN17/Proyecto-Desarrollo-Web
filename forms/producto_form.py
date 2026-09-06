from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(min=10, max=500, message="La descripción debe tener entre 10 y 500 caracteres.")
        ]
    )

    categoria = StringField(
        "Categoría",
        validators=[
            DataRequired(message="La categoría es obligatoria."),
            Length(min=3, max=50, message="La categoría debe tener entre 3 y 50 caracteres.")
        ]
    )

    submit = SubmitField("Guardar producto")
