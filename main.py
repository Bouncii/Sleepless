import sys
import subprocess
import importlib

def check_and_install(package_name, import_name=None):
    '''
    Vérifie si une librairie est installée. Si non, l'installe.
    entrée:
        package_name : le nom à utiliser pour pip install (ex: pygame-ce)
        import_name : le nom utilisé dans le code (ex: pygame). Si None, utilise package_name.
    sortie : None
    '''
    if import_name is None:
        import_name = package_name

    try:
        importlib.import_module(import_name)
    except ImportError:
        
        print(f"⚠️ La librairie '{import_name}' est manquante. Installation automatique de '{package_name}' en cours...")

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ '{package_name}' installé avec succès !")
            importlib.invalidate_caches()

        except Exception as e:
            print(f"❌ Erreur lors de l'installation de {package_name}: {e}")
            sys.exit(1)

check_and_install("pygame-ce", "pygame") 
check_and_install("pygame_gui")


from src.core.game import Game

def main():
    '''Fonction principale pour lancer le jeu'''
    game = Game()
    game.run() 

if __name__ == "__main__":
    main()