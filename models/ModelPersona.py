from database.db import get_connection
from .entities.Persona import Persona
from flask import flash
from psycopg2 import IntegrityError

class ModelPersona():

  @classmethod
  def get_personas(self):
    try:
      conn = get_connection()
      personas = []

      with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM personas ORDER BY id')
        resultset = cursor.fetchall()

        for row in resultset:
          persona = Persona(row[0], row[1], row[2], row[3], row[4], row[5])
          personas.append(persona.to_Dict())
      conn.close()
      return personas
    except Exception as ex:
      raise Exception(ex)
    
  @classmethod
  def edit_persona_Nofoto(self, p: Persona):
    try:
      conn = get_connection()
      cursor = conn.cursor()
      sql = "UPDATE personas SET nombre = %s, apellido = %s, descripcion = %s WHERE id = %s"
      params = (p.nombre, p.apellido, p.descripcion, p.id)
      cursor.execute(sql, params)
      conn.commit()
      flash("Guardado correctamente", "success")
    except Exception as ex:
      raise Exception(ex)
    

  @classmethod
  def edit_persona_foto(self, p: Persona):
    try:
      conn = get_connection()
      cursor = conn.cursor()
      sql = "UPDATE personas SET nombre = %s, apellido = %s, descripcion = %s, foto = %s WHERE id = %s"
      params = (p.nombre, p.apellido, p.descripcion, p.foto, p.id)
      cursor.execute(sql, params)
      conn.commit()
      flash("Guardado correctamente", "success")
    except Exception as ex:
      raise Exception(ex)
      
    