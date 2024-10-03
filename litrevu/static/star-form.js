// Récupérer tous les boutons radio
const radios = document.querySelectorAll('.radio-btns');
const starContainer = document.querySelector('.radioboutons-below');
const starFullURL = starContainer.dataset.starFull;
const starEmptyURL = starContainer.dataset.starEmpty;

// Ajouter un écouteur d'événements à chaque bouton radio
radios.forEach(radio => {
    radio.addEventListener('change', function() {
        const ratingValue = parseInt(this.value);  // Valeur du bouton radio sélectionné

        // Boucle pour mettre à jour les étoiles
        for (let i = 1; i <= 5; i++) {
            const star = document.getElementById(`id_star_${i}`);
            if (i <= ratingValue) {
                star.src = starFullURL;  // Etoile pleine
            } else {
                star.src = starEmptyURL; // Etoile vide
            }
        }
    });
});