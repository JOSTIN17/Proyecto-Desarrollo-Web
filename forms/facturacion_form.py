from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):
    numero_factura = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio."),
            Length(min=3, max=20, message="El número de factura debe tener entre 3 y 20 caracteres.")
        ]
    )

    cliente = SelectField(
    "Cliente",
    coerce=int,
    choices=[],
    validators=[
        DataRequired(message="Seleccione un cliente.")
    ]
)

    total = FloatField(
        "Total",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(min=0.01, message="El total debe ser mayor que 0.")
        ]
    )

    submit = SubmitField("Guardar factura")
