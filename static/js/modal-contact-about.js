document.getElementById('openContactModal').onclick = function() {
    document.getElementById('contactModal').classList.remove('hidden');
};
// Ferme le modal
document.getElementById('closeContactModal').onclick = function() {
    document.getElementById('contactModal').classList.add('hidden');
};
// Ferme le modal si on clique en dehors du contenu
document.getElementById('contactModal').onclick = function(e) {
    if (e.target === this) {
        this.classList.add('hidden');
    }
};