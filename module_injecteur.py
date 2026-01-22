#not finish

import subprocess
import sys
import os
import re


def install_missing_dependencies(code):
    """
    Installe automatiquement les dépendances nécessaires au code Python donné.
    
    :param code: str, le code Python à analyser.
    """
    import_lines = [line for line in code.split("\n") if line.strip().startswith("import") or line.strip().startswith("from")]
        
    libraries = []
    for line in import_lines:
            parts = line.split()
            if line.startswith("import"):
                libraries.append(parts[1].split('.')[0])
            elif line.startswith("from"):
                libraries.append(parts[1].split('.')[0])

    for lib in libraries:
            try:
                __import__(lib)
            except ImportError:
                print(f"Installation de la bibliothèque manquante : {lib}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib,"--break-system-packages"])


def execute_code_with_dependencies(code):
    """
    Exécute un code Python avec gestion automatique des dépendances.
    
    :param code: str, le code Python à exécuter.
    """
    install_missing_dependencies(code)
    filename = "temp_script.py"
    with open(filename, "w") as f:
        f.write(code)

    try:
        result = subprocess.run([sys.executable, filename], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Erreur dans le script :\n{result.stderr}")
    except Exception as e:
        print(f"Erreur lors de l'exécution du code : {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def generate_code(code_string, filename='script.py'):
    """
    Génère un fichier Python à partir d'une chaîne de caractères contenant du code Python,
    puis exécute ce fichier.

    :param code_string: Une chaîne contenant le code Python à écrire et exécuter.
    :param filename: Le nom du fichier Python à générer (par défaut: 'generated_script.py').
    """
    print(code_string["thecode"]) 
    with open(filename, 'w') as file:
        file.write(code_string["thecode"])

def testr(input_str):
    lines = input_str.splitlines()

    if len(lines) > 2:
        lines = lines[1:-1]
    else:
        print("La chaîne est trop courte pour effectuer cette opération.")
        return ""

    return "\n".join(lines)
