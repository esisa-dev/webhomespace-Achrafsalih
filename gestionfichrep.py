import os
import subprocess
import zipfile


class gestionfichrep:
    
    def __init__(self):
        pass
    
    def get_path(self, path):
        return [
            {
                'chemin': os.path.join(path, i),
                'nom': i,
            } for i in os.listdir(path) if not i.startswith('.')
        ]
    
    def get_user_directory(self, path):
        return [
            i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))
        ]
    
    def get_user_files(self, path):
        return [
            i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))
        ]
    
    def get_nbr_files(self, path):
        return len([
            i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and not i.startswith('.')
        ])
    
    def get_nbr_directory(self, path):
        return len([
            i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))
        ])
    
    def get_taille(self, path):
        cmd = ['du', '-s', path]
        try:
            return subprocess.run(cmd, capture_output=True, text=True).stdout.split()[0]
        except:
            return 0
        
    def search_files_name_file_extention(self, path, filename):
        return [
            {
                'chemin': os.path.join(path, i),
                'nom': i,
            } for i in os.listdir(path) if not i.startswith('.') and filename in i
        ]
    
    def home_directory(self, username):
        home_dir = os.path.expanduser('/home/' + username)
        zip_filename = os.path.join(home_dir, username + '.zip')
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(home_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, home_dir))


if __name__ == "__main__":
    a = gestionfichrep()
    a.get_path("/home/t")
    # print(a.get_nbr_fichier("/home"))
    # print(a.get_taille("/home/t"))
    # a.telechercher_home_directory()
    # a.recherche_files(".html")
