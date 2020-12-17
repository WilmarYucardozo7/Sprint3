import os
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Email,Length,Regexp

class IniciosesionForm(FlaskForm):
    usuario=StringField('Usuario')
    contraseña=PasswordField('Contraseña')
    submit=SubmitField('Iniciar sesion')

class OlvidarForm(FlaskForm):
    correo=StringField('Correo',validators=[InputRequired()])
    submit=SubmitField('Recuperar')

class NuevaContraseña(FlaskForm):
    contraseña= PasswordField('Contraseña', validators=[InputRequired()])
    submit=SubmitField('Cambiar contraseña')

class RegistrarForm(FlaskForm):
    enviar=SubmitField('Siguiente')
    name=StringField('Nombre')
    user=StringField('Usuario')
    email=StringField('Correa')
    contra=PasswordField('Contraseña')   

