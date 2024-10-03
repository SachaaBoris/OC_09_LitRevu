document.getElementById('image-input').addEventListener('change', function(event) {
    const file = event.target.files[0]; // Obtenir le fichier sélectionné
    const preview = document.getElementById('image-preview'); // L'élément image de prévisualisation
    
    if (file) {
        const reader = new FileReader(); // Créer un FileReader pour lire le fichier
        
        // Lorsque le fichier est chargé, définir la source de l'image sur l'URL locale
        reader.onload = function(e) {
            preview.src = e.target.result; // Définir l'URL locale de l'image
            preview.style.display = 'block'; // Rendre l'image visible
        };
        
        reader.readAsDataURL(file); // Lire le fichier sélectionné en tant qu'URL de données
    } else {
        preview.src = ''; // Effacer la prévisualisation si aucun fichier n'est sélectionné
        preview.style.display = 'none'; // Cacher l'élément image
    }
});