from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Maestros
import forms

maestros_bp = Blueprint('maestros', __name__)

# ====================== LISTAR ======================
@maestros_bp.route("/maestros", methods=['GET'])
def maestros():
    form = forms.MaestrosForm(request.form)
    maestro_list = Maestros.query.all()
    return render_template("maestros/maestros.html", form=form, maestro=maestro_list)

# ====================== INSERTAR ======================
@maestros_bp.route('/insertar_maestro', methods=['GET', 'POST'])
def insertar():
    form = forms.MaestrosForm(request.form)

    if request.method == 'POST':
        mae = Maestros(
            matricula=form.matricula.data,
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )
        db.session.add(mae)
        db.session.commit()
        return redirect(url_for('maestros.maestros'))

    return render_template("maestros/insertar_maestro.html", form=form)

# ====================== DETALLES ======================
@maestros_bp.route('/detalles_maestro', methods=['GET'])
def detalles_maestro():
    matricula = request.args.get('mat')
    if not matricula:
        return redirect(url_for('maestros.maestros'))
    
    mae = Maestros.query.filter_by(matricula=matricula).first()
    if not mae:
        return "Maestro no encontrado", 404
    
    # Se envía el objeto completo para poder iterar sobre sus cursos en el HTML
    return render_template("maestros/detalles_maestro.html", mae=mae)

# ====================== MODIFICAR ======================
@maestros_bp.route('/modificar_maestro', methods=['GET', 'POST'])
def modificar():
    form = forms.MaestrosForm(request.form)
    matricula = request.args.get('mat')

    if not matricula:
        return redirect(url_for('maestros.maestros'))

    mae = Maestros.query.filter_by(matricula=matricula).first()
    if not mae:
        return "Maestro no encontrado", 404

    if request.method == 'GET':
        form.matricula.data = mae.matricula
        form.nombre.data = mae.nombre
        form.apellidos.data = mae.apellidos
        form.especialidad.data = mae.especialidad
        form.email.data = mae.email

    if request.method == 'POST':
        mae.nombre = form.nombre.data
        mae.apellidos = form.apellidos.data
        mae.especialidad = form.especialidad.data
        mae.email = form.email.data
        
        db.session.add(mae)
        db.session.commit()
        return redirect(url_for('maestros.maestros'))

    return render_template("maestros/modificar_maestro.html", form=form)

# ====================== ELIMINAR ======================
@maestros_bp.route('/eliminar_maestro', methods=['GET', 'POST'])
def eliminar():
    form = forms.MaestrosForm(request.form)
    
    # Capturamos la matrícula ya sea por la URL (GET) o por el formulario oculto (POST)
    matricula = request.args.get('mat') or request.form.get('matricula_oculta')

    if not matricula:
        return redirect(url_for('maestros.maestros'))

    mae = Maestros.query.filter_by(matricula=matricula).first()
    if not mae:
        return "Maestro no encontrado", 404

    # Obtenemos TODOS los demás maestros para poder reasignar los cursos
    otros_maestros = Maestros.query.filter(Maestros.matricula != matricula).all()

    if request.method == 'GET':
        form.matricula.data = mae.matricula
        form.nombre.data = mae.nombre
        form.apellidos.data = mae.apellidos
        form.especialidad.data = mae.especialidad
        form.email.data = mae.email
        
        return render_template("maestros/eliminar_maestro.html", form=form, mae=mae, otros_maestros=otros_maestros)

    if request.method == 'POST':
        # 1. Verificar si el maestro tiene cursos asignados
        if mae.cursos:
            nuevo_maestro_id = request.form.get('nuevo_maestro')
            if nuevo_maestro_id:
                # Reasignar todos los cursos al nuevo maestro seleccionado
                for curso in mae.cursos:
                    curso.maestro_id = int(nuevo_maestro_id)
                # Aplicamos los cambios en los cursos ANTES de borrar al maestro
                db.session.commit()
            else:
                return "Debe seleccionar un maestro para reasignar los cursos", 400

        # 2. Ahora que los cursos están a salvo o no tenía cursos, eliminamos al maestro
        db.session.delete(mae)
        db.session.commit()
        return redirect(url_for('maestros.maestros'))