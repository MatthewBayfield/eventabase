// JS Section: DOM element constants:

const moreMenuContainer = document.getElementById('more_menu_container');
const moreMenu = document.getElementById('more_menu');
const moreMenuButtons = document.getElementsByClassName('more_menu_button');

// JS Section: Event listeners:

/** Creates click event listeners for the 'more menu' hamburger button, and the 'more menu'
 * close button. Event handlers essentially close or open the menu.
 */
function createMoreMenuButtonsListeners() {
    for (let button of moreMenuButtons) {
        button.addEventListener('click', function() {
            let moreMenuContainerStyles = window.getComputedStyle(moreMenuContainer);
            let moreMenuContainerDisplay = moreMenuContainerStyles.getPropertyValue('display');
            if (moreMenuContainerDisplay === 'none') {
                openMenu();
            } else {
                closeMenu();
            }
        })
    }
}

createMoreMenuButtonsListeners();

/** Adds a click event listener to the more menu background container
 * element. Alows the more menu to be closed when clicking anywhere
 * not on it. 
 */
function createMoreMenuContainerListener() {
    moreMenuContainer.addEventListener('click', function(event) {
        let moreMenuContainerStyles = window.getComputedStyle(moreMenuContainer);
        let moreMenuContainerDisplay = moreMenuContainerStyles.getPropertyValue('display');
        if (moreMenuContainerDisplay != 'none') {
            if (event.target === moreMenuContainer) {
                closeMenu();
            }
        }
    })
}

createMoreMenuContainerListener();

// JS Section: Functions:

/** An event handler that performs the DOM manipulations necessary
 *  to open the more menu, when the more menu hamburger button is
 *  clicked.
 */
function openMenu() {
    moreMenuContainer.style.display = 'block';
    moreMenu.style.visibility = 'visible';
    moreMenu.focus();
    moreMenuButtons[0].setAttribute('aria-expanded', 'True');
}

/** An event handler that performs the DOM manipulations necessary
 *  to close the more menu, when the more menu close button is
 *  clicked, or anywhere not on the menu is clicked.
 */
function closeMenu() {
    moreMenu.style.removeProperty('visibility');
    moreMenuButtons[0].setAttribute('aria-expanded', 'False');
    moreMenuContainer.style.removeProperty('display');
    moreMenu.blur();   
}

// uncommented during testing
//module.exports = {moreMenu, moreMenuContainer, moreMenuButtons, openMenu, closeMenu};
