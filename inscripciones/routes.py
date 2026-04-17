from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Curso, Alumnos, Inscripcion
import forms

inscripciones_bp = Blueprint('inscripciones', __name__)

# ====================== LISTAR CURSOS PARA INSCRIBIR ======================
@inscripciones_bp.route("/inscripciones")
def inscripciones():
    # Mandamos todos los cursos a la tabla principal
    cursos_list = Curso.query.all()
    return render_template("inscripciones/inscripciones.html", cursos=cursos_list)

# ====================== AÑADIR ALUMNO AL CURSO ======================
@inscripciones_bp.route("/inscribir_alumno", methods=['GET', 'POST'])
def inscribir():
    curso_id = request.args.get('curso_id')
    if not curso_id:
        return redirect(url_for('inscripciones.inscripciones'))
    
    curso = Curso.query.get_or_404(curso_id)
    form = forms.InscripcionForm(request.form)
    
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apaterno} {a.amaterno}") for a in Alumnos.query.all()]

    if request.method == 'POST':
        existe = Inscripcion.query.filter_by(alumno_id=form.alumno_id.data, curso_id=curso.id).first()
        
        if not existe:
            nueva_inscripcion = Inscripcion(
                alumno_id=form.alumno_id.data, 
                curso_id=curso.id
            )
            db.session.add(nueva_inscripcion)
            db.session.commit()
            
        return redirect(url_for('inscripciones.inscripciones'))

    return render_template("inscripciones/inscribir_alumno.html", form=form, curso=curso)