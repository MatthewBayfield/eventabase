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
// mock functions
const get = jest.fn();
global.Cookies = {'get': get};
global.Request = jest.fn();
let json_data;
global.fetch = jest.fn(() => Promise.resolve({
    json: () => Promise.resolve(json_data)
}));
let swal_fire = jest.spyOn(Swal, 'fire');
clickSpy = jest.spyOn(HTMLElement.prototype, 'click');

describe('All tests', () => {
    beforeEach(() => {
        jest.resetModules();
        // Adds rendered home_page template HTML content to the JSDOM
        fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_search_adverts_page.html', 'utf-8');
        document.documentElement.innerHTML = fileContents;
        //refresh DOM variables
        ({moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
            registerInterestButtons, registerInterestFetchHandler} = require('../script.js'));
    })

    describe('test that the register interest fetch POST request operates as expected', () => {
        afterEach(() => {
                    Request.mockClear();
                    fetch.mockClear();
                    swal_fire.mockClear();
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
})

