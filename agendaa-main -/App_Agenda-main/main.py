from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key=  'lucero'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db1.sqlite"

db = SQLAlchemy(app) 


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    nombre = db.Column(db.Text, nullable=False)    

class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Text, nullable=False,default='Pediente')
    email = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/",methods=['GET','POST'])
def index():
    if session:
        if request.method=='POST':
            name = request.form.get('name')
            if name:
                obj = Tareas(nombre=name,email=session['email'] )
                db.session.add(obj)
                db.session.commit()
                lista_tareas = Tareas.query.all()
            return render_template('index.html',lista_tareas = lista_tareas)

        else:
            lista_tareas = Tareas.query.all()
            return render_template('index.html',session=session,lista_tareas = lista_tareas)
            # return render_template('index.html',lista_tareas = lista_tareas)
    else:
        return redirect(url_for('login'))
   
# Rutas seguras
@app.route("/change_passwor")
def change_passwor():
    session.clear()
    return redirect(url_for('login'))

@app.route("/change_password")
def change_password():
    return render_template('change_password.html')


@app.route("/update/<id>")
def update_task(id):
    obj = Tareas.query.filter_by(id = id).first()
    if obj.estado == "Hecho":
        obj.estado = "Pendiente"
    else:
        obj.estado = "Hecho"
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<id>")
def delete_task(id):
    obj= Tareas.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('index'))


#rutas No seguras
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(email=email, password=password).first()
        print(usuario)
        if usuario:
            session['email']=usuario.email
            session['nombre']=usuario.nombre
            return redirect(url_for('index'))
        else:
            error = "Usuario o pass incorrecto"
            return render_template('login.html',error=error)
    return render_template('login.html')

with app.app_context():
    db.create_all()
    try:
        obj=Usuario(email='admin@admin.com', password='12345',nombre='Admin')
        db.session.add(obj)
        db.session.commit()
    except:
        pass




@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/registe")
def registe():
    obj = Usuario(email='angel.ucero@gmail.com',password="12345",nombre='Angel Lucero')
    db.session.add(obj)
    db.session.commit()
    return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template('register.html')
    
if __name__  ==  "__main__":
    app.run(debug=True)