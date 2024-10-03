// Récupérer tous les boutons radio
const radios = document.querySelectorAll('.radio-btns');
const starContainer = document.querySelector('.radioboutons-below');
const starFullURL = starContainer.dataset.starFull;
const starEmptyURL = starContainer.dataset.starEmpty;

// Fonction pour mettre à jour les étoiles en fonction de la note sélectionnée
function updateStars(ratingValue) {
    for (let i = 1; i <= 5; i++) {
        const star = document.getElementById(`id_star_${i}`);
        if (i <= ratingValue) {
            star.src = starFullURL;  // Etoile pleine
        } else {
            star.src = starEmptyURL; // Etoile vide
        }
    }
}

// Initialisation au chargement de la page
radios.forEach(radio => {
    if (radio.checked) {
        updateStars(parseInt(radio.value));  // Afficher les étoiles correspondant à la valeur par defaut
    }
	
	// Écouteur d'événements au changement de valeur
	radio.addEventListener('change', function() {
        const ratingValue = parseInt(this.value);  // Valeur du bouton radio sélectionné
        updateStars(ratingValue);  // Mettre à jour les étoiles
    });
	
    // Écouteur d'événements pour l'agrandissement de l'étoile au survol
    radio.addEventListener('mouseenter', function() {
        const starId = this.value; // Obtenir la valeur de l'étoile correspondante
        const star = document.getElementById(`id_star_${starId}`);
        star.style.transform = 'scale(1.2)';  // Agrandir l'étoile
    });

    // Écouteur d'événements pour remettre à la taille normale après le survol
    radio.addEventListener('mouseleave', function() {
        const starId = this.value; // Obtenir la valeur de l'étoile correspondante
        const star = document.getElementById(`id_star_${starId}`);
        star.style.transform = 'scale(1)';  // Rétablir la taille normale
    });
});