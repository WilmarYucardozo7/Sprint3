from conexion import Conexion
from flask import render_template, redirect
import time
import hashlib
import smtplib
import yagmail as yagmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Usuario():
	def __init__(self, id = "", usuario = "", nombres = "", apellidos = "", correo = "", contrasena = "", activo = 0, codigoActivacion = ""):
		self.id = id
		self.usuario = usuario
		self.nombres = nombres
		self.apellidos = apellidos
		self.correo = correo
		self.contrasena = contrasena
		self.activo = activo
		self.codigoActivacion = codigoActivacion
		

	def setId(self, id):
		self.id = id

	def setUsuario(self, usuario):
		self.usuario = usuario

	def setNombres(self, nombres):
		self.nombres = nombres

	def setApellidos(self, apellidos):
		self.apellidos = apellidos

	def setCorreo(self, correo):
		self.correo = correo

	def setContrasena(self, contrasena):
		self.contrasena = contrasena

	def setActivo(self, activo):
		self.activo = activo

	def setCodigoActivacion(self, codigoActivacion):
		self.codigoActivacion = codigoActivacion


	def getId(self):
		return self.id

	def getUsuario(self):
		return self.usuario

	def getNombres(self):
		return self.nombres

	def getApellidos(self):
		return self.apellidos

	def getCorreo(self):
		return self.correo

	def getContrasena(self):
		return self.contrasena

	def getActivo(self):
		return self.activo

	def getCodigoActivacion(self):
		return self.codigoActivacion

	def registrar(self):
		resultado = {
			"estado": "error",
			"error": "No se pudo crear la cuenta del usuario"
		}
		con = Conexion()
		hayConexion = con.getConexion()
		if hayConexion:
			try:
				codigo = self.usuario + self.contrasena + str(time.time())
				codigo = codigo.encode('utf-8')
				codigo = hashlib.md5(codigo)
				self.codigoActivacion = codigo.hexdigest()
				query = "INSERT INTO usuarios(usuario, nombres, apellidos, correo, contrasena, activo, codigo_activacion) VALUES(%s, %s, %s, %s, %s, %s, %s)"
				params = (self.usuario, self.nombres, self.apellidos, self.correo, self.contrasena, 0, self.codigoActivacion)
				resultadoQuery = con.ejecutar(query, params, False)
				if resultadoQuery:
					resultado["estado"] = "ok"
					resultado["error"] = con.error
					self.enviarCorreoActivacion()
				else:
					resultado["error"] = con.error
			except Exception as e:
				resultado["error"] = ("Error: %s" % (e))
			except:
				resultado["error"] = "Error desconocido"
		else:
			resultado['error'] =  "No hay conexión: " + con.error
		return resultado

	def enviarCorreoActivacion(self):
                yag=yagmail.SMTP('mintic2022@gmail.com','HolamundoMintic2020')
                message_template_text = 'Hola, sigue este enlace http://127.0.0.1:5000/activar?codigo=' + self.codigoActivacion +' para activar tu cuenta'
                yag.send(to=self.correo,subject='Activar cuenta', contents=message_template_text)
                return redirect('Iniciosesion')
