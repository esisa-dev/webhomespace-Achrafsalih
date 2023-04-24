import crypt
import os
import spwd

class Login:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        
    def find_user(self) -> bool:
          return os.path.exists(f'/home/{self.username}')
    
    def compare_password(self) -> bool:
       try:
            user_info = spwd.getspnam(self.username)
            hashed_password, salt = user_info.sp_pwdp , user_info.sp_pwdp
            generated_hash = crypt.crypt(self.password, salt)
            return generated_hash == hashed_password
       except KeyError:
            return False
    
    def authenticate(self) -> bool:
       return self.find_user() and self.compare_password()
