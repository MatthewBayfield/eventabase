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

/** Adds mousenter and mouseleave event listeners to the
 * more menu items to provide hover feedback. Feedback
 * entails a background colour change.
 * @summary Adds event listeners to the more menu items
 */
function menuItemHoverFeedbackListeners() {
    const menuItems = document.getElementsByClassName('menu_item');
    for (item of menuItems) {
        item.addEventListener('mouseenter', () => {
            item.classList.add('active');
        })
        item.addEventListener('mouseleave', () => {
            item.classList.remove('active');
        })
    }
}

menuItemHoverFeedbackListeners();

/** Adds click event listeners to certain elements to provide clicked/pressed feedback. Feedback
 * entails a temporary background and font colour change.
 * @summary Adds click event listeners to chosen elements to provide clicked feedback.
 */
 function clickedFeedbackListeners() {
    const menuItems = document.getElementsByClassName('menu_item');
    for (item of menuItems) {
        item.addEventListener('mousedown', () => {
            item.classList.add('clicked');
        })
        item.addEventListener('mouseup', () => {
            item.classList.remove('clicked');
        })
    }
}

clickedFeedbackListeners();

/** Adds the current_image class atrribute to the nextImage parameter element.
 * Passes the currentImage parameter to the imageFadeOut function.
 * @param {Object} currentImage - The image element with the current_image class attribute
 * @param {Object} nextImage - The image element to feature next in the slideshow
 * @summary Fades in the next slideshow image due to be displayed.
*/
function imageFadeIn(nextImage, currentImage) {
    nextImage.className += " current_image"
    imageFadeOut(currentImage);
}

/** Removes the current_image class attribute from the currentImage parameter element.
 *  Queues a recursive call to the slideshowHandler function to continue the slideshow
 *  operation.
 * @param {Object} currentImage - The image element to be faded out, as passed from the imageFadeOut function.
 * @summary Fades out the currently displayed image.
 */
function imageFadeOut(currentImage) {
    currentImage.classList.remove('current_image');
    setTimeout(slideshowHandler, 8000);
}


/** Determines the currently displayed image, and the image due to be displayed next. Passes
 *  these image vars on to the imageFadeOut function.
 * @summary Operates the image slideshow. 
 */
function slideshowHandler() {
    const slideshowImages = [...document.getElementsByClassName('slideshow_images')];
    // current_image class image elements have opacity of 1, slideshow image elements have default opacity 0
    let currentImage = document.getElementsByClassName('current_image')[0];
    let currentImageIndex = slideshowImages.indexOf(currentImage);
    let nextImage;
    if (currentImageIndex === slideshowImages.length - 1) {
        nextImage = slideshowImages[0];
    } else {
        nextImage = slideshowImages[currentImageIndex + 1]
    }
    imageFadeIn(nextImage, currentImage);
}

if (document.getElementsByTagName('title')[0].textContent === 'Landing page') {
    // Initial delay so that initally displayed image does not fade out immediately
    setTimeout(slideshowHandler, 8000);
}

// uncommented during testing
//module.exports = {moreMenu, moreMenuContainer, moreMenuButtons, openMenu, closeMenu, imageFadeIn, imageFadeOut};