# OC_09 LitRevu :notebook:   
  
# ● Description du projet  
WebApp django permettant à une communauté d'utilisateurs de donner son avis ou de demander un avis sur un livre. Elle intégre un système d'authentification, d'actualitées et d'abonnements.  
  
<details>
  <summary>Screen previews</summary>
  :camera:
	<details>
		<summary>Log In</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 01 - Log in.png" alt="Log In preview"/>
	</details>
	<details>
		<summary>Sign Up</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 02 - Sign Up.png" alt="Sign Up preview"/>
	</details>
	<details>
		<summary>Feed</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 03 - Feed.png" alt="Feed preview"/>
	</details>
	<details>
		<summary>Create Ticket</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 04 - Create Ticket.png" alt="Create Ticket preview"/>
	</details>
	<details>
		<summary>Create Ticket & Review</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 05 - Create Ticket and Review.png" alt="Create Ticket & Review preview"/>
	</details>
	<details>
		<summary>Submit Review</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 06 - Create Review.png" alt="Submit Review preview"/>
	</details>
	<details>
		<summary>Posts</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 07 - Posts.png" alt="Posts preview"/>
	</details>
	<details>
		<summary>Subscriptions</summary>
			<img src="https://github.com/SachaaBoris/OC_09_LitRevu/blob/main/previews/LITRevu 08 - Abonnements.png" alt="Subscriptions preview"/>
	</details>
</details>

  
# ● Comment installer et démarrer l'application  
1. Prérequis :  
    Avoir Python 3 installé  
    Avoir téléchargé et dézipé l'archive du projet sur votre disque dur,  
    Ou clonez le repo avec cette commande :  
  ```  
  git clone https://github.com/SachaaBoris/OC_09_LitRevu.git "local\folder"
  ```  
  
2. Générer et utiliser une clé secrète Django :  
	Rendez-vous sur https://djecrety.ir/ et générez une clé que vous pourrez coller dans le fichier .env.sample situé à la racine du projet.  
	Rennomez .env.sample en .env  
  
3. Installer l'environnement virtuel :  
    Depuis votre console favorite, naviguez jusqu'au répertoire du projet  
    Pour créer l'environnement virtuel rentrez la ligne de commande : `py -m venv ./venv`  
    Activez ensuite l'environnement virtuel en rentrant la commande : `venv\Scripts\activate`  
    Installer les requirements du projet avec la commande : `py -m pip install -r requirements.txt`  
  
4. Démarrer le serveur :  
    Toujours dans la console et à la racine du projet, tapez la commande : `py litrevu/manage.py runserver`  
	Rendez-vous dans votre navigateur et allez à l'adresse :  
	http://127.0.0.1:8000 ou http://localhost:8000/  
  
:black_circle:  
  
Vous pouvez désormais créer un compte et utiliser l'application.  
  
Sept comptes demo sont fournis :  
| UserID | Password |
| :---: | :---: |
| Toto | igotapass24 |
| Michel56 | igotapass23 |
| Starlette | igotapass22 |
| Darkdev | igotapass21 |
| Maïté | igotapass20 |
| Sarma | igotapass19 |
| Administrator | 123456789 |
  
:black_circle:  
  
Par defaut, ces comptes sont abonnés a et peuvent voir les publications de :  
|   | Toto | Michel56 | Starlette | Darkdev | Maïté | Sarma | Administrator |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Toto | X |  |  |  |  | X |  |
| Michel56 | X | X | X | X | X | X |  |
| Starlette | X | X | X |  |  | X |  |
| Darkdev | X | X | X | X |  | X |  |
| Maïté |  |  | X |  | X | X |  |
| Sarma |  |  |  |  |  | X |  |
| Administrator | X | X | X | X | X | X | X |  
  
:black_circle:  
  
Permissions par défaut :  
| User | Can follow / unfollow other users | Can Post Reviews and Tickets | Can update own posts | Can delete own posts | Can delete others posts | Can delete Users |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| CustomUser | X | X | X | X |  |  |
| Administrator |  |  |  |  | X | X |  
  
:black_circle:  
  
# ● Etapes supplémentaires facultatives  
5. Démarrer une nouvelle BDD :  
	Quittez le serveur (CTRL+C dans la console) si vous l'avez lancé et supprimez le fichier db.sqlite3  
	Vous pouvez également supprimer les images des anciens tickets du dossier media/tickets
	Et rentrer les commandes suivantes pour créer une nouvelle BDD
  ``` 
  py litrevu/manage.py makemigrations
  py litrevu/manage.py migrate
  ``` 
  
6. Créer un SuperUser :  
	Rentrez la commande suivante et suivez les instructions  
  ``` 
	py litrevu/manage.py createsuperuser
  ```  
  
7. Noubliez pas de switcher ces variables dans les settings du projet avant mise en production :  
	DEBUG = False  
	CSRF_COOKIE_SECURE = True  
	SESSION_COOKIE_SECURE = True  
  
:black_circle:  
  
---  
  
[![CC BY 4.0][cc-by-shield]][cc-by]  
  
This work is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].  
  
[cc-by]: http://creativecommons.org/licenses/by/4.0/  
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg  
