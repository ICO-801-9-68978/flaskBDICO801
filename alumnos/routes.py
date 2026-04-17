from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Alumnos 
import forms

alumnos_bp = Blueprint('alumnos', __name__)

# ====================== MENÚ PRINCIPAL ======================
@alumnos_bp.route("/")
@alumnos_bp.route("/index")
def index():
    create_alumno = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    # Muestra el panel con las 5 tarjetas de módulos
    return render_template("index.html", form=create_alumno, alumno=alumno)

# ====================== LISTAR ALUMNOS (Solo Tabla) ======================
@alumnos_bp.route("/Alumnos", methods=['GET'])
def alumnos():
    alumnos_registrados = Alumnos.query.all()
    return render_template("alumnos/Alumnos.html", alumno=alumnos_registrados)

# ====================== INSERTAR ======================
@alumnos_bp.route("/insertar", methods=['GET', 'POST'])
def insertar():
    form = forms.UserForm(request.form)
    
    if request.method == 'POST':
        alum = Alumnos(
            nombre=form.nombre.data, 
            apaterno=form.apaterno.data, 
            amaterno=form.amaterno.data, 
            edad=form.edad.data, 
            correo=form.correo.data
        )
        db.session.add(alum)
        db.session.commit()
        # Regresa a la tabla después de guardar
        return redirect(url_for('alumnos.alumnos'))
        
    return render_template("alumnos/insertar.html", form=form)

# ====================== MODIFICAR ======================
@alumnos_bp.route("/modificar", methods=['GET', 'POST'])
def modificar():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    form = forms.UserForm(request.form, obj=alum)
    
    if request.method == 'POST':
        form.populate_obj(alum)
        db.session.commit()
        # Regresa a la tabla después de editar
        return redirect(url_for('alumnos.alumnos'))
    
    return render_template("alumnos/modificar.html", form=form)

# ====================== ELIMINAR ======================
@alumnos_bp.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    form = forms.UserForm(request.form, obj=alum)
    
    if request.method == 'POST':
        db.session.delete(alum)
        db.session.commit()
        # Regresa a la tabla después de borrar
        return redirect(url_for('alumnos.alumnos'))
    
    return render_template('alumnos/eliminar.html', form=form)

# ====================== DETALLES ======================
@alumnos_bp.route("/detalles")
def detalles():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    
    if not alum:
        return redirect(url_for('alumnos.alumnos'))
        
    return render_template('alumnos/detalles.html', 
                           id=alum.id, 
                           nombre=alum.nombre, 
                           apaterno=alum.apaterno, 
                           amaterno=alum.amaterno, 
                           edad=alum.edad, 
                           correo=alum.correo)