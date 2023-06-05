/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
// Adds rendered home_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_search_adverts_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
     registerInterestButtons, registerInterestFetchHandler} = require('../script.js');
// sweetalert2 library import
global.Swal = require('sweetalert2');
// function from script.js, but redefined in this scope; needed to update references to updated DOM.
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
    postEventFormDoneButton = document.getElementById('post_events_modal') ? document.getElementById('post_events_modal').querySelector('.modal_button') : null;
    postEventForm = document.getElementById('post_events_form');
    advertisedEvents = [...document.getElementsByClassName('advertised')];
    upcomingEvents = [...document.getElementsByClassName('upcoming')];
    radioInputs = [...document.querySelectorAll("[type = 'radio']")];
    deleteEventButtons = [...document.getElementsByClassName('delete_advert')];
    cancelEventButtons = [...document.getElementsByClassName('cancel_event')];
    withdrawButtons = [...document.getElementsByClassName('withdraw')];
    registerInterestButtons = {...document.getElementsByClassName('register_interest')};
}
// mock functions
const get = jest.fn();
global.Cookies = {'get': get};
global.Request = jest.fn();
let json_data;
global.fetch = jest.fn(() => Promise.resolve({
    json: () => Promise.resolve(json_data)
}));
let swal_fire = jest.spyOn(Swal, 'fire');
// global variables needed for some tests
initialSearchEventAdvertsPageContent = document.body.innerHTML;

describe('test that the register interest fetch POST request operates as expected', () => {
    beforeEach(() => {
        refreshDomElementVariables();
    })
    afterEach(() => {
                Request.mockClear();
                fetch.mockClear();
                swal_fire.mockClear();
                // reset html content
                document.body.innerHTML = initialSearchEventAdvertsPageContent;
    })

    test('check request and response/actions when a successful request to register interest is made', async () => {
                json_data = {'successful': 'true'};
                expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
                // the event should be visible
                expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
                // call the handler
                let registerInterestButton = registerInterestButtons[0];
                let event = {currentTarget: registerInterestButton};
                await registerInterestFetchHandler(event);
                expect(Request).toHaveBeenCalledTimes(1);
                expect(fetch).toHaveBeenCalledTimes(1);
                expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['']));
                // check event advert has been hidden and the 'no more adverts' message appears
                expect(document.querySelectorAll('.event_container.advert').length).toBe(2);
                expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('none');
                let message = 'There are currently no adverts, please refresh the page or check again later.';
                expect(window.getComputedStyle(document.querySelectorAll('.event_container.advert')[1]).getPropertyValue('display')).toBe('block');
                expect(document.querySelector('.event_container.advert > p').innerHTML).toBe(message);
                // check success alert has been fired
                expect(swal_fire).toHaveBeenCalledTimes(1);
                expect(swal_fire).toHaveBeenLastCalledWith({
                    title: 'Success',
                    text: 'Your interest in this event/activity has been registered',
                    icon: 'success',
                    allowOutsideClick: false,
                    confirmButtonText: 'Continue',
                    confirmButtonAriaLabel: 'Continue',
                })
    })

    test('check request and response/actions when an unsuccessful request to register interest is made, due to an event clash type exception', async () => {
        json_data = {'successful': 'false', 'error_msg': 'error message', 'error_type': 'clash'};
        expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
        // the event should be visible
        expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
        // call the handler
        let registerInterestButton = registerInterestButtons[0];
        let event = {currentTarget: registerInterestButton};
        await registerInterestFetchHandler(event);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['']));
        // check event advert has not been hidden
        expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
        expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
        // check warning alert has been fired
        expect(swal_fire).toHaveBeenCalledTimes(1);
        expect(swal_fire).toHaveBeenLastCalledWith({
            title: 'Event Date Clash',
            text: 'error message',
            icon: 'warning',
            allowOutsideClick: false,
            confirmButtonText: 'Continue',
            confirmButtonAriaLabel: 'Continue',
        })
    })

    test('check request and response/actions when an unsuccessful request to register interest is made, due to a max_people type exception', async () => {
        json_data = {'successful': 'false', 'error_msg': 'error message', 'error_type': 'max_people'};
        expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
        // the event should be visible
        expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
        // call the handler
        let registerInterestButton = registerInterestButtons[0];
        let event = {currentTarget: registerInterestButton};
        await registerInterestFetchHandler(event);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['']));
        // check event advert has not been hidden
        expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
        expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
        // check warning alert has been fired
        expect(swal_fire).toHaveBeenCalledTimes(1);
        expect(swal_fire).toHaveBeenLastCalledWith({
            title: 'Too many attendees',
            text: 'error message',
            icon: 'info',
            allowOutsideClick: false,
            confirmButtonText: 'Continue',
            confirmButtonAriaLabel: 'Continue',
        })
    })

    test('check request and response/actions when an unsuccessful request to register interest is made, due to a database type exception', async () => {
        json_data = {'successful': 'false', 'error_msg': 'error message', 'error_type': 'database'};
        expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
        // the event should be visible
        expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
        // call the handler
        let registerInterestButton = registerInterestButtons[0];
        let event = {currentTarget: registerInterestButton};
        await registerInterestFetchHandler(event);
        expect(Request).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['']));
        // check event advert has not been hidden
        expect(document.querySelectorAll('.event_container.advert').length).toBe(1);
        expect(document.querySelectorAll('.event_container.advert')[0].style.display).toBe('');
        // check warning alert has been fired
        expect(swal_fire).toHaveBeenCalledTimes(1);
        expect(swal_fire).toHaveBeenLastCalledWith({
            title: 'Something went wrong',
            text: 'error message',
            icon: 'error',
            allowOutsideClick: false,
            confirmButtonText: 'Continue',
            confirmButtonAriaLabel: 'Continue',
        })
    })
})