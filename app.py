from flask import Flask,flash,render_template,request,redirect
from forms import IniciosesionForm,OlvidarForm,RegistrarForm
import yagmail as yagmail
import utils
from flask import session


app=Flask(__name__)
app.secret_key=b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def pagina():
    return render_template("page1.html")

@app.route("/registrarse", methods=('POST','GET'))
def Registrarse():
    session.clear()
    form=RegistrarForm()
    form1=IniciosesionForm()
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
            flash("Contraseña invalida")
            return render_template('registrarse.html',form=form)    
        
        yag = yagmail.SMTP('mintic2022@gmail.com', 'HolamundoMintic2020')  #SMTP protocolo de envío de correos      
        yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido, usa el link para activar tu cuenta')
        flash("Cuenta creada con éxito")
        return render_template('Iniciosesion.html', form= form1)
    return render_template("registrarse.html",form=form)

@app.route("/Olvidar",methods=('POST','GET'))
def olvidarcontraseña():
    olv=OlvidarForm()
    if request.method=='POST':
        correo=request.form.get('correo')

        if not utils.isEmailValid(correo):
            flash('Formato de correo invalido')
            return render_template('Olvidar.html',olv=olv)
        yag=yagmail.SMTP('mintic2022@gmail.com','HolamundoMintic2020')
        yag.send(to=correo,subject='Recuperación de contraseña',contents='Se le ha asignado la siguiente contraseña para su cuenta')

        return redirect('Iniciosesion')
    return render_template("Olvidar.html", olv=olv)

@app.route("/Galeria")
def galeria():
    return render_template("Galeria.html")

@app.route("/Iniciosesion", methods=('GET','POST'))
def iniciarsesion():
    form=IniciosesionForm()
    if form.is_submitted():
        result=request.form
        return render_template('index.html',result=result)

    return render_template("Iniciosesion.html",form=form)    