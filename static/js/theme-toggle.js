if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
var themeToggleText = document.getElementById('theme-toggle-text'); // Récupère l'élément texte

// Change les icônes et le texte en fonction des paramètres précédents
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    themeToggleLightIcon.classList.remove('hidden');
    themeToggleText.textContent = 'Light'; // Affiche 'Light' lorsque le thème sombre est actif
} else {
    themeToggleDarkIcon.classList.remove('hidden');
    themeToggleText.textContent = 'Dark'; // Affiche 'Dark' lorsque le thème clair est actif
}

var themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function() {
    // Toggle les icônes et le texte
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // Change le texte en fonction de l'état du thème
    if (document.documentElement.classList.contains('dark')) {
        themeToggleText.textContent = 'Light'; // Affiche 'Light' quand le thème sombre est activé
    } else {
        themeToggleText.textContent = 'Dark'; // Affiche 'Dark' quand le thème clair est activé
    }

    // Si défini via localStorage précédemment
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }
    } else {
        // Si non défini dans le localStorage précédemment
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
});
