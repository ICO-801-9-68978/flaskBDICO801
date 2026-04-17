from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Curso, Maestros
import forms

cursos_bp = Blueprint('cursos', __name__)

# ====================== LISTAR ======================
@cursos_bp.route("/cursos")
def cursos():
    return render_template("cursos/cursos.html", cursos=Curso.query.all())

# ====================== INSERTAR ======================
@cursos_bp.route('/insertar_curso', methods=['GET', 'POST'])
def insertar():
    form = forms.CursosForm(request.form)
    # Llenamos el select con los maestros disponibles
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'POST':
        cur = Curso(
            nombre=form.nombre.data, 
            descripcion=form.descripcion.data, 
            maestro_id=form.maestro_id.data
        )
        db.session.add(cur)
        db.session.commit()
        return redirect(url_for('cursos.cursos'))
    
    return render_template("cursos/insertar_curso.html", form=form)

# ====================== MODIFICAR ======================
@cursos_bp.route('/modificar_curso', methods=['GET', 'POST'])
def modificar():
    cur = Curso.query.get(request.args.get('id'))
    form = forms.CursosForm(request.form, obj=cur)
    # Llenamos el select para que muestre el maestro actual y los disponibles
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'POST':
        form.populate_obj(cur)
        db.session.commit()
        return redirect(url_for('cursos.cursos'))
        
    return render_template("cursos/modificar_curso.html", form=form)

# ====================== DETALLES ======================
@cursos_bp.route('/detalles_curso', methods=['GET'])
def detalles_curso():
    id = request.args.get('id')
    if not id:
        return redirect(url_for('cursos.cursos'))
    
    cur = Curso.query.filter_by(id=id).first()
    if not cur:
        return "Curso no encontrado", 404
        
    return render_template("cursos/detalles_curso.html", cur=cur)

# ====================== ELIMINAR ======================
@cursos_bp.route('/eliminar_curso', methods=['GET', 'POST'])
def eliminar():
    cur = Curso.query.get(request.args.get('id'))
    form = forms.CursosForm(request.form, obj=cur)
    # Llenamos las opciones por si el HTML necesita mostrar el nombre del maestro
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'POST':
        db.session.delete(cur)
        db.session.commit()
        return redirect(url_for('cursos.cursos'))
        
    # Pasamos tanto el 'form' (para el token de seguridad) como 'cur' (para los datos visuales)
    return render_template("cursos/eliminar_curso.html", form=form, cur=cur)