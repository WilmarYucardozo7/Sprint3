#!/usr/bin/python

import MySQLdb

class Conexion():
	
	def __init__(self):
		# Variable que determina si estamos conectados a MySQL...
		self.connected = 0
		self.error = ""
		self.conexion = None

	def getConexion(self):
		resultado = False
		try:
			if self.connected == 0:
				self.db = MySQLdb.connect("localhost", "root", "toor", "galeria")
				self.connected = 1
				self.conexion = self.db.cursor()
				resultado = True
		except Exception as e:
			self.error = ("Error: %s" % (e))
		except:
			self.error = "Error desconocido"
		return resultado

	def cerrarConexion(self):
		self.connected = 0
		try:
			self.conexion.close()
		except:pass

	def ejecutar(self, query, params = None, execute = True):
		resultado = False
		if self.connected:
			self.error=""
			try:
				self.conexion.execute(query,params)
				self.db.commit()
				if execute:
				    # convert de result to dictionary
				    result = []
				    columns = tuple([d[0].decode('utf8') for d in self.conexion.description])
				    for row in self.conexion:
				        result.append(dict(zip(columns, row)))
				    resultado = result
				resultado = True
			except Exception as e:
				self.error= ("Error: %s" % (e))
		return resultado

	def ultimoId(self):
		return self.conexion.lastrowid
