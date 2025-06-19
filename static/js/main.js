const profileMenu = document.getElementById('profile-menu');
const navMenu = document.getElementById('nav-mobile');
const profileBtn = document.querySelector('.profile-mobile-btn');
const navBtn = document.querySelector('.nav-mobile-btn');

function showProfileMenu() {
    profileMenu.classList.toggle('visible');
    navMenu.classList.remove('visible');
}

function showNavMenu() {
    navMenu.classList.toggle('visible');
    profileMenu.classList.remove('visible');
}

document.addEventListener('click', function(e) {
    if (!profileMenu.contains(e.target) && !profileBtn.contains(e.target)) {
        profileMenu.classList.remove('visible');
    }
    if (!navMenu.contains(e.target) && !navBtn.contains(e.target)) {
        navMenu.classList.remove('visible');
    }
});