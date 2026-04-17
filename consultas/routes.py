from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Curso, Alumnos, Maestros
import forms

consultas_bp = Blueprint('consultas', __name__)

# 1. MENÚ PRINCIPAL DE CONSULTAS
@consultas_bp.route("/consultas")
def menu_consultas():
    return render_template("consultas/consultas.html")

# 2. CONSULTA: ALUMNOS POR CURSO
@consultas_bp.route("/consultas/alumnos_curso", methods=['GET', 'POST'])
def alumnos_curso():
    form = forms.ConsultaAlumnosCursoForm(request.form)
    # Llenamos el select con los cursos
    form.curso_id.choices = [(c.id, c.nombre) for c in Curso.query.all()]
    
    alumnos_inscritos = None
    curso_seleccionado = None
    
    if request.method == 'POST':
        # Obtenemos el ID del curso seleccionado
        curso_id = form.curso_id.data
        curso_seleccionado = Curso.query.get(curso_id)
        # ¡La magia de SQLAlchemy! Sacamos los alumnos directo de la relación
        if curso_seleccionado:
            alumnos_inscritos = curso_seleccionado.alumnos
            
    return render_template("consultas/alumnos_curso.html", form=form, alumnos=alumnos_inscritos, curso=curso_seleccionado)

# 3. CONSULTA: CURSOS POR ALUMNO
@consultas_bp.route("/consultas/cursos_alumno", methods=['GET', 'POST'])
def cursos_alumno():
    form = forms.ConsultaCursosAlumnoForm(request.form)
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apaterno}") for a in Alumnos.query.all()]
    
    cursos_inscritos = None
    alumno_seleccionado = None
    
    if request.method == 'POST':
        alumno_id = form.alumno_id.data
        alumno_seleccionado = Alumnos.query.get(alumno_id)
        if alumno_seleccionado:
            cursos_inscritos = alumno_seleccionado.cursos
            
    return render_template("consultas/cursos_alumno.html", form=form, cursos=cursos_inscritos, alumno=alumno_seleccionado)

# 4. CONSULTA: CURSOS POR MAESTRO
@consultas_bp.route("/consultas/cursos_maestro", methods=['GET', 'POST'])
def cursos_maestro():
    form = forms.ConsultaCursosMaestroForm(request.form)
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    cursos_impartidos = None
    maestro_seleccionado = None
    
    if request.method == 'POST':
        maestro_id = form.maestro_id.data
        maestro_seleccionado = Maestros.query.get(maestro_id)
        if maestro_seleccionado:
            cursos_impartidos = maestro_seleccionado.cursos
            
    return render_template("consultas/cursos_maestro.html", form=form, cursos=cursos_impartidos, maestro=maestro_seleccionado)