from flask import Flask,flash,render_template,request,make_response,redirect,url_for,session,current_app,g
from forms import IniciosesionForm,OlvidarForm,RegistrarForm,NuevaContraseña
import yagmail as yagmail
import utils
import os
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from db import get_db
from functools import wraps

def login_required(view):
    @wraps(view)
    def wrapped_view():
        if g.user is None:
            return redirect(url_for('iniciarsesion'))
        return view()
    return wrapped_view
app=Flask(__name__)
app.secret_key=os.urandom(20)
s=URLSafeTimedSerializer(app.secret_key)
@app.route("/",methods=('GET','POST'))
def pagina():
    if request.method=='POST':
         session.clear()
         return render_template("page1.html")
    if g.user:
        return redirect(url_for('perfil'))
    return render_template("page1.html")

@app.route("/registrarse", methods=('POST','GET'))
def Registrarse():
    if g.user:
        return redirect(url_for('perfil'))
    form=RegistrarForm()
    if request.method=='GET':
         return render_template("registrarse.html",form=form)
    if request.method == 'POST':
        name= request.form.get('name') 
        email = request.form.get('email')
        username = request.form.get('user')
        password = request.form.get('contra')
        
        if not utils.isUsernameValid(name):
            flash("Nombre invalido")
        if not utils.isEmailValid(email):
            flash("Correo invalido")
            return render_template('registrarse.html',form=form)
        if not utils.isUsernameValid(username):
            flash("Usuario invalido")
            return render_template('registrarse.html',form=form)    
        if not utils.isPasswordValid(password):
            flash("La contraseña debe tener al menos una mayúscula y un número")
            return render_template('registrarse.html',form=form)        
        

        db=get_db()
        usuariodisponible=db.execute("SELECT * FROM usuario WHERE user = ?",(username,)).fetchall()
        if usuariodisponible:
            flash("El usuario no esta disponible")
            return render_template('registrarse.html',form=form) 
        else:
            correodisponible=db.execute("SELECT * FROM usuario WHERE correo = ?",(email,)).fetchall()
            if correodisponible:
                flash("El correo ya está registrado")
                return render_template('registrarse.html',form=form) 
       
        activacion=s.dumps(email,salt='activacion-correo')
        hash_password=generate_password_hash(password)
        db.execute("INSERT INTO usuario (nombre,user,correo,contraseña,activo,activacion) values (?,?,?,?,?,?)",(name,username,email,hash_password,False,activacion))
        db.commit()
        link=url_for('confirmar_correo',activacion=activacion,_external=True)
        yag = yagmail.SMTP('mintic2022@gmail.com', 'HolamundoMintic2020')  #SMTP protocolo de envío de correos      
        yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido, usa el link para activar tu cuenta ' +link)
        form1=IniciosesionForm()
        return render_template('Iniciosesion.html', form= form1)
    
@app.route('/confirmar_correo/<activacion>')
def confirmar_correo(activacion):
    try:
        email=s.loads(activacion,salt='activacion-correo',max_age=60)
    except SignatureExpired:
        return '<h1> El enlace ha expirado </h1>'
    db=get_db()
    db.execute("update usuario set activo=? where activacion=?",(True,activacion))
    db.commit()    
    return '<h1> La cuenta ha sido activada con éxito </h1>'

@app.route("/Olvidar",methods=('POST','GET'))
def olvidarcontraseña():
    olv1=OlvidarForm()
    if request.method=='POST':
        correo=request.form.get('correo')

        if not utils.isEmailValid(correo):
            flash('Formato de correo invalido')
            return render_template('Olvidar.html',olv=olv1)
        recuperacion=s.dumps(correo,salt='recuperacion-correo')
        link=url_for('recuperar_contraseña',recuperacion=recuperacion,_external=True)   
        db=get_db()
        db.execute("update usuario set activacion = ? where correo = ?",(recuperacion,correo))
        db.commit() 
        yag=yagmail.SMTP('mintic2022@gmail.com','HolamundoMintic2020')
        yag.send(to=correo,subject='Recuperación de contraseña',contents='Ingrese al link para cambiar la contraseña de la cuenta '+link)

        return redirect(url_for('pagina'))
    return render_template("Olvidar.html", olv1=olv1)

@app.route('/recuperar_contrasena/<recuperacion>',methods=('POST','GET'))
def recuperar_contraseña(recuperacion):
    try:
        cambio=s.loads(recuperacion,salt='recuperacion-correo',max_age=500)
    except SignatureExpired:
        return '<h1> El enlace ha expirado </h1>'

    return redirect(url_for('recuperar',recuperacion=recuperacion))


@app.route("/Recuperar/<recuperacion>",methods=('POST','GET'))
def recuperar(recuperacion):
    olv=NuevaContraseña()
    if request.method=='POST':
        contraseña=request.form.get('contraseña')
        if not utils.isPasswordValid(contraseña):
            flash('La contraseña debe tener al menos una mayúscula y un número')
            return render_template('Recuperar.html',olv=olv)    
        db=get_db()
        db.execute("update usuario set contraseña = ? where activacion = ?",(contraseña,recuperacion))
        db.commit() 
        return redirect(url_for('iniciarsesion'))
    return render_template('Recuperar.html',olv=olv)
    


@app.route("/perfil")
@login_required
def perfil():
    return render_template("index.html")

@app.route("/Galeria")
def galeria():
    return render_template("Galeria.html")


@app.route("/Iniciosesion", methods=('GET','POST'))
def iniciarsesion():
    form=IniciosesionForm()
    error=None
    if g.user:
        return redirect(url_for('perfil'))
    if request.method=='POST':
        usuario=request.form.get('usuario')
        contraseña=request.form.get('contraseña')
        db=get_db()
        user=db.execute("SELECT * FROM usuario WHERE user = ? ",(usuario, )).fetchone()
        if user is None:
            error='Usuario inválido'
        else:
            if check_password_hash(user[4],contraseña):
                 session.clear()
                 session['id']=user[0]
                 resp=make_response(redirect(url_for('perfil')))
                 resp.set_cookie('usuario',usuario)
            error='Contraseña invalida'
        flash(error)
        return render_template("Iniciosesion.html",form=form)  
    
    return render_template("Iniciosesion.html",form=form)    


@app.before_request
def load_logged_in_user():
    user_id=session.get('id')
    print(user_id)
    if user_id is None:
        g.user=None
    else:
        g.user=get_db().execute('SELECT * FROM usuario where id = ?',(user_id,)).fetchone()