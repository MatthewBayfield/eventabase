// JS Section: DOM element effective constants:

// defined with let to allow re-application of event listeners to updated dom elements
let moreMenuContainer = document.getElementById('more_menu_container');
let moreMenu = document.getElementById('more_menu');
let moreMenuButtons = document.getElementsByClassName('more_menu_button');
let menuItems = document.getElementsByClassName('menu_item');
let signupButton = document.querySelector("[name = 'sign-up']");
let signinButton = document.querySelector("[name = 'sign-in']");
let slideshowImages = [...document.getElementsByClassName('slideshow_images')];
let linksAndButtons = [...document.getElementsByTagName('a'), ...document.getElementsByTagName('button')];
let focusable = [...linksAndButtons, ...document.querySelectorAll('[tabindex="0"]')];
let uniqueFocusable = [...new Set(focusable)];
let helpTextIcons = [...document.querySelectorAll('[data-icon-type = "help"]')];
let helpText = [...document.getElementsByClassName('help_text')];
let matchingIcons = [...document.getElementsByClassName('matching_icon')];
let expandIcons = [...document.querySelectorAll('[data-icon-type ^= "expand"]')];
let modalContainers = [...document.getElementsByClassName('modal_container')];
let modals = [...document.getElementsByClassName('modal')]
let closeModalButtons = [...document.getElementsByClassName('close_button')];
let editPersonalInfoForm = document.getElementById('personal_info_form');
let editAddressForm = document.getElementById('address_form');
let editProfileModal = document.getElementById('edit_profile_modal');
let editProfileModalDoneButton = editProfileModal ? editProfileModal.lastElementChild.children[0] : null;
let modalButtons = [...document.getElementsByClassName('modal_button')];
let openModalButtons = [...document.getElementsByClassName('open_modal_button')];
let postEventModal = document.getElementById('post_events_modal');
let postEventForm = document.getElementById('post_events_form');
let postEventFormDoneButton = document.getElementById('post_events_modal') ? document.getElementById('post_events_modal').querySelector('.modal_button').children[0] : null;
let advertisedEvents = [...document.getElementsByClassName('advertised')];
let upcomingEvents = [...document.getElementsByClassName('upcoming')];
let radioInputs = [...document.querySelectorAll("[type = 'radio']")];

// JS Section: Event listeners:

/** Creates click event listeners for the 'more menu' hamburger button, and the 'more menu'
 * close button. Event handler essentially closes or opens the menu.
 */
function createMoreMenuButtonsListeners() {
    for (let button of moreMenuButtons) {
        // prevent listener duplication
        button.removeEventListener('click', moreMenuButtonEventHandler);
        button.addEventListener('click', moreMenuButtonEventHandler);
    }
}

/** Adds a click event listener to the more menu background container
 * element. Alows the more menu to be closed when clicking anywhere
 * not on it. 
 */
function createMoreMenuContainerListener() {
    moreMenuContainer.removeEventListener('click', moreMenuContainerEventHandler);
    moreMenuContainer.addEventListener('click', moreMenuContainerEventHandler);
}

/** Adds mousenter and mouseleave event listeners to the
 * more menu items to provide hover feedback. Feedback
 * entails a background colour change.
 * @summary Adds event listeners to the more menu items.
 */
 function menuItemHoverFeedbackListeners() {
    // remove existing listeners to prevent duplication
    for (let item of menuItems) {
        item.removeEventListener('mouseenter', menuItemHoverFeedbackMouseenter);
        item.removeEventListener('mouseleave', menuItemHoverFeedbackMouseleave);
    }
    // add new listeners
    for (let item of menuItems) {
        item.addEventListener('mouseenter', menuItemHoverFeedbackMouseenter); 
        item.addEventListener('mouseleave', menuItemHoverFeedbackMouseleave);
    }
}

/** Adds click event listeners to certain elements to provide clicked/pressed feedback. Feedback
 * entails a temporary background and font colour change.
 * @summary Adds click event listeners to chosen elements to provide clicked feedback.
 */
 function clickedFeedbackListeners() {
    // remove exisitng listeners to prevent duplication
    for (let element of [...new Set([...menuItems, ...uniqueFocusable])]) {
        element.removeEventListener('mousedown', clickedFeedbackMousedown);
        element.removeEventListener('mouseup', clickedFeedbackMouseup);
    }
    // add new listeners
    for (let element of [...new Set([...menuItems, ...uniqueFocusable])]) {
        element.addEventListener('mousedown', clickedFeedbackMousedown); 
        element.addEventListener('mouseup', clickedFeedbackMouseup); 
    }
}

/** Adds enter key press event listeners to focusable elements, to allow
 * clicking of the element with the enter key. Also provides feedback
 * when pressed.
 * @summary Adds enter key click equivalent event listeners to focusable elements.
 */
 function enterKeyListeners() {
    // remove exisitng listeners to prevent duplication
    for (let element of uniqueFocusable) {
        element.removeEventListener('keydown', enterKeyKeydown);
        element.removeEventListener('keyup', enterKeyKeyup);
    }
    // add new listeners
    for (let element of uniqueFocusable) {
        element.addEventListener('keydown', enterKeyKeydown);
        element.addEventListener('keyup', enterKeyKeyup); 
    }
}

/** Adds click event listener to the sign-up button on the
 * landing page. When clicked redirects the user to the
 * signup page.
 * @summary Adds click event listener to sign-up button. Redirects to signup page.
 */
function signupButtonEventListener() {
    // remove exisitng listeners to prevent duplication
    signupButton.removeEventListener('click', signupButtonHandler);
    // add new listeners
    signupButton.addEventListener('click', signupButtonHandler); 
}

/** Adds click event listener to the sign-in button on the
 * landing page. When clicked redirects the user to the
 * login page.
 * @summary Adds click event listener to sign-in button. Redirects to login page.
 */
 function signinButtonEventListener() {
    // remove exisitng listeners to prevent duplication
    signinButton.removeEventListener('click', signinButtonHandler);
    // add new listeners
    signinButton.addEventListener('click', signinButtonHandler); 
}

/** Adds click event Listeners to the expand more/less section icons.
 *  Provides the expand/contract functionality, and handles focus switching.
 * @summary Gives expand icons their functionality.
 */
function expandIconListeners() {
    // remove existing listeners to prevent duplication
    for (let icon of expandIcons) {
        icon.removeEventListener('click', expandIconHandler);
    }
    // add new listeners
    for (let icon of expandIcons) {
        icon.addEventListener('click', expandIconHandler)
    }
}

/** Adds a click event listener to all open modal buttons.
 * When clicked the matching modal is opened with focus, and the background
 * scrollbar is hidden.
 * @summary Gives the open modal buttons their button functionality.
 */
function openModalButtonListeners() {
    // remove existing listeners to prevent duplication
    for (let i=0; i < openModalButtons.length; i++) {
        openModalButtons[i].removeEventListener('click', openModalButtonHandler);
    }
    // add new listeners
    for (let i=0; i < openModalButtons.length; i++) {
        openModalButtons[i].addEventListener('click', openModalButtonHandler); 
    }
}


/** Adds input event listeners to the post
 * events section radio inputs to control
 * which type of events are displayed
 * @summary Adds radio input listeners to control which events are visible.
 */
function addRadioInputListeners() {
    // remove existing listeners to prevent duplication
    for (let input of radioInputs) {
        input.removeEventListener('change', radioInputHandler);
    }
    // add new listeners
    for (let input of radioInputs) {
        if (input.value === 'advertised') {
            input.click();
            updateVisibleEvents(input);
        }
        input.addEventListener('change', radioInputHandler);
    }
}

// JS Subsection: form related event listeners 

/** Adds mouseenter and mouseleave event listeners to 'help icon' elements, to
 * alter the visibility of the field help text.
 * @summary Adds mouse event listeners to 'help icon' elements to display related field help text.
 */
function helpTextIconsListeners() {
    // remove existing listeners to prevent duplication
    for (let helpIcon of helpTextIcons) {
        helpIcon.removeEventListener('mouseenter', helpTextIconsMouseenter);   
        helpIcon.removeEventListener('mouseleave', helpTextIconsMouseleave);  
        helpIcon.removeEventListener('touchstart', helpTextIconsTouchstart);
    }
    // add new listeners
    for (let helpIcon of helpTextIcons) {
        helpIcon.addEventListener('mouseenter', helpTextIconsMouseenter);
        helpIcon.addEventListener('mouseleave', helpTextIconsMouseleave); 

        // touchstart event listeners to trigger the same effects as the above mouseenter and mouseleave event listeners for touchscreens
        helpIcon.addEventListener('touchstart', helpTextIconsTouchstart);
    }
}

/** Adds input event listeners to a pair of related input fields, with one having a matching/no_match icon indicator.
 *  After an input event, the input values of both
 * fields are compared and the display of the indicator icons altered using the compareFields handler.
 * @summary Adds input event listeners to a pair of typed/retyped input fields.
 */
function formFieldChangeListeners() {
    // remove existing listeners to prevent duplication
    for (let matchingIcon of matchingIcons) {
        let noMatchIcon = matchingIcon.nextElementSibling;
        let secondField = matchingIcon.parentElement.firstElementChild.children[1];
        let firstField = matchingIcon.parentElement.previousElementSibling.firstElementChild.children[1];
        let fields = [firstField, secondField];
        let icons = [matchingIcon, noMatchIcon];
        for (let field of fields) {
            field.removeEventListener('input', formFieldChangeHandler);
        }
    }
    // add new event listeners
    for (let matchingIcon of matchingIcons) {
        let noMatchIcon = matchingIcon.nextElementSibling;
        let secondField = matchingIcon.parentElement.firstElementChild.children[1];
        let firstField = matchingIcon.parentElement.previousElementSibling.firstElementChild.children[1];
        let fields = [firstField, secondField];
        let icons = [matchingIcon, noMatchIcon];
        for (let field of fields) {
            field.addEventListener('input', formFieldChangeHandler); 
        }
    }
}

// JS Subsection: modal related event listeners:

/** Adds click event listeners to the close modal buttons, that
 * cause the related modal to be closed, and the focus returned
 * to the open modal button. The body scrollbar also becomes visible again.
 * @summary Gives the close modal buttons their button functionality.
 */
function closeModalButtonListeners() {
    for (let button of closeModalButtons) {
        button.firstElementChild.removeEventListener('click', closeModal);
        button.firstElementChild.removeEventListener('click', restoreForm);
        button.firstElementChild.addEventListener('click', closeModal);
        button.firstElementChild.addEventListener('click', restoreForm);
    }
}

/**
 * @summary Adds click listener to modal cancel buttons to close modals.
 */
function createModalCancelButtonListeners() {
    for (let button of modalButtons) {
        if (button.getAttribute('name') === 'Cancel') {
            button.removeEventListener('click', closeModal);
            button.removeEventListener('click', restoreForm);
            button.addEventListener('click', closeModal);
            button.addEventListener('click', restoreForm);
        }
    }
}

/** Adds blur event listener to the last button in a modal. Ensures focus remains on
 * elements within the modal, and cannot exit it by pressing the tab key.
 * @summary Creates event listeners that trap focus within an open modal.
 */
function trapFocusModalListeners() {
    // remove existing listeners to prevent duplication
    for (let modal of modals) {
        let modalId = modal.id;
        let querySelector = '#' + modalId + ' button';
        // The last modal button is its last focusable element.
        let lastButtonInModal = [...document.querySelectorAll(querySelector)].pop();
        lastButtonInModal.removeEventListener('blur', trapFocusModalBlur);
        let parentModalContainer = modal.parentElement
        parentModalContainer.removeEventListener('focus', trapFocusModalFocus);
    }
    // add new listeners
    for (let modal of modals) {
        let modalId = modal.id;
        let querySelector = '#' + modalId + ' button';
        // The last modal button is its last focusable element.
        let lastButtonInModal = [...document.querySelectorAll(querySelector)].pop();
        lastButtonInModal.addEventListener('blur', trapFocusModalBlur); 
        let parentModalContainer = modal.parentElement
        parentModalContainer.addEventListener('focus', trapFocusModalFocus);
    }
}

/** Adds click event listener to the edit profile modal done
 * button, to act as the form submission button.
 * @summary Click listener to submit form.
 */
function addEditProfileModalDonebuttonListeners() {
    editProfileModalDoneButton.removeEventListener('click', editProfileFormFetchHandler)
    editProfileModalDoneButton.addEventListener('click', editProfileFormFetchHandler)
}

// JS Section: Functions:

// hoisted event handlers

var clickedFeedbackMousedown = (event) => {
    let element = event.currentTarget;
    element.classList.add('clicked')
};
var clickedFeedbackMouseup = (event) => {
    let element = event.currentTarget
    setTimeout(() => element.classList.remove('clicked'), 100)
};
var enterKeyKeydown = (event) => {
    let element = event.currentTarget;
    if (event.key === 'Enter') {
        element.classList.add('clicked');
    }
};
var enterKeyKeyup = (event) => {
    let element = event.currentTarget;
    if (event.key === 'Enter') {
        element.classList.remove('clicked');
        element.click();
    }
};
var menuItemHoverFeedbackMouseenter = (event) => {
    let item = event.currentTarget;
    item.classList.add('active');
};
var menuItemHoverFeedbackMouseleave = (event) => {
    let item = event.currentTarget;
    item.classList.remove('active');
};
var expandIconHandler = (event) => {
    let icon = event.currentTarget;
    if (icon.getAttribute('data-icon-type') === 'expand_more') {
        icon.parentElement.parentElement.children[1].style.display = 'grid';
        icon.parentElement.parentElement.children[1].focus();
    }
    else {
        icon.parentElement.parentElement.children[1].removeAttribute('style');
    }
    if (icon.hasAttribute('style')) {
        icon.removeAttribute('style');
    }
    else {
        icon.style.display = 'none';
    }
    let siblingIcon = icon.nextElementSibling || icon.previousElementSibling;
    if (siblingIcon.hasAttribute('style')) {
        siblingIcon.removeAttribute('style');
    }
    else {
        siblingIcon.style.display = 'inline-block'
    }
};
var openModalButtonHandler = (event) => {
    let i = openModalButtons.indexOf(event.currentTarget);
    if (window.getComputedStyle(modalContainers[i]).getPropertyValue('display') === 'none') {
        modalContainers[i].style.display = 'block';
        modals[i].focus();
        document.body.style.overflowY = 'hidden';
    }
};
var radioInputHandler = (event) => {
    let input = event.currentTarget;
    updateVisibleEvents(input);
};
var helpTextIconsMouseenter = (event) => {
    let helpIcon = event.currentTarget;
    let helpTextIndex = helpTextIcons.indexOf(helpIcon);
    helpText[helpTextIndex].style.display = 'block';
};
var helpTextIconsMouseleave = (event) => {
    let helpIcon = event.currentTarget;
    let helpTextIndex = helpTextIcons.indexOf(helpIcon);
    helpText[helpTextIndex].removeAttribute('style');
};
var helpTextIconsTouchstart  = (event) => {
    let helpIcon = event.currentTarget;
    event.preventDefault();
    let helpTextIndex = helpTextIcons.indexOf(helpIcon);
    if (window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display') === 'none') {
        helpText[helpTextIndex].style.display = 'block';
        setTimeout(() => {
            helpText[helpTextIndex].removeAttribute('style');
        }, 8000)
    }
};
var formFieldChangeHandler = (event) => {
    let field = event.currentTarget;
    let matchingIcon;
    if (field.name.includes('2')) {
        matchingIcon = field.parentElement.nextElementSibling;
    }
    else {
        matchingIcon = field.parentElement.parentElement.nextElementSibling.children[1];
    }
    let noMatchIcon = matchingIcon.nextElementSibling;
    let secondField = matchingIcon.parentElement.firstElementChild.children[1];
    let firstField = matchingIcon.parentElement.previousElementSibling.firstElementChild.children[1];
    let fields = [firstField, secondField];
    let icons = [matchingIcon, noMatchIcon];
    compareFields(fields, icons);
};
var signupButtonHandler = () => {
    let current_location = window.location.href;
    let next_location = current_location + 'accounts/signup/';
    window.location.assign(next_location);
};
var signinButtonHandler = () => {
    let current_location = window.location.href;
    let next_location = current_location + 'accounts/login/';
    window.location.assign(next_location);
};
var trapFocusModalBlur = (event) => {
    let modal = event.currentTarget.parentElement.parentElement;
    modal.focus();
};
var trapFocusModalFocus  = (event) => {
    let modal = event.currentTarget.firstElementChild;
    modal.focus();
};

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

/** An event handler for the moreMenuButton click event listeners.
 * Opens and closes the more menu container.
 * @summary moreMenuButton event handler to open and close the more menu.
 */
function moreMenuButtonEventHandler() {
    let moreMenuContainerStyles = window.getComputedStyle(moreMenuContainer);
    let moreMenuContainerDisplay = moreMenuContainerStyles.getPropertyValue('display');
    if (moreMenuContainerDisplay === 'none') {
        openMenu();
    } else {
        closeMenu();
    }
}

/** Event handler for the more menu container click event listener.
 *  Clicking on the container outside of the more menu closes
 *  the menu.
 * @param {Object} event 
 * @summary moreMenuContainer click event handler that closes the more menu.
 */
function moreMenuContainerEventHandler(event) {
    let moreMenuContainerStyles = window.getComputedStyle(moreMenuContainer);
    let moreMenuContainerDisplay = moreMenuContainerStyles.getPropertyValue('display');
    if (moreMenuContainerDisplay != 'none') {
        if (event.target === moreMenuContainer) {
            closeMenu();
        }
    }
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

/** 
 * @param {Object} input - eiher a dispatched event or cancel/close button element.
 * @summary Event handler/function for closing a modal form.
 */
function closeModal(input) {
    let target;
    if (input.currentTarget) {
        target = input.currentTarget;
    }
    else {
        target = input;
    }
    
    let parentModalContainer;
    if (target.tagName === 'BUTTON') {
        parentModalContainer = target.parentElement.parentElement.parentElement;
    }
    else {
        parentModalContainer = target.parentElement.parentElement.parentElement.parentElement;
    }
            parentModalContainer.removeAttribute('style');
            document.body.removeAttribute('style');
            if (parentModalContainer.firstElementChild.id === 'edit_profile_modal') {
                openModalButtons[0].focus(); 
            }
            // if (parentModalContainer.firstElementChild.id === 'post_event_modal') {
            //     openModalButtons[0].focus(); 
            // }
}

/** Event handler for the radioInput event listeners.
 *  Alters whether advertised or upcoming events
 * are displayed in the post events section.
 * @summary event handler for radioInput listeners. Alters which events are displayed.
 */
function updateVisibleEvents(input) {
    if (input.value === 'advertised') {
        for (let eventContainer of advertisedEvents) {
            if (eventContainer.classList.contains('hidden')) {
                eventContainer.classList.remove('hidden');
            }
        }
        for (let eventContainer of upcomingEvents) {
            if (eventContainer.classList.contains('hidden')) {

            }
            else {
                eventContainer.classList.add('hidden');
            }
        }
    }
    else {
        for (let eventContainer of advertisedEvents) {
            if (eventContainer.classList.contains('hidden')) {

            }
            else {
                eventContainer.classList.add('hidden');
            }
        }
        for (let eventContainer of upcomingEvents) {
            if (eventContainer.classList.contains('hidden')) {
                eventContainer.classList.remove('hidden');
            }
        }
    }
}

/** Event handler that clears/restores modal forms
 * after close or cancel button click.
 *  @summary Event handler that clears/restores a modal form.
 * @param {Object} event - the dispatched event.
 */
function restoreForm(event) {
    let target = event.currentTarget;
    refreshFormFetchHandler(target);
}

/** Recreates all the event listeners
 * for shared elements across all pages.
 * Necessary when the DOM is dynamically
 * updated.
 * @summary Recreates event listeners shared across all pages.
 */
function executeAllPageAddListenerFunctions() {
    createMoreMenuButtonsListeners();
    createMoreMenuContainerListener();
    menuItemHoverFeedbackListeners();
    clickedFeedbackListeners();
    enterKeyListeners();
    expandIconListeners();
    helpTextIconsListeners();
    formFieldChangeListeners();
}

/**Recreates all the event listeners
 * for the HomePage.
 * Necessary when the DOM is dynamically
 * updated.
 * @summary Recreates event listeners for the HomePage.
 */
function executeAllHomePageAddListenersFunctions() {
    openModalButtonListeners();
    closeModalButtonListeners();
    trapFocusModalListeners();
    addEditProfileModalDonebuttonListeners();
    createModalCancelButtonListeners();
    addRadioInputListeners();
}

/**Recreates all the event listeners
 * for the LandingPage.
 * Necessary when the DOM is dynamically
 * updated.
 * @summary Recreates event listeners for the LandingPage.
 */
function executeAllLandingPageAddListenersFunctions() {
    signupButtonEventListener();
    signinButtonEventListener();
}

/**Recreates all DOM element variables.
 * Necessary when the DOM is dynamically
 * updated.
 * @summary Recreates all DOM element variables.
 */
function refreshDomElementVariables() {
    moreMenuContainer = document.getElementById('more_menu_container');
    moreMenu = document.getElementById('more_menu');
    moreMenuButtons = document.getElementsByClassName('more_menu_button');
    menuItems = document.getElementsByClassName('menu_item');
    signupButton = document.querySelector("[name = 'sign-up']");
    signinButton = document.querySelector("[name = 'sign-in']");
    slideshowImages = [...document.getElementsByClassName('slideshow_images')];
    linksAndButtons = [...document.getElementsByTagName('a'), ...document.getElementsByTagName('button')];
    focusable = [...linksAndButtons, ...document.querySelectorAll('[tabindex="0"]')];
    uniqueFocusable = [...new Set(focusable)];
    helpTextIcons = [...document.querySelectorAll('[data-icon-type = "help"]')];
    helpText = [...document.getElementsByClassName('help_text')];
    matchingIcons = [...document.getElementsByClassName('matching_icon')];
    expandIcons = [...document.querySelectorAll('[data-icon-type ^= "expand"]')];
    modalContainers = [...document.getElementsByClassName('modal_container')];
    modals = [...document.getElementsByClassName('modal')]
    closeModalButtons = [...document.getElementsByClassName('close_button')];
    editPersonalInfoForm = document.getElementById('personal_info_form');
    editAddressForm = document.getElementById('address_form');
    editProfileModal = document.getElementById('edit_profile_modal');
    editProfileModalDoneButton = editProfileModal ? editProfileModal.lastElementChild.children[0] : null;
    modalButtons = [...document.getElementsByClassName('modal_button')];
    openModalButtons = [...document.getElementsByClassName('open_modal_button')];
    postEventModal = document.getElementById('post_events_modal');
    postEventFormDoneButton = document.getElementById('post_events_modal') ? document.getElementById('post_events_modal').querySelector('.modal_button').children[0] : null;
    postEventForm = document.getElementById('post_events_form');
    advertisedEvents = [...document.getElementsByClassName('advertised')];
    upcomingEvents = [...document.getElementsByClassName('upcoming')];
    radioInputs = [...document.querySelectorAll("[type = 'radio']")];
}

// JS Subsection: Fetch requests:

/** Fetch POST request handler for submitting
 *  the edit profile form. Updates page
 *  when a valid form is submitted.
 * @summary Fetch POST request handler for edit profile form submission.
 */
 async function editProfileFormFetchHandler() {
    // form data for the first pair of requests
    let personalInfoFormData = new FormData(editPersonalInfoForm);
    personalInfoFormData.append('validate', 'true');
    let addressFormData = new FormData(editAddressForm);
    addressFormData.append('validate', 'true');
    let issue = false;
    try {
        // For aquiring the form csrf token
        const csrftoken = Cookies.get('csrftoken');
    
        // first two requests to check each form's validity
        let firstRequest = new Request('profile_form/',
                                    {method: 'POST', headers: {'X-CSRFToken': csrftoken},
                                    mode: 'same-origin',
                                    body: personalInfoFormData});
        let firstResponse = await fetch(firstRequest);
        let firstResponseJson = await firstResponse.json();

        let secondRequest = new Request('profile_form/',
                                        {method: 'POST', headers: {'X-CSRFToken': csrftoken},
                                        mode: 'same-origin',
                                        body: addressFormData});
        let secondResponse = await fetch(secondRequest);
        let secondResponseJson = await secondResponse.json();
        
        // If both forms are valid submit both forms again to be postprocessed and saved.
        // Update profile section.
        if (firstResponseJson.valid === 'true' && secondResponseJson.valid === 'true') {
            personalInfoFormData.set('validate', 'false');
            addressFormData.set('validate', 'false')
            let thirdRequest = new Request('profile_form/',
                                    {method: 'POST', headers: {'X-CSRFToken': csrftoken},
                                    mode: 'same-origin',
                                    body: personalInfoFormData});
            let thirdResponse = await fetch(thirdRequest);
            let thirdResponseJson = await thirdResponse.json();

            let fourthRequest = new Request('profile_form/',
                                        {method: 'POST', headers: {'X-CSRFToken': csrftoken},
                                        mode: 'same-origin',
                                        body: addressFormData});
            let fourthResponse = await fetch(fourthRequest);
            let fourthResponseJson = await fourthResponse.json();
            if (fourthResponseJson.hasOwnProperty('error')) {
                errMsg = `There was a problem processing your submitted address, please check that the address information you entered
    is valid and try again; If the address is valid, try another address; if the problem persists, try again later.`;
                alert(errMsg);
                issue = true;
            }
            editPersonalInfoForm.innerHTML = firstResponseJson.form;
            if (!issue) {
                editAddressForm.innerHTML = secondResponseJson.form;
                if (editProfileModal.firstElementChild.firstElementChild.hasAttribute('style')) {
                    editProfileModal.firstElementChild.firstElementChild.removeAttribute('style');
                }
                if (editProfileModal.lastElementChild.children.length < 2) {
                    let cancelButton = document.createElement('button');
                    editProfileModal.lastElementChild.appendChild(cancelButton);
                    cancelButton.outerHTML = '<button class="modal_button" type="button" name="Cancel">Cancel</button>'
                }
            }
            editProfileModal.parentElement.previousElementSibling.innerHTML = fourthResponseJson.profile;
            refreshDomElementVariables();
            executeAllPageAddListenerFunctions();
            executeAllHomePageAddListenersFunctions();
            if (!issue) {
                //close edit profile modal
                closeModal(editProfileModal.firstElementChild.firstElementChild.firstElementChild);
            }
            
        }
        
        // update 'edit profile modal' forms
        if (firstResponseJson.valid === 'false') {
            editPersonalInfoForm.innerHTML = firstResponseJson.form;
        }

        if (secondResponseJson.valid === 'false') {
            editAddressForm.innerHTML = secondResponseJson.form;
        }
        refreshDomElementVariables();
        executeAllPageAddListenerFunctions();
        executeAllHomePageAddListenersFunctions();
    }
    catch(error) {
        console.error(error);
    }
}

/** Fetch POST request handler for submitting
 *  the post event form. Updates page
 *  when a valid form is submitted.
 * @summary Fetch POST request handler for post events form submission.
 */
 async function postEventFormFetchHandler() {
    // form data for request
    let formData = new FormData(postEventForm);

    try {
        // For aquiring the form csrf token
        const csrftoken = Cookies.get('csrftoken');
    
        // make request to submit form and check response

        let request = new Request('post_events/',
                                    {method: 'POST', headers: {'X-CSRFToken': csrftoken},
                                    mode: 'same-origin',
                                    body: formData});
        let response = await fetch(request);
        let responseJSON = await response.json();
        if (responseJSON.valid === 'true') {
            // update displayed events
            let allEventContainer = document.getElementById('post_events').querySelector('.both_columns.bottom_row');
            let first_event_container = document.getElementsByClassName('event_container advertised')[0];
            let new_event = document.createElement('div');
            allEventContainer.insertBefore(new_event, first_event_container);
            new_event.outerHTML = responseJSON.event;
            let no_events_msg = allEventContainer.querySelector('.advertised.event_container > p');
            if (no_events_msg !== null) {
                no_events_msg.parentElement.remove();
            }
            //close modal
            closeModal(postEventModal.firstElementChild.firstElementChild.firstElementChild);

        }
        postEventForm.innerHTML = responseJSON.form;
        refreshDomElementVariables();
        executeAllPageAddListenerFunctions();
        executeAllHomePageAddListenersFunctions();
    }
    catch(error) {
        console.error(error);
    }     
}

/** Fetch GET request handler for refreshing
 *  the edit profile and post event modal forms. Reloads
 *  the database content for a prefilled form. 
 * @summary Fetch GET request for refreshing certain forms.
 * @param {Object} target - the event target that triggered the request.
 */
async function refreshFormFetchHandler(target) {
    try {
        // For aquiring the form csrf token
        const csrftoken = Cookies.get('csrftoken');
        //console.log(target.outerHTML);
        let requestUrl;
        let buttonType;
        let modalContainer;

        if (target.parentElement.parentElement.id === 'edit_profile_modal') {
            requestUrl = 'profile_form/?refresh=true&first_login=false';
            buttonType = 'cancel';
        }
        if (target.parentElement.parentElement.parentElement.id === 'edit_profile_modal') {
            requestUrl = 'profile_form/?refresh=true&first_login=false';
            buttonType = 'close';
        }
        
        if (target.parentElement.parentElement.id === 'post_events_modal') {
            requestUrl = 'post_events/?refresh=true';
            buttonType = 'cancel';
        }
        if (target.parentElement.parentElement.parentElement.id === 'post_events_modal') {
            requestUrl = 'post_events/?refresh=true';
            buttonType = 'close';
        }
                                        

        let getRequest = new Request(requestUrl,
                                     {method: 'GET', headers: {'X-CSRFToken': csrftoken},
                                      mode: 'same-origin'});
        let response = await fetch(getRequest);
        let responseJson = await response.json();
        if (buttonType === 'cancel') {
            modalContainer = target.parentElement.parentElement.parentElement;
        } else {
            modalContainer = target.parentElement.parentElement.parentElement.parentElement;
        }
        let modalReplacement = document.createElement('div');
        modalReplacement.innerHTML = responseJson.modal;
        modalContainer.parentElement.replaceChild(modalReplacement.firstElementChild, modalContainer);
        refreshDomElementVariables();
        executeAllPageAddListenerFunctions();
        executeAllHomePageAddListenersFunctions();
    }
    catch(error) {
        console.error(error);
    }
}

// JS Section: Page specific executed code

// all pages:
executeAllPageAddListenerFunctions();

// landing page
if (document.getElementsByTagName('title')[0].textContent === 'Eventabase') {
    // Initial delay so that initally displayed image does not fade out immediately
    setTimeout(slideshowHandler, 8000);
    executeAllLandingPageAddListenersFunctions();
}

// homepage
if (document.getElementsByTagName('title')[0].textContent === 'Home') {
    executeAllHomePageAddListenersFunctions();    
}

// JS Section: code for jest testing

//uncommented during testing
// module.exports = {
//     moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable,
//     slideshowImages, openMenu, closeMenu, imageFadeIn, imageFadeOut, helpTextIcons,
//     helpText, matchingIcons, signupButton, signinButton, expandIcons, modalContainers, modals,
//     closeModalButtons, editProfileModal, editPersonalInfoForm, editAddressForm,
//     editProfileFormFetchHandler, editProfileModalDoneButton, addEditProfileModalDonebuttonListeners,
//     modalButtons, openModalButtons, postEventModal, radioInputs, advertisedEvents, upcomingEvents, postEventFormFetchHandler, postEventForm,
//     refreshFormFetchHandler
// };