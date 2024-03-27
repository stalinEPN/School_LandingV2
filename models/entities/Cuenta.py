
class Cuenta():

  def __init__(self,id , correo, contraseña):
    self.id = id
    
    self.correo_o_telefono = correo
    self.contraseña = contraseña

  def to_Dict(self):
    return{
      'id' : self.id,
      'cargo' : self.cargo,
      'nombre' : self.nombre,
      'apellido' : self.apellido,
      'descripcion' : self.descripcion,
      'foto' : self.get_base64_encoded_image()
    }
