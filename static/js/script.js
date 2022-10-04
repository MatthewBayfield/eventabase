// JS Section: DOM element constants:

const moreMenuContainer = document.getElementById('more_menu_container');
const moreMenu = document.getElementById('more_menu');
const moreMenuButtons = document.getElementsByClassName('more_menu_button');
const menuItems = document.getElementsByClassName('menu_item');
const slideshowImages = [...document.getElementsByClassName('slideshow_images')];
const linksAndButtons = [...document.getElementsByTagName('a'), ...document.getElementsByTagName('button')];
const focusable = [...linksAndButtons, ...document.querySelectorAll('[tabIndex="0"]')];
const uniqueFocusable = [...new Set(focusable)];
const helpTextIcons = [...document.querySelectorAll('[data-icon-type = "help"]')];
const helpText = [...document.getElementsByClassName('help_text')];
const matchingIcons = [...document.getElementsByClassName('matching_icon')];

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

/** Adds mousenter and mouseleave event listeners to the
 * more menu items to provide hover feedback. Feedback
 * entails a background colour change.
 * @summary Adds event listeners to the more menu items
 */
 function menuItemHoverFeedbackListeners() {
    for (let item of menuItems) {
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
    for (let element of [...new Set([...menuItems, ...uniqueFocusable])]) {
        element.addEventListener('mousedown', () => {
            element.classList.add('clicked');
        })
        element.addEventListener('mouseup', () => {
            setTimeout(() => element.classList.remove('clicked'), 100);
        })
    }
}

clickedFeedbackListeners();

/** Adds enter key press event listeners to focusable elements, to allow
 * clicking of the element with the enter key. Also provides feedback
 * when pressed.
 * @summary Adds enter key click equivalent event listeners to focusable elements.
 */
 function enterKeyListeners() {
    for (let element of uniqueFocusable) {
        element.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                element.classList.add('clicked');
            }

        })
        element.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                element.classList.remove('clicked');
                element.click();
            }
        })
    }
}

enterKeyListeners();

// JS Subsection: form related event listeners 

/** Adds mouseenter and mouseleave event listeners to 'help icon' elements, to
 * alter the visibility of the field help text.
 * @summary Adds mouse event listeners to 'help icon' elements to display related field help text.
 */
function helpTextIconsListeners() {
    for (let helpIcon of helpTextIcons) {
        helpIcon.addEventListener('mouseenter', () => {
            let helpTextIndex = helpTextIcons.indexOf(helpIcon);
            helpText[helpTextIndex].style.display = 'block';
            helpIcon.style.setProperty('align-self', 'start');
        })

        helpIcon.addEventListener('mouseleave', () => {
            let helpTextIndex = helpTextIcons.indexOf(helpIcon);
            helpText[helpTextIndex].removeAttribute('style');
            helpIcon.removeAttribute('style');
        })

        // touchstart event listeners to trigger the same effects as the above mouseenter and mouseleave event listeners for touchscreens
        helpIcon.addEventListener('touchstart', (event) => {
            event.preventDefault();
            let helpTextIndex = helpTextIcons.indexOf(helpIcon);
            if (window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display') === 'none') {
                helpIcon.style.setProperty('align-self', 'start');
                helpText[helpTextIndex].style.display = 'block';
                setTimeout(() => {
                    helpText[helpTextIndex].removeAttribute('style');
                    helpIcon.removeAttribute('style');
                }, 8000)
            }
        })

    }
}

helpTextIconsListeners();

/** Adds keyup event listeners to a pair of related input fields, with one having a matching/no_match icon indicator.
 *  After a keyup event in either field (indicating a change to its input value), the input values of both
 * fields are compared and the display of the indicator icons altered using the compareFields handler.
 * @summary Adds keyup event listeners to a pair of typed/retyped input fields.
 */
function formFieldChangeListeners() {
    for (let matchingIcon of matchingIcons) {
        let noMatchIcon = matchingIcon.nextElementSibling;
        let secondField = matchingIcon.parentElement.firstElementChild.children[1];
        let firstField = matchingIcon.parentElement.previousElementSibling.firstElementChild.children[1];
        let fields = [firstField, secondField];
        let icons = [matchingIcon, noMatchIcon];
        for (let field of fields) {
            field.addEventListener('keyup', () => {
                compareFields(fields, icons);
            })
        }
    }
}

formFieldChangeListeners();

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

/** An event handler thar compares the values of two input text fields
 * and then conditionally changes the display of the matching
 * and no-match field icons.
 * @param {array} fields - The two fields whose values to compare.
 * @param {array} icons - The matching and no-match icons.
 */
function compareFields(fields, icons) {
    let [field1, field2] = fields;
    let [matchingIcon, noMatchIcon] = icons;
    if (field1.value !== field2.value) {
            matchingIcon.style.display = 'none';
            noMatchIcon.style.display = 'inline';
    } else {
        if (window.getComputedStyle(matchingIcon).getPropertyValue('display') === 'none') {
            matchingIcon.removeAttribute('style');
            noMatchIcon.removeAttribute('style');
        }
    }
}

/** Adds the current_image class atrribute to the nextImage parameter element.
 * Passes the currentImage parameter to the imageFadeOut function.
 * @param {Object} currentImage - The image element with the current_image class attribute
 * @param {Object} nextImage - The image element to feature next in the slideshow
 * @summary Fades in the next slideshow image due to be displayed.
*/
function imageFadeIn(nextImage, currentImage) {
    nextImage.className += " current_image"
    imageFadeOut(currentImage);
    nextImage.setAttribute('aria-hidden', 'false');
}

/** Removes the current_image class attribute from the currentImage parameter element.
 *  Queues a recursive call to the slideshowHandler function to continue the slideshow
 *  operation.
 * @param {Object} currentImage - The image element to be faded out, as passed from the imageFadeOut function.
 * @summary Fades out the currently displayed image.
 */
function imageFadeOut(currentImage) {
    currentImage.setAttribute('aria-hidden', 'true');
    currentImage.classList.remove('current_image');
    setTimeout(slideshowHandler, 8000);
}

/** Determines the currently displayed image, and the image due to be displayed next. Passes
 *  these image vars on to the imageFadeOut function.
 * @summary Operates the image slideshow. 
 */
function slideshowHandler() {
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
// module.exports = {
//     moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable,
//     slideshowImages, openMenu, closeMenu, imageFadeIn, imageFadeOut, helpTextIcons,
//     helpText, matchingIcons
// };