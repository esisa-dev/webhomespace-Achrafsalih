from flask import Flask , render_template ,request , send_file

from login import Login
from gestionfichrep import gestionfichrep
from Accounts import Account

import os

login : Login
gsFiledr = gestionfichrep()
account = Account()
pathcurent : str = ""
fixUsername : str = ""

app = Flask(__name__,template_folder="template",static_folder = 'static')

@app.route("/")
def accueil():
    return render_template("Login.html")

@app.route('/logout')
def lougout():
    return render_template("Login.html")

@app.route("/auth",methods =["GET","POST"])
def home():
    global fixUsername
    global pathcurent
    username : str = request.form['username']
    password : str = request.form['password']
    login = Login(username,password)
    if username != "" :
        if login.authenticate() == True:   
            fixUsername = username
            pathcurent = "/home/"+username
            return render_template("home.html",directory = gsFiledr.get_path("/home/"+username) )
    return render_template("Login.html",erreur = "username or password incorrect ")

@app.route('/adduser',methods =["GET","POST"])
def createaccpunt():
    if request.method == 'GET':
        return render_template("createUser.html")
    else :
        username : str = request.form['username']
        password : str = request.form['password']
        repassword : str = request.form['repassword']
        if password != repassword : 
            return render_template("createUser.html",erreur = "password incorrect")
        if account.adduser(username,password) == False :
            return render_template("createUser.html",erreur = "username already exists")
        return render_template("home.html",directory = gsFiledr.get_path("/home/"+username))
    
@app.route('/deluser',methods =["GET","POST"])
def deleteuser():
    if request.method == 'GET':
        return render_template("deleteUser.html")
    else :
        username : str = request.form['username']
        password : str = request.form['password']
        if account.deleteuser(username,password) == False :
            return render_template("deleteUser.html",erreur = "username or password incorrect")
        return render_template("Login.html")

@app.route('/changepassw',methods =["GET","POST"])
def changepassword():
    if request.method == 'GET':
        return render_template("changePassword.html")
    else:
        username : str = request.form['username']
        password : str = request.form['password']
        newpassword : str = request.form['newpassword']
        if account.changePassword(username,password,newpassword) == False :
            return render_template("changePassword.html",erreur = "username or password incorrect")
        return render_template("home.html",directory = gsFiledr.get_path("/home/"+username))

 
@app.route('/<path:path>/',methods =["GET"]) 
def routefolders(path):
    try :
        global pathcurent
        pathcurent = "/"+path
        if os.path.isdir(pathcurent):
            return render_template("home.html",directory = gsFiledr.get_path(pathcurent))
        elif os.path.isfile(pathcurent):
            f = open(pathcurent)
            return render_template("home.html",text = f.read())
    except :
        return "erreur"

@app.route('/back',methods =["GET","POST"])
def back():
    global pathcurent
    t = pathcurent.split("/")
    if len(t) != 3 :
        pathcurent = ""
        for i in range(len(t)-1):
            pathcurent += t[i] + "/"
        pathcurent = pathcurent[:len(pathcurent)-1]
  
    if os.path.isdir(pathcurent):
       return render_template("home.html",directory = gsFiledr.get_path(pathcurent))


@app.route("/download")
def download():
    gsFiledr.home_directory(fixUsername)
    return send_file("/home/"+fixUsername+"/"+fixUsername+".zip", as_attachment=True)


@app.route('/nbrfiles')
def nbrfiles():
    return render_template("home.html",directory = gsFiledr.get_path(pathcurent),fil = str(gsFiledr.get_nbr_files(pathcurent)))


@app.route('/nbrdir')
def nbrdirs():
    return render_template("home.html",directory = gsFiledr.get_path(pathcurent),dir = str(gsFiledr.get_nbr_directory(pathcurent)))


@app.route('/space')
def space():
    return render_template("home.html",directory = gsFiledr.get_path(pathcurent),spa = str(gsFiledr.get_taille(pathcurent)))


@app.route('/findfile',methods =["GET","POST"])
def fileSearch():
    filename : str = request.form['file']
    return render_template("home.html",directory = gsFiledr.search_files_name_file_extention(pathcurent,filename))

if __name__ == '__main__':
    app.run()