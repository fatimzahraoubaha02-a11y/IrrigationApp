import sys
import logging
import os
from pathlib import Path
from tkinter import messagebox

os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

logging.basicConfig(
    level=logging.ERROR,
    format='%(message)s',
    handlers=[
        logging.FileHandler('irrigation_app.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def setup_project_path():
    """
    Configure le chemin du projet pour les imports.
    Ajoute le répertoire racine au sys.path si nécessaire.
    """
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def check_dependencies():
    """
    Vérifie que toutes les dépendances requises sont installées.
    Affiche un message d'erreur et quitte si une dépendance manque.
    """
    try:
        import customtkinter
    except ImportError:
        print(" Installe customtkinter : pip install customtkinter")
        sys.exit(1)
    
    try:
        import pulp
    except ImportError:
        print(" Installe pulp : pip install pulp")
        sys.exit(1)


if __name__ == "__main__":
    try:
        setup_project_path()
        check_dependencies()

        from ui.interface import MainApp

        app = MainApp()
        app.mainloop()

    except Exception as e:
        logger.error(e)
        messagebox.showerror("Erreur", str(e))
        sys.exit(1)