from conexion import Conexion
import time
import hashlib
import smtplib
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
		s = smtplib.SMTP(host='smtp.gmail.com', port=465)
		s.ehlo()
		s.starttls()
		s.login("test.galeria.tic@gmail.com", "galeria.tic.1234")
		msg = MIMEMultipart('alternative')
		message_template_text = "Hola, sigue este enlace LINK_URL para activar tu cuenta"
		message_template_html = "Hola, sigue este <a href='LINK_URL' target='_blank'> enlace </a> para activar tu cuenta"
		message_html = message_template_html.substitute(LINK_URL = "http://127.0.0.1:5000/activar?codigo=" + self.codigoActivacion)
		message_text = message_template_text.substitute(LINK_URL = "http://127.0.0.1:5000/activar?codigo=" + self.codigoActivacion)

		msg['From'] = "test.galeria.tic@gmail.com"
		msg['To'] = self.correo
		msg['Subject'] = "Correo de activación de cuenta"

		msg.attach(MIMEText(message_text, 'plain'))
		msg.attach(MIMEText(message_html, 'html'))

		s.send_message(msg['From'], msg['To'],msg.as_string())
		s.quit()
		del msg







