let lastScrollY = window.scrollY;
const navbar = document.getElementById("main-navbar");

window.addEventListener("scroll", () => {
if (window.scrollY > 150) {
    navbar.classList.add("translate-y-[-100%]"); // cache vers le haut
} else {
    navbar.classList.remove("translate-y-[-100%]");
}
});
