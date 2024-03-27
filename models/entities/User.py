from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
class User(UserMixin):

  def __init__(self, id, username, password, email=" ") -> None:
    self.id = id
    self.username = username
    self.password = password
    self.email = email


  @classmethod
  def check_password(self, hasshedPass, password):
    return check_password_hash(hasshedPass, password)

  


if __name__ == '__main__':


  print(generate_password_hash("admin"))
