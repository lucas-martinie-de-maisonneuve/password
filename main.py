#---------------------- Import----------------------#

import hashlib
import json
import string
import random

#---------------------- Fonctions ----------------------#

### Fonction pour vérifier la validité du mot de passe
def verif_pwd(mot_de_passe):
    longueur = len(mot_de_passe) >= 8
    majuscule = any(c.isupper() for c in mot_de_passe)
    minuscule = any(c.islower() for c in mot_de_passe)
    chiffre = any(c.isdigit() for c in mot_de_passe)
    special = any(c in "!@#$%^&*" for c in mot_de_passe)

    return longueur and majuscule and minuscule and chiffre and special

### Fonction pour hasher le mot de passe
def hash_pwd(mot_de_passe):
    return hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()

### Fonction pour charger les mots de passe depuis le fichier
def charger_mots_de_passe():
    try:
        with open("password.json", "r") as fichier:
            return json.load(fichier)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

### Fonction pour ajouter un mot de passe à la liste
def add_pwd(mot_de_passe, hashed_pwd, li_passe):
    li_passe.append({
        'password': mot_de_passe,
        'hashed_password': hashed_pwd
    })

### Sauvegarder la liste des mots de passe dans le fichier
    with open("password.json", "w") as fichier:
        json.dump(li_passe, fichier)

### Fonction pour afficher les mots de passe
def afficher_pwd(mots_de_passe):
    print("Mots de passe enregistrés :\n")
    for i, j in enumerate(mots_de_passe, 1):
        print(f"{i}. Hash: {j['hashed_password']} | Password: {j['password']}")

### Fonction pour générer un mot de passe aléatoire
def random_pwd():
    special_characters = "!@#$%^&*"
    new_pwd = ''
    while not verif_pwd(new_pwd):
        new_pwd = ''.join(random.choice(string.ascii_letters + string.digits + special_characters)
        for a in range(random.randint(8, 14)))
    print(f"Le mot de passe généré est : {new_pwd}")
    return new_pwd

#---------------------- Fonction principale ----------------------#

def create_pwd():
    mots_de_passe = charger_mots_de_passe()

    while True:
        print("""
              |----------------------------------------------------|
              |  Entrez '1' pour ajouter un nouveau mot de passe   |
              |  Entrez '2' pour générer un mot de passe aléatoire |
              |  Entrez '3' pour afficher les mots de passe        |
              |  Entrez '4' pour quitter le script                 |
              |----------------------------------------------------|""")

        choix = input("""
                Choisissez une option (1/2/3/4)
                      
                ==> """)

        if choix == "1":
            new_pwd = input("""
               > Entrez un nouveau mot de passe
               > Il doit contenir au minimum une majuscule, une minuscule
               > Un caractère spécial (!, @, #, $, %, ^, &, *)
               > Il doit faire un minimum de 8 caractères
                
                ==> """)
            hashed_pwd = hash_pwd(new_pwd)
            if hashed_pwd not in [j['hashed_password'] for j in mots_de_passe]:
                add_pwd(new_pwd, hashed_pwd, mots_de_passe)
                print ("""
                       Le mot de passe à été créé avec succès !
                       
                       Fermeture du programme
                       """)
                break
            else:
                print("Le mot de passe existe déjà dans la base de données.")
        elif choix == "2":
            new_pwd = random_pwd()
            hashed_pwd = hash_pwd(new_pwd)
            if hashed_pwd not in [j['hashed_password'] for j in mots_de_passe]:
                add_pwd(new_pwd, hashed_pwd, mots_de_passe)

        elif choix == "3":
            afficher_pwd(mots_de_passe)
        elif choix == "4":
            print("""           Programme terminé.
                  """)
            break
        else:
            print("Option invalide. Veuillez réessayer.")

create_pwd()
