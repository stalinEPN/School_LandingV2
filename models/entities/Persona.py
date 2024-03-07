import base64
class Persona():

  def __init__(self,id , cargo, nombre, apellido, descripcion, foto):
    self.id = id
    self.cargo = cargo
    self.nombre = nombre
    self.apellido = apellido
    self.descripcion = descripcion
    self.foto = foto

  def to_Dict(self):
    return{
      'id' : self.id,
      'cargo' : self.cargo,
      'nombre' : self.nombre,
      'apellido' : self.apellido,
      'descripcion' : self.descripcion,
      'foto' : self.get_base64_encoded_image()
    }
  
  def get_base64_encoded_image(self):
        if self.foto:
            return base64.b64encode(self.foto).decode('utf-8')
        else:
            return None