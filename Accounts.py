import subprocess
import os

from login import Login
class Account : 
    
    def __init__(self) -> None:
        pass
    
    def adduser(self,username,password) -> bool:
        if username in os.listdir("/home"):
            return False
        try :
            cmd = f"sudo adduser {username} --gecos '' --disabled-password"
            subprocess.run(cmd.split(), check=True)
            cmd = f"echo '{username}:{password}' | sudo chpasswd"
            subprocess.run(cmd, shell=True, check=True)
        except :
            return False
        return True
    
    def deleteuser(self,username,password) -> bool:
        test = Login(username,password)
        try :
            if test.authenticate() == False :
                return False
            command = f"sudo deluser {username}"
            os.system(command)
        except :
            return False
        return True
    
    def changePassword(self,username,password,new_password)  -> bool:
        test = Login(username,password)
        if test.authenticate() == False :
            return False
        try :
            command = f"echo '{username}:{new_password}' | sudo chpasswd"
            os.system(command)
        except : 
            return False
        return True
    
if __name__ == "__main__":
    a =  Account()
    # a.changePasswprd("asss","azertyu")
    # print(a.adduser("as","azerty"))
    #print(a.deleteuser("as","sdsdsd"))

 