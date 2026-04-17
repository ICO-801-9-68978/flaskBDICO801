from wtforms import Form, StringField, IntegerField, EmailField, SelectField, validators

class UserForm(Form):
    id = IntegerField("ID")
    nombre = StringField('Nombre')
    apaterno = StringField('Apaterno')
    amaterno = StringField('Amaterno')
    edad = IntegerField("Edad")
    correo = EmailField('Correo')

class MaestrosForm(Form):
    matricula = StringField('Matrícula', [validators.DataRequired()])
    nombre = StringField('Nombre', [validators.DataRequired()])
    apellidos = StringField('Apellidos', [validators.DataRequired()])
    especialidad = StringField('Especialidad', [validators.DataRequired()])
    email = StringField('Email', [validators.Email()])

class CursosForm(Form):
    id = IntegerField("ID")
    nombre = StringField('Nombre del Curso', [validators.DataRequired()])
    descripcion = StringField('Descripción')
    maestro_id = SelectField('Maestro Asignado', coerce=int)

class InscripcionForm(Form):
    alumno_id = SelectField('Seleccionar Alumno', coerce=int)
   
class ConsultaAlumnosCursoForm(Form):
    curso_id = SelectField('Seleccionar Curso', coerce=int)

class ConsultaCursosAlumnoForm(Form):
    alumno_id = SelectField('Seleccionar Alumno', coerce=int)

class ConsultaCursosMaestroForm(Form):
    maestro_id = SelectField('Seleccionar Maestro', coerce=int)