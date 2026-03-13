from flask  import Flask, render_template,request, redirect, url_for
from flask import flash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Alumnos, Maestros # Agregado Maestros
import forms  

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate=Migrate(app, db)
csrf = CSRFProtect(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_alumno = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_alumno, alumno=alumno)

@app.route("/maestros",methods=["GET","POST"])
def maestros():
    mat=0
    nom=''
    ape=''
    esp=''
    email=''
    maestros_clas=forms.MaestroForm(request.form)
    if request.method=='POST':
        mat=maestros_clas.matricula.data
        nom=maestros_clas.nombre.data
        ape=maestros_clas.apellidos.data
        esp=maestros_clas.especialidad.data
        email=maestros_clas.correo.data
        
        # Guardar en la base de datos igual que Alumnos
        nuevo_maestro = Maestros(matricula=mat, nombre=nom, apellidos=ape, 
                                 especialidad=esp, email=email)
        db.session.add(nuevo_maestro)
        db.session.commit()
    
    # Select para mostrar en la tabla de maestros.html
    lista_maestros = Maestros.query.all()
    
    return render_template('maestros.html', form=maestros_clas, maestros=lista_maestros,
                           mat=mat, nom=nom, ape=ape, esp=esp, email=email)

@app.route("/usuarios",methods=["GET","POST"])
def usuario():
    mat=0
    nom=''
    apa=''
    ama=''
    edad=0
    email=''
    usuarios_clas=forms.UserForm(request.form)
    if request.method=='POST':
        mat=usuarios_clas.matricula.data
        nom=usuarios_clas.nombre.data
        apa=usuarios_clas.apaterno.data
        ama=usuarios_clas.amaterno.data
        edad=usuarios_clas.edad.data
        email=usuarios_clas.correo.data
    
    return render_template('usuarios.html',form=usuarios_clas,mat=mat,
                           nom=nom,apa=apa,ama=ama,edad=edad,email=email)

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()