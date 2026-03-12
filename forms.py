from wtforms import Form
from wtforms import StringField, IntegerField, EmailField
from wtforms import validators

class UserForm(Form):
    id = IntegerField("Matricula")
    nombre = StringField('Nombre')
    apaterno = StringField('Apaterno')
    amaterno = StringField('Amaterno')
    edad = IntegerField("Edad")
    correo = EmailField('Correo')

class MaestroForm(Form):
    matricula = IntegerField("Matricula")
    nombre = StringField('Nombre')
    apellidos = StringField('Apellidos')
    especialidad = StringField('Especialidad')
    correo = EmailField('Correo')