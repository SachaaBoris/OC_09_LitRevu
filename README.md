# OC_09 LitRevu    
  
# ● Description du projet  
WebApp django permettant de donner son avis ou de demander un avis sur un livre.
  
# ● Comment installer et démarrer l'application  
1. Prérequis :  
    Avoir Python 3 installé  
    Avoir téléchargé et installé l'API :  
    git clone https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR "local\folder"  
    Avoir téléchargé et dézipé l'archive du projet sur votre disque dur,  
    Ou clonez le repo avec cette commande :  
  ```  
  git clone https://github.com/SachaaBoris/OC_09_LitRevu.git "local\folder"  
  ```  
  
2. Installer l'environnement virtuel :  
    Depuis votre console favorite, naviguez jusqu'au repertoire du script  
    Pour créer l'environnement virtuel rentrez la ligne de commande : `py -m venv ./venv`  
    Activez ensuite l'environnement virtuel en rentrant la commande : `venv\Scripts\activate`  
    Installer les requirements du projet avec la commande : `py -m pip install -r requirements.txt`   
  
3. Démarrer le serveur :  
    Toujours dans la console et à la racine du script, tapez la commande : `py LitRevu/manage.py runserver`  
	Rendez-vous dans votre navigateur et allez à l'adresse :  
	http://127.0.0.1:8000 ou http://localhost:8000/  
	
	Vous pouvez désormais créer un compte et utiliser l'application.  
	Cinq comptes demo sont fournis :  
	| UserID | Password |
	| :---: | :---: |
	| Toto | igotapass24 |
	| Michel56 | igotapass23 |
	| Starlette | igotapass22 |
	| Darkdev | igotapass21 |
	| Maïté | igotapass20 |
	| Sarma | igotapass19 |
	| Administrator | 123456789 |
	
	Par defaut, ces comptes sont abonnés et peuvent voir les publications de :  
	|   | Toto | Michel56 | Starlette | Darkdev | Maïté | Sarma | Administrator |
	| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
	| Toto | X |  |  |  |  | X |  |
	| Michel56 | X | X | X | X | X | X |  |
	| Starlette | X | X |  |  |  | X |  |
	| Darkdev | X | X | X | X |  | X |  |
	| Maïté |  |  | X |  | X | X |  |
	| Sarma |  |  |  |  |  | X |  |
	| Administrator | X | X | X | X | X | X | X |  
  
---  
  
[![CC BY 4.0][cc-by-shield]][cc-by]  
  
This work is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].  
  
[cc-by]: http://creativecommons.org/licenses/by/4.0/  
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg  
