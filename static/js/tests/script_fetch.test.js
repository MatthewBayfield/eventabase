/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
// Adds rendered home_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_home_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
     modalContainers, modals, closeModalButtons, editProfileModal, editProfileModalDoneButton,
     editProfileFormFetchHandler, addEditProfileModalDonebuttonListeners, postEventModal,
     postEventFormFetchHandler, postEventForm, refreshFormFetchHandler,
     editAddressForm, editPersonalInfoForm} = require('../script.js');
// functions from script.js, but redefined in this scope; needed to update references to updated DOM.
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

// mock functions
const get = jest.fn()
global.Cookies = {'get': get};
global.Request = jest.fn();
let json_data;
global.fetch = jest.fn(() => Promise.resolve({
    json: () => Promise.resolve(json_data)
}));
global.alert = jest.fn();
// global variables needed for some tests
let initialPostEventsSection = postEventModal.parentElement.previousElementSibling.innerHTML;
let initialPostEventForm = postEventForm.innerHTML;
let initialProfileSection = editProfileModal.parentElement.previousElementSibling.innerHTML;
let initialAddressForm = editAddressForm.innerHTML;
let initialPersonalInfoForm =  editPersonalInfoForm.innerHTML;

describe('test the ProfileFormView fetch POST request works', () => {
    beforeEach(() => {
        editProfileModal.parentElement.style.display = 'block';
    })
    afterEach(() => {
        Request.mockClear();
        fetch.mockClear();
        alert.mockClear();
        // reset html content
        editProfileModal.parentElement.previousElementSibling.innerHTML = initialProfileSection;
        editAddressForm.innerHTML = initialAddressForm;
        editPersonalInfoForm.innerHTML = initialPersonalInfoForm;
    })

    test('only two requests are made if the submitted forms are invalid, and the profile content does not change', async () => {
        json_data = {'valid': 'false', 'profile': 'profile', 'form': 'form'}
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
        expect(editAddressForm.innerHTML).not.toBe('form');
        expect(editPersonalInfoForm.innerHTML).not.toBe('form');
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe('profile');
        // call handler
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(2);
        expect(fetch).toHaveBeenCalledTimes(2);
        expect(editAddressForm.innerHTML).toBe('form');
        expect(editPersonalInfoForm.innerHTML).toBe('form');
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe('profile');
        // check modal is still open
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
    })

    test('four requests are made if the submitted forms are valid, and the profile content is updated', async () => {
        json_data = {'valid': 'true', 'profile': 'profile', 'form': 'form'}
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe('profile');
        expect(editAddressForm.innerHTML).not.toBe('form');
        expect(editPersonalInfoForm.innerHTML).not.toBe('form');
        // call handler
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(4);
        expect(fetch).toHaveBeenCalledTimes(4);
        expect(editAddressForm.innerHTML).toBe('form');
        expect(editPersonalInfoForm.innerHTML).toBe('form');
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML).toBe('profile');
        // check modal is closed
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(false);
    })

    test('that an alert is raised when the related python exception occurs', async () => {
        json_data = {'valid': 'true', 'profile': 'profile', 'error': 'true', 'form': 'form'}
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(4);
        expect(fetch).toHaveBeenCalledTimes(4);
        expect(alert).toHaveBeenCalledTimes(1);
        errMsg = `There was a problem processing your submitted address, please check that the address information you entered
    is valid and try again; If the address is valid, try another address; if the problem persists, try again later.`;
        expect(alert).toHaveBeenCalledWith(errMsg);
        
    })        

    test('that the profile is updated when the error occurs', async () => {
        json_data = {'valid': 'true', 'profile': 'profile', 'error': 'true', 'form': 'form'}
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe('profile');
        // call handler
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(4);
        expect(fetch).toHaveBeenCalledTimes(4);
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML).toBe('profile');
        // check modal is still open
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
    })

    test('that the edit profile modal close/cancel button become available after first successful form submission', async () => {
        json_data = {'valid': 'true', 'profile': 'profile', 'form': 'form'}
        // close button is hidden on first login
        editProfileModal.firstElementChild.firstElementChild.style = "visibility:hidden";
        // no cancel button on first login
        let cancelButton = editProfileModal.querySelector("[name = 'Cancel']");
        cancelButton.remove();

        // initial state
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
        expect(editProfileModal.firstElementChild.firstElementChild.hasAttribute('style')).toBe(true);
        expect(editProfileModal.lastElementChild.children.length < 2).toBe(true);
        // call handler with valid form response
        await editProfileFormFetchHandler();
        // check cancel button exists, and close button is visible
        expect(editProfileModal.parentElement.hasAttribute('style')).toBe(false);
        expect(editProfileModal.lastElementChild.children.length < 2).toBe(false);
        expect(editProfileModal.querySelector("[name = 'Cancel']")).not.toBe(null);
    })
})

describe('test the post events form fetch POST request operates as expected', () => {
    beforeEach(() => {
        // modal container styling
        postEventModal.parentElement.style.display = 'block';
    })
    afterEach(() => {
        Request.mockClear();
        fetch.mockClear();
        // reset html content
        postEventModal.parentElement.previousElementSibling.innerHTML = initialPostEventsSection;
        postEventForm.innerHTML = initialPostEventForm;
    })

    test('check request and response/actions when a valid form is submitted', async () => {
        json_data = {'valid': 'true', 'form': 'form', 'event': '<div class="event_container advertised">event</div>'};
        expect(postEventModal.parentElement.hasAttribute('style')).toBe(true);
        expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
        // add no_event_msg p element for the sake of testing
        let div = document.createElement('div');
        document.querySelectorAll('.event_container.advertised')[0].parentElement.appendChild(div);
        div.outerHTML = "<div class='advertised event_container'><p></p></div>";
        expect(document.querySelectorAll('.event_container.advertised').length).toBe(2);
        expect(document.querySelectorAll('.event_container.advertised > p').length).toBe(1);
        // call the handler
        await postEventFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['post_events/']));
        expect(document.querySelectorAll('.event_container.advertised').length).toBe(2);
        // check event has been added
        expect(document.querySelectorAll('.event_container.advertised')[0].innerHTML).toBe('event');
        // check message has been removed
        expect(document.querySelectorAll('.event_container.advertised > p').length).toBe(0);
        // check form content updated
        expect(postEventForm.innerHTML).toBe('form');
        // check modal has been closed
        expect(postEventModal.parentElement.hasAttribute('style')).toBe(false);
    })

    test('check request and response/actions when an invalid form is submitted', async () => {
        json_data = {'valid': 'false', 'form': 'form', 'event': '<div class="event_container advertised">event</div>'};
        expect(postEventModal.parentElement.hasAttribute('style')).toBe(true);
        expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
        // add no_event_msg p element for the sake of testing
        let div = document.createElement('div');
        document.querySelectorAll('.event_container.advertised')[0].parentElement.appendChild(div);
        div.outerHTML = "<div class='advertised event_container'><p></p></div>";
        expect(document.querySelectorAll('.event_container.advertised').length).toBe(2);
        expect(document.querySelectorAll('.event_container.advertised > p').length).toBe(1);
        // call the handler
        await postEventFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['post_events/']));
        expect(document.querySelectorAll('.event_container.advertised').length).toBe(2);
        // check message still present
        expect(document.querySelectorAll('.event_container.advertised > p').length).toBe(1);
        // check no new event has been added
        expect(document.querySelectorAll('.event_container.advertised')[0].innerHTML).not.toBe('event');
        // check form content updated
        expect(postEventForm.innerHTML).toBe('form');
        // check modal is still open
        expect(postEventModal.parentElement.hasAttribute('style')).toBe(true);
    })
})

describe('test the ProfileFormView and PostEventsView fetch GET requests work', () => {
    beforeEach(() => {
        editProfileModal.parentElement.style.display = 'block';
        postEventModal.parentElement.style.display = 'block';
    })
    afterEach(() => {
        Request.mockClear();
        fetch.mockClear();
        alert.mockClear();
        // reset html content
        refreshDomElementVariables();
        editProfileModal.parentElement.previousElementSibling.innerHTML = initialProfileSection;
        editAddressForm.innerHTML = initialAddressForm;
        editPersonalInfoForm.innerHTML = initialPersonalInfoForm;
        postEventModal.parentElement.previousElementSibling.innerHTML = initialPostEventsSection;
        postEventForm.innerHTML = initialPostEventForm;
    })

    test('that the edit_profile_modal is modified as expected for GET request triggered by clicking cancel', async () => {
        // simulate json response
        modalPlaceholder = editProfileModal.parentElement;
        modalPlaceholder.setAttribute('data-dummy', 'test');
        json_data = {'modal': modalPlaceholder.outerHTML};
        // set target parameter
        let editProfileModalCancelButton = editProfileModal.getElementsByClassName('modal_button')[1];
        // call handler
        await refreshFormFetchHandler(editProfileModalCancelButton);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(editProfileModal.parentElement.outerHTML).toBe(modalPlaceholder.outerHTML);
    })

    test('that the edit_profile_modal is modified as expected for GET request triggered by clicking close', async () => {
        // simulate json response
        modalPlaceholder = editProfileModal.parentElement;
        modalPlaceholder.setAttribute('data-dummy', 'test');
        json_data = {'modal': modalPlaceholder.outerHTML};
        // set target parameter
        let editProfileModalCloseButton = editProfileModal.getElementsByClassName('close_button')[0].firstElementChild;
        // call handler
        await refreshFormFetchHandler(editProfileModalCloseButton);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(editProfileModal.parentElement.outerHTML).toBe(modalPlaceholder.outerHTML);
    })

    test('that the post_events_modal is modified as expected for GET request triggered by clicking cancel', async () => {
        // simulate json response
        modalPlaceholder = postEventModal.parentElement;
        modalPlaceholder.setAttribute('data-dummy', 'test');
        json_data = {'modal': modalPlaceholder.outerHTML};
        // set target parameter
        let postEventModalCancelButton = postEventModal.getElementsByClassName('modal_button')[1];
        // call handler
        await refreshFormFetchHandler(postEventModalCancelButton);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(postEventModal.parentElement.outerHTML).toBe(modalPlaceholder.outerHTML);
    })

    test('that the post_events_modal is modified as expected for GET request triggered by clicking close', async () => {
        // simulate json response
        modalPlaceholder = postEventModal.parentElement;
        modalPlaceholder.setAttribute('data-dummy', 'test');
        json_data = {'modal': modalPlaceholder.outerHTML};
        // set target parameter
        let postEventModalCloseButton = postEventModal.getElementsByClassName('close_button')[0].firstElementChild;
        // call handler
        await refreshFormFetchHandler(postEventModalCloseButton);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(postEventModal.parentElement.outerHTML).toBe(modalPlaceholder.outerHTML);
    })
})