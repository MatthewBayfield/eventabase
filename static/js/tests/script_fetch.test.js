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
     postEventFormFetchHandler, postEventForm,
     editAddressForm, editPersonalInfoForm} = require('../script.js');
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

describe('test the ProfileFormView fetch request works', () => {
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
})

describe('test the post events form fetch request operates as expected', () => {
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