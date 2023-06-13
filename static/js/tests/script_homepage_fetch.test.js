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
     postEventFormFetchHandler, postEventForm, refreshFormFetchHandler, updateEventFetchHandler,
     editAddressForm, editPersonalInfoForm, openModalButtons, deleteEventButtons, cancelEventButtons,
     withdrawButtons, withdrawFromEventFetchHandler, registerInterestFetchHandler,
     attendeeContactInfoModalCloseButton, attendeeInfoButtons, hostInfoButtons, attendeeContactInfoModal,
     hostContactInfoModalCloseButton, hostContactInfoModal, retrieveContactInfoFetchHandler, postEventFormDoneButton} = require('../script.js');
const { default: Swal } = require('sweetalert2');
// sweetalert2 library import
global.Swal = require('sweetalert2');
// mock functions
const get = jest.fn();
get.mockReturnValue('token');
global.Cookies = {'get': get};
global.Request = jest.fn();
let json_data;
global.fetch = jest.fn(() => Promise.resolve({
    json: () => Promise.resolve(json_data)
}));
global.alert = jest.fn();
let swal_fire = jest.spyOn(Swal, 'fire');
// mocking the scrollTo method of a DOM element
Element.prototype.scrollTo = jest.fn();
// will be used to simulate DOM update from fetch payload. The content is chosen to allow other tests to still work
let profile_content = '<div class="open_modal_button" aria-controls="edit_profile_modal"></div>'

describe('All tests', () => {
    beforeEach(() => {
        jest.resetModules();
        // Adds rendered home_page template HTML content to the JSDOM
        fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_home_page.html', 'utf-8');
        document.documentElement.innerHTML = fileContents;
        //refresh DOM variables
        ({moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
        modalContainers, modals, closeModalButtons, editProfileModal, editProfileModalDoneButton,
        editProfileFormFetchHandler, addEditProfileModalDonebuttonListeners, postEventModal,
        postEventFormFetchHandler, postEventForm, refreshFormFetchHandler, updateEventFetchHandler,
        editAddressForm, editPersonalInfoForm, openModalButtons, deleteEventButtons, cancelEventButtons,
        withdrawButtons, withdrawFromEventFetchHandler, registerInterestFetchHandler,
        attendeeContactInfoModalCloseButton, attendeeInfoButtons, hostInfoButtons, attendeeContactInfoModal,
        hostContactInfoModalCloseButton, hostContactInfoModal, retrieveContactInfoFetchHandler, postEventFormDoneButton} = require('../script.js'));
    })
    describe('test the ProfileFormView fetch POST request works', () => {
        beforeEach(() => {
            editProfileModal.parentElement.style.display = 'block';
        })
        afterEach(() => {
            Request.mockClear();
            fetch.mockClear();
            alert.mockClear();
            swal_fire.mockClear();
        })
    
        test('only two requests are made if the submitted forms are invalid, and the profile content does not change', async () => {
            json_data = {'valid': 'false', 'profile': profile_content, 'form': "<p>form</p>"}
            expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
            expect(editAddressForm.innerHTML).not.toBe("<p>form</p>");
            expect(editPersonalInfoForm.innerHTML).not.toBe("<p>form</p>");
            expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe(profile_content);
            // call handler
            await editProfileFormFetchHandler();
            expect(Request).toHaveBeenCalledTimes(2);
            expect(fetch).toHaveBeenCalledTimes(2);
            // check form content
            expect(editAddressForm.innerHTML).toBe("<p>form</p>");
            let content = '<p class="errorlist"><strong>Please correct the errors described/indicated below, before resubmitting the form:</strong></p><p>form</p>';
            expect(editPersonalInfoForm.innerHTML).toBe(content);
            // check profile content has not changed
            expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe(profile_content);
            // check modal is still open
            expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
        })
    
        test('four requests are made if the submitted forms are valid, and the profile content is updated', async () => {
            json_data = {'valid': 'true', 'profile': profile_content, 'form': 'form'}
            expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
            expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe(profile_content);
            expect(editAddressForm.innerHTML).not.toBe('form');
            expect(editPersonalInfoForm.innerHTML).not.toBe('form');
            // call handler
            await editProfileFormFetchHandler();
            expect(Request).toHaveBeenCalledTimes(4);
            expect(fetch).toHaveBeenCalledTimes(4);
            expect(editAddressForm.innerHTML).toBe('form');
            expect(editPersonalInfoForm.innerHTML).toBe('form');
            expect(editProfileModal.parentElement.previousElementSibling.innerHTML).toBe(profile_content);
            // check success alert has been fired
            expect(swal_fire).toHaveBeenCalledTimes(1);
            expect(swal_fire.mock.lastCall[0].toString()).toEqual({
                title: 'Success',
                text: 'Your profile information has been successfully updated',
                icon: 'success',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
                //close edit profile modal
                willClose: () => {closeModal(editProfileModal.firstElementChild.firstElementChild.firstElementChild)}
            }.toString());
            // check modal is closed after closing alert
            Swal.getConfirmButton().click();
            expect(editProfileModal.parentElement.hasAttribute('style')).toBe(false);
        })
    
        test('that an alert is raised when the related python exception occurs', async () => {
            json_data = {'valid': 'true', 'profile': profile_content, 'error': 'true', 'form': 'form'}
            await editProfileFormFetchHandler();
            expect(Request).toHaveBeenCalledTimes(4);
            expect(fetch).toHaveBeenCalledTimes(4);
            expect(alert).toHaveBeenCalledTimes(1);
            errMsg = `There was a problem processing your submitted address, please check that the address information you entered
    is valid and try again; If the address is valid, try another address; if the problem persists, try again later.`;
            expect(alert).toHaveBeenCalledWith(errMsg);
            
        })        
    
        test('that the profile is updated when the error occurs', async () => {
            json_data = {'valid': 'true', 'profile': profile_content, 'error': 'true', 'form': 'form'}
            expect(editProfileModal.parentElement.previousElementSibling.innerHTML).not.toBe(profile_content);
            // call handler
            await editProfileFormFetchHandler();
            expect(Request).toHaveBeenCalledTimes(4);
            expect(fetch).toHaveBeenCalledTimes(4);
            expect(editProfileModal.parentElement.previousElementSibling.innerHTML).toBe(profile_content);
            // check modal is still open
            expect(editProfileModal.parentElement.hasAttribute('style')).toBe(true);
        })
    
        test('that the edit profile modal close/cancel button become available after first successful form submission', async () => {
            json_data = {'valid': 'true', 'profile': profile_content, 'form': 'form'}
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
            // close success alert
            Swal.getConfirmButton().click();
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
            swal_fire.mockClear();
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
            // check success alert has been fired
            expect(swal_fire).toHaveBeenCalledTimes(1);
            expect(swal_fire.mock.lastCall[0].toString()).toEqual({
                title: 'Success',
                text: 'Your event/activity advert has been posted',
                icon: 'success',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
                willClose: () => {closeModal(postEventModal.firstElementChild.firstElementChild.firstElementChild)}
            }.toString())
            // check modal has been closed after alert is closed
            Swal.getConfirmButton().click();
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
    
    describe('test the update events fetch POST request operates as expected', () => {
        beforeEach(() => {
            // grid container styling
            document.getElementById('post_events_grid').style.display = 'grid';
            document.querySelectorAll('.event_container.advertised')[0].style.display = 'block';
            document.querySelectorAll('.event_container.upcoming')[0].style.display = 'block';
        })
        afterEach(() => {
            Request.mockClear();
            fetch.mockClear();
            swal_fire.mockClear();
        })
    
        test('check request and response/actions when a successful cancel event request is submitted', async () => {
            json_data = {'successful': 'true'};
            expect(document.querySelectorAll('.event_container.upcoming').length).toBe(1);
            // the event should be visible
            expect(document.querySelectorAll('.event_container.upcoming')[0].style.display).toBe('block');
            // call the handler
            let cancelButton = cancelEventButtons[0];
            let event = {currentTarget: cancelButton};
            await updateEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['update_events/?cancel=true']));
            // check event has been hidden
            expect(document.querySelectorAll('.event_container.upcoming').length).toBe(2);
            expect(document.querySelectorAll('.event_container.upcoming')[0].style.display).toBe('none');
            // check success alert has been fired
            expect(swal_fire).toHaveBeenCalledTimes(1);
            let success_msg = `Your upcoming event/activity has been cancelled.`;
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Success',
                text: success_msg,
                icon: 'success',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
        })
    
        test('check request and response/actions when a successful delete advert request is submitted', async () => {
            json_data = {'successful': 'true'};
            expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
            // the event should be visible
            expect(document.querySelectorAll('.event_container.advertised')[0].style.display).toBe('block');
            // call the handler
            let deleteButton = deleteEventButtons[0];
            let event = {currentTarget: deleteButton};
            await updateEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['update_events/?cancel=false']));
            // check event has been hidden
            expect(document.querySelectorAll('.event_container.advertised').length).toBe(2);
            expect(document.querySelectorAll('.event_container.advertised')[0].style.display).toBe('none');
            // check success alert has been fired
            expect(swal_fire).toHaveBeenCalledTimes(1);
            let success_msg = `Your event/activity advert has been deleted.`;
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Success',
                text: success_msg,
                icon: 'success',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
        })
    
        test('check request and response/actions when an unsuccessful cancel event request is submitted', async () => {
            json_data = {'successful': 'false'};
            expect(document.querySelectorAll('.event_container.upcoming').length).toBe(1);
            // the event should be visible
            expect(document.querySelectorAll('.event_container.upcoming')[0].style.display).toBe('block');
            // call the handler
            let cancelButton = cancelEventButtons[0];
            let event = {currentTarget: cancelButton};
            await updateEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['update_events/?cancel=true']));
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(1);
            let error_msg = `Unable to cancel the event at the moment, please try again later.
If the problem persists, please report the issue to us.`;
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Something went wrong',
                text: error_msg,
                icon: 'error',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
            // check event has not been hidden
            expect(document.querySelectorAll('.event_container.upcoming').length).toBe(1);
            expect(document.querySelectorAll('.event_container.upcoming')[0].style.display).not.toBe('none');
        })
    
        test('check request and response/actions when an unsuccessful delete advert request is submitted', async () => {
            json_data = {'successful': 'false'};
            expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
            // the event should be visible
            expect(document.querySelectorAll('.event_container.advertised')[0].style.display).toBe('block');
            // call the handler
            let deleteButton = deleteEventButtons[0];
            let event = {currentTarget: deleteButton};
            await updateEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['update_events/?cancel=false']));
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(1);
            let error_msg = `Unable to delete advert at the moment, please try again later.
If the problem persists, please report the issue to us.`;
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Something went wrong',
                text: error_msg,
                icon: 'error',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
            // check event has not been hidden
            expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
            expect(document.querySelectorAll('.event_container.advertised')[0].style.display).not.toBe('none');
        })
    
        test("check no the expected no events message displays once all a user's events/adverts have been cancelled/deleted", async () => {
            json_data = {'successful': 'true'};
            // testing for when cancelling events:
    
            expect(document.querySelectorAll('.event_container.upcoming').length).toBe(1);
            // the events should be visible
            expect(document.querySelectorAll('.event_container.upcoming')[0].style.display).toBe('block');
            let event;
            for (button of cancelEventButtons) {
                event = {currentTarget: button};
                // call the handler to simulate cancelling an event
                await updateEventFetchHandler(event);
                if (document.querySelectorAll('.event_container.upcoming')[0].style.display === 'block') {
                    expect(document.querySelectorAll('.event_container.upcoming').length).toBe(1);
                    expect(document.querySelector('.event_container.upcoming > p')).toBe(null);
                }
                else {
                    expect(document.querySelectorAll('.event_container.upcoming').length).toBe(2);
                    let message = `You currenty have no upcoming events or activities that are you are confirmed to host. An event becomes confirmed once the closing advert date has passed.`;
                    expect(window.getComputedStyle(document.querySelectorAll('.event_container.upcoming')[1]).getPropertyValue('display')).toBe('block');
                    expect(document.querySelector('.event_container.upcoming > p').innerHTML).toBe(message);
                }
            }
            // testing for when deleting adverts:
    
            expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
            // the events should be visible
            expect(document.querySelectorAll('.event_container.advertised')[0].style.display).toBe('block');
            for (button of deleteEventButtons) {
                event = {currentTarget: button};
                // call the handler to simulate deleting an event advert
                await updateEventFetchHandler(event);
                if (document.querySelectorAll('.event_container.advertised')[0].style.display === 'block') {
                    expect(document.querySelectorAll('.event_container.advertised').length).toBe(1);
                    expect(document.querySelector('.event_container.advertised > p')).toBe(null);
                }
                else {
                    expect(document.querySelectorAll('.event_container.advertised').length).toBe(2);
                    let message = `You currenty have no adverts for hosting events or activities.`;
                    expect(window.getComputedStyle(document.querySelectorAll('.event_container.advertised')[1]).getPropertyValue('display')).toBe('block');
                    expect(document.querySelector('.event_container.advertised > p').innerHTML).toBe(message);
                }
            }
        })
    })
    
    describe('test the event withdrawal fetch POST request operates as expected', () => {
        beforeEach(() => {
            // grid container styling
            document.getElementById('search_events_grid').style.display = 'grid';
            document.querySelectorAll('.event_container.interested')[0].style.display = 'block';
            document.querySelectorAll('.event_container.attending')[0].style.display = 'block';
            document.querySelectorAll('.event_container.interested')[1].style.display = 'block';
            document.querySelectorAll('.event_container.attending')[1].style.display = 'block';
            document.querySelectorAll('.event_container.interested')[2].style.display = 'block';
        })
        afterEach(() => {
            Request.mockClear();
            fetch.mockClear();
            swal_fire.mockClear();
        })
    
        test('check request and response/actions when a successful event withdrawal request is submitted', async () => {
            json_data = {'successful': 'true'};
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            // the events should be visible
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            let withdrawInterestButton = withdrawButtons[0];
            let withdrawButton = withdrawButtons[3];
            let event = {currentTarget: withdrawInterestButton};
            // call the handler to simulate withdrawing interest
            await withdrawFromEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['event_withdrawal/']));
            // check only the intended event has been hidden
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('none');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(1);
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Success',
                text: 'You have successfully been withdrawn from this event/activity',
                icon: 'success',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
    
            // call the handler to simulate withdrawing from a confirmed event
            event = {currentTarget: withdrawButton};
            await withdrawFromEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(2);
            expect(fetch).toHaveBeenCalledTimes(2);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['event_withdrawal/']));
            // check event has been hidden
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('none');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('none');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(2);
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Success',
                text: 'You have successfully been withdrawn from this event/activity',
                icon: 'success',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
        })
    
        test('check request and response/actions when an unsuccessful event withdrawal request is submitted', async () => {
            json_data = {'successful': 'false'};
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            // the events should be visible
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            let withdrawInterestButton = withdrawButtons[0];
            let withdrawButton = withdrawButtons[3];
            let event = {currentTarget: withdrawInterestButton};
            // call the handler to simulate withdrawing interest
            await withdrawFromEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['event_withdrawal/']));
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(1);
            let err_msg = `Unable to withdraw you from the event at the moment, please try again later.
If the problem persists, please report the issue to us.`;
            expect(swal_fire).toHaveBeenLastCalledWith({
                    title: 'Something went wrong',
                    text: err_msg,
                    icon: 'error',
                    allowOutsideClick: false,
                    confirmButtonText: 'Continue',
                    confirmButtonAriaLabel: 'Continue',
                })
            // check event has not been hidden
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            // call the handler to simulate withdrawing from a confirmed event
            event = {currentTarget: withdrawButton};
            await withdrawFromEventFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(2);
            expect(fetch).toHaveBeenCalledTimes(2);
            expect(Request.mock.lastCall).toEqual(expect.arrayContaining(['event_withdrawal/']));
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(2);
            expect(swal_fire).toHaveBeenLastCalledWith({
                    title: 'Something went wrong',
                    text: err_msg,
                    icon: 'error',
                    allowOutsideClick: false,
                    confirmButtonText: 'Continue',
                    confirmButtonAriaLabel: 'Continue',
                })
            // check event has not been hidden
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
        })
    
        test('check no the expected no events message displays once all events have been withdrawn from', async () => {
            json_data = {'successful': 'true'};
            // testing for a user's interested events:
    
            expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            // the events should be visible
            expect(document.querySelectorAll('.event_container.interested')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.interested')[2].style.display).toBe('block');
            let withdrawInterestButtons = withdrawButtons.slice(0, 3);
            let withdrawalButtons = withdrawButtons.slice(3, 5);
            let event;
            for (button of withdrawInterestButtons) {
                event = {currentTarget: button};
                // call the handler to simulate withdrawing interest
                await withdrawFromEventFetchHandler(event);
                if (document.querySelectorAll('.event_container.interested')[2].style.display === 'block') {
                    expect(document.querySelectorAll('.event_container.interested').length).toBe(3);
                    expect(document.querySelector('.event_container.interested > p')).toBe(null);
                }
                else {
                    expect(document.querySelectorAll('.event_container.interested').length).toBe(4);
                    let message = 'You currenty have no events or activities for which you have registered you interest in.';
                    expect(window.getComputedStyle(document.querySelectorAll('.event_container.interested')[3]).getPropertyValue('display')).toBe('block');
                    expect(document.querySelector('.event_container.interested > p').innerHTML).toBe(message);
                    
                }
            }
            // testing for a user's upcoming events:
    
            expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
            expect(document.querySelectorAll('.event_container.attending')[0].style.display).toBe('block');
            expect(document.querySelectorAll('.event_container.attending')[1].style.display).toBe('block');
            // call the handler to simulate withdrawing from a confirmed event
            for (button of withdrawalButtons) {
                event = {currentTarget: button};
                await withdrawFromEventFetchHandler(event);
                if (document.querySelectorAll('.event_container.attending')[1].style.display === 'block') {
                    expect(document.querySelectorAll('.event_container.attending').length).toBe(2);
                    expect(document.querySelector('.event_container.attending > p')).toBe(null);
                }
                else {
                    expect(document.querySelectorAll('.event_container.attending').length).toBe(3);
                    let message = `You currenty have no upcoming events or activities that are you are confirmed to attend. An event becomes confirmed once the closing advert date has passed.`;
                    expect(window.getComputedStyle(document.querySelectorAll('.event_container.attending')[2]).getPropertyValue('display')).toBe('block');
                    expect(document.querySelector('.event_container.attending > p').innerHTML).toBe(message);
                }
            }
        })
    })

    describe('test the fetch POST request of the retrieveContactInfoFetchHandler operates as expected', () => {
        beforeEach(() => {
            // grid container styling
            get.mockClear();
            Element.prototype.scrollTo.mockClear();
        })
        afterEach(() => {
            Request.mockClear();
            fetch.mockClear();
            swal_fire.mockClear();
        })
    
        test('check request and response/actions when a successful request for attendee contact info is submitted', async () => {
            let rendered_modal = `<div id="attendee_contact_info" tabindex="0">rendered_modal_placeholder</div>`;
            json_data = {'successful': 'true','rendered_modal': rendered_modal};
            let attendeeContactInfoButton = attendeeInfoButtons[0];
            let event = {currentTarget: attendeeContactInfoButton};
            // call the handler to simulate opening modal
            await retrieveContactInfoFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(['/events_and_activities/retrieve_contact_info/', {method: 'POST', headers: {'X-CSRFToken': 'token'},
            mode: 'same-origin', body: JSON.stringify({event_id: '5', host: 'no'})}]);
            // check rendered modal is added to DOM
            expect(document.getElementById('post_events').firstElementChild.outerHTML).toBe(`<div class="modal_container" tabindex="0" style="display:block;">${rendered_modal}</div>`);
            // check modal has focus
            expect(document.hasFocus(attendeeContactInfoModal)).toBe(true);
            // check modal scrolled to top
            expect(Element.prototype.scrollTo).toHaveBeenCalledTimes(1);
            expect(Element.prototype.scrollTo).toHaveBeenLastCalledWith({
                top: 0,
                behaviour: 'instant'
            });
        })
    
        test('check request and response/actions when a successful request for host contact info is submitted', async () => {
            let rendered_modal = `<div id="host_contact_info" tabindex="0">rendered_modal_placeholder</div>`;
            json_data = {'successful': 'true','rendered_modal': rendered_modal};
            let hostContactInfoButton = hostInfoButtons[0];
            let event = {currentTarget: hostContactInfoButton};
            // call the handler to simulate opening modal
            await retrieveContactInfoFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(['/events_and_activities/retrieve_contact_info/', {method: 'POST', headers: {'X-CSRFToken': 'token'},
            mode: 'same-origin', body: JSON.stringify({event_id: '2', host: 'yes'})}]);
            // check rendered modal is added to DOM
            expect(document.getElementById('search_events').firstElementChild.outerHTML).toBe(`<div class="modal_container" tabindex="0" style="display:block;">${rendered_modal}</div>`);
            // check modal has focus
            expect(document.hasFocus(hostContactInfoModal)).toBe(true);
            // check modal scrolled to top
            expect(Element.prototype.scrollTo).toHaveBeenCalledTimes(1);
            expect(Element.prototype.scrollTo).toHaveBeenLastCalledWith({
                top: 0,
                behaviour: 'instant'
            });
        })
            
        test('check request and response/actions when an unsuccessful request for attendee contact info is submitted', async () => {
            let rendered_modal = `<div id="attendee_contact_info" tabindex="0">rendered_modal_placeholder</div>`;
            msg = `Unable to retrieve the contact information of the attendees of this event at this time. Please refresh the page and try again. If the problem
persists, please contact us.`
            json_data = {'successful': 'false', 'error_msg': msg};
            let attendeeContactInfoButton = attendeeInfoButtons[0];
            let event = {currentTarget: attendeeContactInfoButton};
            // call the handler to simulate opening modal
            await retrieveContactInfoFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(['/events_and_activities/retrieve_contact_info/', {method: 'POST', headers: {'X-CSRFToken': 'token'},
            mode: 'same-origin', body: JSON.stringify({event_id: '5', host: 'no'})}]);
            // check rendered modal has not been added to DOM
            expect(document.getElementById('post_events').firstElementChild.outerHTML).not.toBe(`<div class="modal_container" tabindex="0" style="display:block;">${rendered_modal}</div>`);
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(1);
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Something went wrong',
                text: json_data.error_msg,
                icon: 'error',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
        })
    
        test('check request and response/actions when an unsuccessful request for host contact info is submitted', async () => {
            let rendered_modal = `<div id="host_contact_info" tabindex="0">rendered_modal_placeholder</div>`;
            msg = `Unable to retrieve the contact information of the host of this event at this time. Please refresh the page and try again. If the problem
persists, please contact us.`
            json_data = {'successful': 'false', 'error_msg': msg};
            let hostContactInfoButton = hostInfoButtons[0];
            let event = {currentTarget: hostContactInfoButton};
            // call the handler to simulate opening modal
            await retrieveContactInfoFetchHandler(event);
            expect(Request).toHaveBeenCalledTimes(1);
            expect(fetch).toHaveBeenCalledTimes(1);
            expect(Request.mock.lastCall).toEqual(['/events_and_activities/retrieve_contact_info/', {method: 'POST', headers: {'X-CSRFToken': 'token'},
            mode: 'same-origin', body: JSON.stringify({event_id: '2', host: 'yes'})}]);
            // check rendered modal has not been added to DOM
            expect(document.getElementById('search_events').firstElementChild.outerHTML).not.toBe(`<div class="modal_container" tabindex="0" style="display:block;">${rendered_modal}</div>`);
            // check alert displayed
            expect(swal_fire).toHaveBeenCalledTimes(1);
            expect(swal_fire).toHaveBeenLastCalledWith({
                title: 'Something went wrong',
                text: json_data.error_msg,
                icon: 'error',
                allowOutsideClick: false,
                confirmButtonText: 'Continue',
                confirmButtonAriaLabel: 'Continue',
            })
        })
    })
})
    
    