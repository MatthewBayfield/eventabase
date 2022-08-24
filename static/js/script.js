// JS Section: DOM element constants:

const moreMenuContainer = document.getElementById('more_menu_container');
const moreMenu = document.getElementById('more_menu');
const moreMenuButtons = document.getElementsByClassName('more_menu_button');

// JS Section: Functions:

function openMenu() {
    moreMenuContainer.style.display = 'block';
    moreMenu.style.visibility = 'visible';
    moreMenu.focus();
    moreMenuButtons[0].setAttribute('aria-expanded', 'True');
}

function closeMenu() {
    moreMenu.style.removeProperty('visibility');
    moreMenuButtons[0].setAttribute('aria-expanded', 'False');
    moreMenuContainer.style.removeProperty('display');
    moreMenu.blur();   
}
