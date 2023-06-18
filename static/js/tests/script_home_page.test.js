/**
* @jest-environment jsdom
*/
jest.useFakeTimers();
// Adds rendered home_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_home_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, focusable, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
     modalContainers, modals, closeModalButtons, modalButtons, editProfileModalDoneButton, editProfileModal,
     openModalButtons, postEventModal, radioInputs, advertisedEvents, upcomingEvents, closeModal, linksAndButtons,
     restoreForm, postEventFormDoneButton, editProfileFormFetchHandler, postEventFormFetchHandler,
     refreshFormFetchHandler, updateEventFetchHandler, deleteEventButtons, cancelEventButtons,
     interestedEvents, attendingEvents, openModalButtonHandler, searchAdvertsButton,
     attendeeInfoButtons, attendeeContactInfoModal, hostInfoButtons, hostContactInfoModal, closeContactInfoModal} = require('../script.js');
// mock functions
clickSpy = jest.spyOn(HTMLElement.prototype, 'click');
let mockFetchEditProfile = jest.fn(() => {
    // code taken from editProfileFormFetchHandler
    closeModal(editProfileModal.firstElementChild.firstElementChild.firstElementChild);
})
let mockFetchEvent = jest.fn(() => {
    closeModal(postEventModal.firstElementChild.firstElementChild.firstElementChild);
})
// mocking the scrollTo method of a DOM element
Element.prototype.scrollTo = jest.fn();
// mocking the openModalButtonHandler so that it uses the mocked scrollTo method
let openModalButtonMockHandler = jest.fn((event) => {
    let i = openModalButtons.indexOf(event.currentTarget);
    if (window.getComputedStyle(modalContainers[i]).getPropertyValue('display') === 'none') {
        modalContainers[i].style.display = 'block';
        modals[i].focus();
        modals[i].scrollTo({
            top: 0,
            behaviour: 'instant'
        })
    document.body.style.overflowY = 'hidden';
    }
})

describe('All tests', () => {
    beforeEach(() => {
        jest.resetModules();
        // Adds rendered home_page template HTML content to the JSDOM
        fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_home_page.html', 'utf-8');
        document.documentElement.innerHTML = fileContents;
        //refresh DOM variables
        ({moreMenu, moreMenuContainer, focusable, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
         modalContainers, modals, closeModalButtons, modalButtons, editProfileModalDoneButton, editProfileModal,
         openModalButtons, postEventModal, radioInputs, advertisedEvents, upcomingEvents, closeModal, linksAndButtons,
         restoreForm, postEventFormDoneButton, editProfileFormFetchHandler, postEventFormFetchHandler,
         refreshFormFetchHandler, updateEventFetchHandler, deleteEventButtons, cancelEventButtons,
         interestedEvents, attendingEvents, openModalButtonHandler, searchAdvertsButton,
         attendeeInfoButtons, attendeeContactInfoModal, hostInfoButtons, hostContactInfoModal, closeContactInfoModal} = require('../script.js'));
    })

    describe('test more menu functionality', () => {
        describe('check the more menu hamburger-style button works', () => {
            beforeEach(() => {
                moreMenuContainer.style.setProperty('display', 'none');
                moreMenu.style.setProperty('visibility', 'hidden');
                moreMenuButtons[0].setAttribute('aria-expanded', 'false');
            })
        
            test("the button's aria attributes change as expected", () => {
                moreMenuButtons[0].click();
                expect(moreMenuButtons[0].getAttribute('aria-expanded')).toBe('True');
            })
        
            test('that the menu background container opens', () => {
                moreMenuButtons[0].click();
                expect(window.getComputedStyle(moreMenuContainer).getPropertyValue('display')).toBe('block');
            })
            
            test("clicking the button makes the menu visible and focused", () => {
                moreMenuButtons[0].click();
                expect(window.getComputedStyle(moreMenu).getPropertyValue('visibility')).toBe('visible');
                expect(document.activeElement).toBe(moreMenu);
            })
        })
        describe('Check the menu items have hover and click/press feedback', () => {
            const menuItems = document.getElementsByClassName('menu_item');
            test(" a menu item's background colour changes only when hovered over", () => {
                    for (let item of menuItems) {
                        let event = new Event('mouseenter');
                        item.dispatchEvent(event);
                        expect(item.classList.contains('active')).toBe(true);
                        event = new Event('mouseleave');
                        item.dispatchEvent(event);
                        expect(item.classList.contains('active')).toBe(false);
                    }
            })
            test("when clicked/pressed the menu item background and font colour changes temporarily", () => {
                for (let item of menuItems) {
                    let event = new Event('mousedown');
                    item.dispatchEvent(event);
                    expect(item.classList.contains('clicked')).toBe(true);
                    event = new Event('mouseup');
                    item.dispatchEvent(event);
                    jest.runOnlyPendingTimers();
                    expect(item.classList.contains('clicked')).toBe(false);
                }
            })
        })
        
        describe('check that the more menu closes when expected', () => {
            beforeEach(() => {
                // set purposefully to something other than block as is necessary for testing
                moreMenuContainer.style.setProperty('display', 'inline');
                // set purposefully to something other than visible as is necessary for testing
                moreMenu.style.setProperty('visibility', 'hidden');
                moreMenuButtons[0].setAttribute('aria-expanded', 'True');
                moreMenu.focus();
            })
        
            test('the close menu button works', () => {
                moreMenuButtons[1].click();
                expect(moreMenuButtons[0].getAttribute('aria-expanded')).toBe('False');
                // quirk of jsdom, to test code removes an inline style attribute, should be left with 'block' 
                expect(window.getComputedStyle(moreMenuContainer).getPropertyValue('display')).toBe('block');
                 // quirk of jsdom, to test code removes an inline style attribute, should be left with 'visible' 
                expect(window.getComputedStyle(moreMenu).getPropertyValue('visibility')).toBe('visible');
                expect(document.activeElement).not.toBe(moreMenu);
            })
        
            test('clicking anywhere within the visible menu container, but not on the open menu itself, closes it', () => {
                // moreMenu click event
                moreMenu.click();
                expect(moreMenuButtons[0].getAttribute('aria-expanded')).toBe('True'); 
                expect(window.getComputedStyle(moreMenuContainer).getPropertyValue('display')).not.toBe('block');
                expect(window.getComputedStyle(moreMenu).getPropertyValue('visibility')).not.toBe('visible');
                expect(document.activeElement).toBe(moreMenu);
                // more MenuContainer click event
                moreMenuContainer.click();
                expect(moreMenuButtons[0].getAttribute('aria-expanded')).toBe('False');
                expect(window.getComputedStyle(moreMenuContainer).getPropertyValue('display')).toBe('block');
                expect(window.getComputedStyle(moreMenu).getPropertyValue('visibility')).toBe('visible');
                expect(document.activeElement).not.toBe(moreMenu);
                // checking else branch of createMoreMenuContainerListener
                moreMenuContainer.style.setProperty('display', 'none');
                moreMenu.style.setProperty('visibility', 'hidden');
                moreMenuButtons[0].setAttribute('aria-expanded', 'True');
                moreMenu.focus();
                moreMenuContainer.click();
                expect(moreMenuButtons[0].getAttribute('aria-expanded')).not.toBe('False');
                expect(window.getComputedStyle(moreMenuContainer).getPropertyValue('display')).not.toBe('block');
                expect(window.getComputedStyle(moreMenu).getPropertyValue('visibility')).not.toBe('visible');
                expect(document.activeElement).toBe(moreMenu);
            })
        })    
    })
    
    describe('check all focusable elements give feedback when clicked directly or indirectly', () => {
        beforeEach(() => {
            document.documentElement.innerHTML = fileContents;
            // creating a contact info modal, so that its elements exist for the test
            let infoModal = document.createElement('div');
            document.body.appendChild(infoModal);
            let modalContent = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_attendee_contact_info_modal.html', 'utf-8');
            infoModal.innerHTML = modalContent;
            jest.resetModules();
            //refresh DOM variables
            ({moreMenu, moreMenuContainer, focusable, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
            modalContainers, modals, closeModalButtons, modalButtons, editProfileModalDoneButton, editProfileModal,
            openModalButtons, postEventModal, radioInputs, advertisedEvents, upcomingEvents, closeModal, linksAndButtons,
            restoreForm, postEventFormDoneButton, editProfileFormFetchHandler, postEventFormFetchHandler,
            refreshFormFetchHandler, updateEventFetchHandler, deleteEventButtons, cancelEventButtons,
            interestedEvents, attendingEvents, openModalButtonHandler, searchAdvertsButton,
            attendeeInfoButtons, attendeeContactInfoModal, hostInfoButtons, hostContactInfoModal, closeContactInfoModal} = require('../script.js'));
        })
        test('check all focusable elements give feedback when clicked', () => {
            let nonClickableElements = [...document.getElementsByClassName('event_container')];
            for (let element of uniqueFocusable) {
                if (!nonClickableElements.includes(element)) {
                    let event = new Event('mousedown');
                    element.dispatchEvent(event);
                    expect(element.classList.contains('clicked')).toBe(true);
                    event = new Event('mouseup');
                    element.dispatchEvent(event);
                    jest.runOnlyPendingTimers();
                    expect(element.classList.contains('clicked')).toBe(false);
                }
            }
        })
    })
        
    describe("check that the 'enter key' event listeners work", () => {
        beforeEach(() => {
            document.documentElement.innerHTML = fileContents;
            // creating a contact info modal, so that its elements exist for the test
            let infoModal = document.createElement('div');
            let modalContent = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_attendee_contact_info_modal.html', 'utf-8');
            document.body.appendChild(infoModal);
            infoModal.innerHTML = modalContent;
            jest.resetModules();
            //refresh DOM variables
            ({moreMenu, moreMenuContainer, focusable, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
            modalContainers, modals, closeModalButtons, modalButtons, editProfileModalDoneButton, editProfileModal,
            openModalButtons, postEventModal, radioInputs, advertisedEvents, upcomingEvents, closeModal, linksAndButtons,
            restoreForm, postEventFormDoneButton, editProfileFormFetchHandler, postEventFormFetchHandler,
            refreshFormFetchHandler, updateEventFetchHandler, deleteEventButtons, cancelEventButtons,
            interestedEvents, attendingEvents, openModalButtonHandler, searchAdvertsButton,
            attendeeInfoButtons, attendeeContactInfoModal, hostInfoButtons, hostContactInfoModal, closeContactInfoModal} = require('../script.js'));
            for (let button of closeModalButtons) {
                        // dont want to call restoreForm handler in tests
                        button.firstElementChild.removeEventListener('click', restoreForm);
                    }
            for (let button of modalButtons) {
                    if (button.getAttribute('name') === 'Cancel') {
                        // dont want to call restoreForm handler in tests
                        button.removeEventListener('click', restoreForm);
                }
            }
            // do not need these event listeners in these tests. removed to remove console errors.
            editProfileModalDoneButton.removeEventListener('click', editProfileFormFetchHandler);
            postEventFormDoneButton.removeEventListener('click', postEventFormFetchHandler);
            for (let button of deleteEventButtons) {
                button.removeEventListener('click', updateEventFetchHandler);
            }
            for ( let button of cancelEventButtons) {
                button.removeEventListener('click', updateEventFetchHandler);
            }

            // remove relevant event listeners for contact info modal elements, to keep modal existing in DOM, so all its elements exist for the test.
            document.querySelector('#attendee_contact_info span').removeEventListener('click', closeContactInfoModal);
            document.querySelector('#attendee_contact_info button').removeEventListener('click', closeContactInfoModal);

            clickSpy.mockClear();
        })
        afterEach(() => {
            for (let button of closeModalButtons) {
                button.firstElementChild.addEventListener('click', restoreForm);
    
            }
            for (let button of modalButtons) {
                if (button.getAttribute('name') === 'Cancel') {
                    button.addEventListener('click', restoreForm);
                }
            }
            editProfileModalDoneButton.addEventListener('click', editProfileFormFetchHandler);
            postEventFormDoneButton.addEventListener('click', postEventFormFetchHandler);
            for (let button of deleteEventButtons) {
                button.addEventListener('click', updateEventFetchHandler);
            }
            for ( let button of cancelEventButtons) {
                button.addEventListener('click', updateEventFetchHandler);
            }
            clickSpy.mockClear();
        })

        test('when a focusable element has focus and the enter key is pressed, the element is clicked', () => {
            let event;
            let nonClickableElements = [...document.getElementsByClassName('event_container')];
            for (let element of uniqueFocusable) {
                if (!nonClickableElements.includes(element)) {
                    event = new KeyboardEvent('keyup', {key: 'Enter', bubbles: true} );
                    clickSpy.mockClear();
                    element.dispatchEvent(event);
                    if (element.tagName !== 'BUTTON' && element.tagName !== 'A') {
                        expect(clickSpy).toHaveBeenCalledTimes(1);
                    }
                    else {
                        expect(clickSpy).toHaveBeenCalledTimes(0);
                    }
                }
            }
        })
    
        test('feedback is given when the enter key is pressed on a focused element', () => {
            let event;
            let nonClickableElements = [...document.getElementsByClassName('event_container')];
            for (let element of uniqueFocusable) {
                if (!nonClickableElements.includes(element)) {
                    event = new KeyboardEvent('keydown', {key: 'Tab'});
                    element.dispatchEvent(event);
                    expect(element.classList.contains('clicked')).toBe(false);
                    event = new KeyboardEvent('keydown', {key: 'Enter'} );    
                    element.dispatchEvent(event);
                    expect(element.classList.contains('clicked')).toBe(true);
                }                                    
            }
            for (let element of uniqueFocusable) {
                if (!nonClickableElements.includes(element)) {
                    event = new KeyboardEvent('keyup', {key: 'Tab'});
                    element.dispatchEvent(event);
                    expect(element.classList.contains('clicked')).toBe(true);
                    event = new KeyboardEvent('keyup', {key: 'Enter'} );   
                    element.dispatchEvent(event);
                    expect(element.classList.contains('clicked')).toBe(false);           
                }
            }
        })
    })
    
    describe('Test the functionality of the help text icon event listeners', ( () => {
        beforeEach(() => {
            // inline styles used to set initial display of help text elements (cannot parse stylesheet, jsdom default display 'block' for block elements)
            for (let text of helpText) {
                text.style.setProperty('display', 'none');
            }
        })
    
        test('that the field help text displays as expected, only when the mouse hovers over the icon', () => {
            const mouseEnterEvent =  new Event('mouseenter');
            const mouseLeaveEvent = new Event('mouseleave');
            for (let icon of helpTextIcons) {
                let helpTextIndex = helpTextIcons.indexOf(icon);
                expect(helpText[helpTextIndex].style.display).toBe('none');
                icon.dispatchEvent(mouseEnterEvent);
                expect(helpText[helpTextIndex].style.display).toBe('block');
                // for testing purposes, use inline style to set display: inline
                helpText[helpTextIndex].style.display = 'inline';
                icon.dispatchEvent(mouseLeaveEvent);
                // Expect to be left with jsdom block element default display: 'block'
                expect(window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display')).toBe('block');
                // expecting style attribute to have been removed
                expect(icon.hasAttribute('style')).toBe(false);
            }
        })
    
        test('that the touchstart event listeners work', () => {
            for (let icon of helpTextIcons) {
                const touchstartEvent = new Event('touchstart');
                let helpTextIndex = helpTextIcons.indexOf(icon);
                expect(helpText[helpTextIndex].style.display).toBe('none');
                icon.dispatchEvent(touchstartEvent);
                expect(helpText[helpTextIndex].style.display).toBe('block');
                // for testing purposes, use inline style to set display: inline
                helpText[helpTextIndex].style.display = 'inline';
                // testing event handler else path
                icon.dispatchEvent(touchstartEvent);
                expect(helpText[helpTextIndex].style.display).toBe('inline');
                // testing setTimeout statement of event handler
                jest.advanceTimersByTime(7000);
                expect(window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display')).toBe('inline');
                jest.advanceTimersByTime(1000);
                // expecting style attribute to have been removed
                expect(icon.hasAttribute('style')).toBe(false);
                // Expect to be left with jsdom default display: 'block'
                expect(window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display')).toBe('block');
            }
        })
    }))
    
    describe('Test that the expand less and more icons work', () => {
        // initial css styling: elements of class grid container are left with their jsdom default of 'block'
        // for the purpose of testing as oppose to 'none'. Likewise the expand_less and expand_more icons
        // will have default jsdom inline element display of ''. In reality stylesheet styling has expand_more:'inline-block', expand_less:'none'.
                
        test('that after being clicked an icon is no longer visible, whilst its counterpart becomes visible', () => {
                for (let i=0; i < expandIcons.length; ++i) {
                    if ((Boolean((i + 1) % 2))) {
                        // ith even element and zero is an expand more icon
                        let expandLessIcon = expandIcons[i].nextElementSibling;
                        expect(window.getComputedStyle(expandIcons[i]).getPropertyValue('display')).toBe('');
                        expect(window.getComputedStyle(expandLessIcon).getPropertyValue('display')).toBe('');
                    
                        expandIcons[i].click();
                        expect(window.getComputedStyle(expandIcons[i]).getPropertyValue('display')).toBe('none');
                        expect(window.getComputedStyle(expandLessIcon).getPropertyValue('display')).toBe('inline-block');
                        expandLessIcon.click();
                        expect(window.getComputedStyle(expandIcons[i]).getPropertyValue('display')).toBe('');
                        expect(window.getComputedStyle(expandLessIcon).getPropertyValue('display')).toBe('');
                    }
                }
        })
    
        test('that the grid containers become visible when the expand_more icons are clicked, and invisible when the expand_less icons are clicked', () => {
            for (let i=0; i < expandIcons.length; ++i) {
                if ((Boolean((i + 1) % 2))) {
                    // ith even element and zero is an expand more icon
                    let parentGrid = expandIcons[i].parentElement.parentElement.children[1];
                    let expandLessIcon = expandIcons[i].nextElementSibling;
                    expect(window.getComputedStyle(parentGrid).getPropertyValue('display')).toBe('block');
    
                    expandIcons[i].click();
                    expect(window.getComputedStyle(parentGrid).getPropertyValue('display')).toBe('grid');
                    expandLessIcon.click();
                    expect(window.getComputedStyle(parentGrid).getPropertyValue('display')).toBe('block');
                }
            }
        })
    
        test('that the now visible grid container receives focus after the expand icon is clicked', () => {
            for (let i=0; i < expandIcons.length; ++i) {
                if ((Boolean((i + 1) % 2))) {
                    // ith even element and zero is an expand more icon
                    let parentGrid = expandIcons[i].parentElement.parentElement.children[1];
                    expandIcons[i].click();
                    expect(document.activeElement).toBe(parentGrid);
                }
            }
        })
    })
    
    describe('Test that the open modal buttons work', () => {
        beforeEach(() => {
            for (let container of modalContainers) {
                container.style.display = 'none';
            }
            for (let button of openModalButtons) {
                button.removeEventListener('click', openModalButtonHandler);
                button.addEventListener('click', openModalButtonMockHandler);
            }  
        })
        afterEach(() => {
            for (let button of openModalButtons) {
                button.removeEventListener('click', openModalButtonMockHandler);
                button.addEventListener('click', openModalButtonHandler);
            }
            Element.prototype.scrollTo.mockClear();
        })
    
        test('that the container becomes visible, the modal gains focus, and background scrollbar is hidden', () => {
            for (let i=0; i < modalContainers.length; i++) {
                expect(window.getComputedStyle(modalContainers[i]).getPropertyValue('display')).toBe('none');
                openModalButtons[i].click();
                expect(window.getComputedStyle(modalContainers[i]).getPropertyValue('display')).toBe('block');
                expect(document.activeElement).toBe(modals[i]);
                expect(document.body.style.overflowY).toBe('hidden');
            }
        })
        
        test('that the modal is scrolled to the top when opened', () => {
            for (let i=0; i < modalContainers.length; i++) {
                // open the modal
                openModalButtons[i].click();
                expect(Element.prototype.scrollTo).toHaveBeenCalledTimes(i + 1);
                expect(Element.prototype.scrollTo).toHaveBeenLastCalledWith({
                    top: 0,
                    behaviour: 'instant'
                });
            }  
        })
    })
    
    describe("Test that the close ('X') modal buttons work (excluding fetch request). Excludes contactInfoModals", () => {
        beforeEach(() => {
            // simulate open modal containers
            for (let container of modalContainers) {
                container.style.display = 'block';
            }
            for (let button of closeModalButtons) {
                // dont want to call restoreForm handler in tests
                button.firstElementChild.removeEventListener('click', restoreForm);
            }
        })
        afterEach(() => {
            for (let button of closeModalButtons) {
                button.firstElementChild.addEventListener('click', restoreForm);
            }
        })
    
        test('that the modal container is no longer visible', () => {
            for (let button of closeModalButtons) {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                let buttonsModalContainer = button.parentElement.parentElement.parentElement;
                let clickableButtonRegion = button.firstElementChild;
                clickableButtonRegion.click();
                expect(buttonsModalContainer.hasAttribute('style')).toBe(false);
            }
        })
    
        test('that the body scrollbar is no longer hidden', () => {
            for (let button of closeModalButtons) {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                let clickableButtonRegion = button.firstElementChild;
                clickableButtonRegion.click();
                expect(document.body.hasAttribute('style')).toBe(false);
            }
        })
    
        test('that the open modal button has focus after the modal is closed', () => {
            for (let button of openModalButtons) {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                if (button.getAttribute('aria-controls') === 'edit_profile_modal') {
                    let closeButton = editProfileModal.firstElementChild.firstElementChild.firstElementChild;
                    closeButton.click();
                    jest.runAllTimers();
                    expect(document.activeElement).toBe(document.querySelector(".open_modal_button[aria-controls='edit_profile_modal']"));
                }
                else if (button.getAttribute('aria-controls') === 'post_events_modal') {
                    let closeButton = postEventModal.firstElementChild.firstElementChild.firstElementChild;
                    closeButton.click();
                    jest.runAllTimers();
                    expect(document.activeElement).toBe(document.querySelector(".open_modal_button[aria-controls='post_events_modal']")); 
                }
            }
        })
    })
    
    describe("Test that the close ('X') modal button of the contactInfoModals works", () => {
        describe("Tests for attendeeContactInfo type modals", () => {
            beforeEach(() => {
                // create modal
                let new_modal_container = document.createElement('div');
                document.getElementById('post_events').firstElementChild.before(new_modal_container);
                new_modal_container.classList.add('modal_container');
                new_modal_container.setAttribute('tabindex', '0');
                new_modal_container.setAttribute('style', "display:block;")
                new_modal_container.innerHTML = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_attendee_contact_info_modal.html', 'utf-8');
                new_modal_container.innerHTML = new_modal_container.firstElementChild.innerHTML;
            })
            test('that the modal container no longer exists in the DOM', () => {
                // check modal exists in DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).not.toBe(null);
                // simulate close modal button click event
                let closeModalButton = attendeeContactInfoModal.querySelector('.close_button');
                let clickableButtonRegion = closeModalButton.firstElementChild;
                let event = {currentTarget: clickableButtonRegion};
                closeContactInfoModal(event);
                // check modal has been removed from the DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).toBe(null);
            })
    
            test('that the body scrollbar is no longer hidden', () => {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                // check modal exists in DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).not.toBe(null);
                // simulate close modal button click event
                let closeModalButton = attendeeContactInfoModal.querySelector('.close_button');
                let clickableButtonRegion = closeModalButton.firstElementChild;
                let event = {currentTarget: clickableButtonRegion};
                closeContactInfoModal(event);
                // check scrollbar is not hidden
                expect(document.body.hasAttribute('style')).toBe(false);
            })
    
            test('that the related attendee_info button has focus after the modal is closed', () => {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                // check modal exists in DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).not.toBe(null);
                // simulate close modal button click event
                let closeModalButton = attendeeContactInfoModal.querySelector('.close_button');
                let clickableButtonRegion = closeModalButton.firstElementChild;
                let event = {currentTarget: clickableButtonRegion};
                closeContactInfoModal(event);
                jest.runOnlyPendingTimers();
                expect(radioInputs[3].checked).toBe(true);
                expect(document.activeElement).toBe(attendeeInfoButtons[0]);
            })
        })
        
        describe("Tests for hostContactInfo type modals", () => {
            beforeEach(() => {
                // create modal
                let new_modal_container = document.createElement('div');
                document.getElementById('search_events').firstElementChild.before(new_modal_container);
                new_modal_container.classList.add('modal_container');
                new_modal_container.setAttribute('tabindex', '0');
                new_modal_container.setAttribute('style', "display:block;")
                new_modal_container.innerHTML = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_host_contact_info_modal.html', 'utf-8');
                new_modal_container.innerHTML = new_modal_container.firstElementChild.innerHTML;
            })
    
            test('that the modal container for a hostContactInfo type modal no longer exists in the DOM', () => {
                // check modal exists in DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).not.toBe(null);            
                // simulate close modal button click event
                let closeModalButton = hostContactInfoModal.querySelector('.close_button');
                let clickableButtonRegion = closeModalButton.firstElementChild;
                let event = {currentTarget: clickableButtonRegion};
                closeContactInfoModal(event);
                // check modal has been removed from the DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).toBe(null);
            })
    
            test('that the body scrollbar is no longer hidden', () => {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                // check modal exists in DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).not.toBe(null);            
                // simulate close modal button click event
                let closeModalButton = hostContactInfoModal.querySelector('.close_button');
                let clickableButtonRegion = closeModalButton.firstElementChild;
                let event = {currentTarget: clickableButtonRegion};
                closeContactInfoModal(event);
                // check scrollbar is not hidden
                expect(document.body.hasAttribute('style')).toBe(false);
            })
    
            test('that the related host_info button has focus after the modal is closed', () => {
                // check modal exists in DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).not.toBe(null);            
                // simulate close modal button click event
                let closeModalButton = hostContactInfoModal.querySelector('.close_button');
                let clickableButtonRegion = closeModalButton.firstElementChild;
                let event = {currentTarget: clickableButtonRegion};
                closeContactInfoModal(event);
                jest.runAllTimers();
                expect(radioInputs[1].checked).toBe(true);
                expect(document.activeElement).toBe(hostInfoButtons[0]);
            })
        })
    })

    describe("Test that the close (bottom button) modal button of the contactInfoModals works", () => {
        describe("Tests for attendeeContactInfo type modals", () => {
            beforeEach(() => {
                // create modal
                let new_modal_container = document.createElement('div');
                document.getElementById('post_events').firstElementChild.before(new_modal_container);
                new_modal_container.classList.add('modal_container');
                new_modal_container.setAttribute('tabindex', '0');
                new_modal_container.setAttribute('style', "display:block;")
                new_modal_container.innerHTML = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_attendee_contact_info_modal.html', 'utf-8');
                new_modal_container.innerHTML = new_modal_container.firstElementChild.innerHTML;
            })
            test('that the modal container no longer exists in the DOM', () => {
                // check modal exists in DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).not.toBe(null);
                // simulate close modal button click event
                let closeModalButton = attendeeContactInfoModal.querySelector('.modal_button');
                let event = {currentTarget: closeModalButton};
                closeContactInfoModal(event);
                // check modal has been removed from the DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).toBe(null);
            })
    
            test('that the body scrollbar is no longer hidden', () => {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                // check modal exists in DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).not.toBe(null);
                // simulate close modal button click event
                let closeModalButton = attendeeContactInfoModal.querySelector('.modal_button');
                let event = {currentTarget: closeModalButton};
                closeContactInfoModal(event);
                // check scrollbar is not hidden
                expect(document.body.hasAttribute('style')).toBe(false);
            })
    
            test('that the related attendee_info button has focus after the modal is closed', () => {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                // check modal exists in DOM
                attendeeContactInfoModal = document.getElementById('attendee_contact_info');
                expect(attendeeContactInfoModal).not.toBe(null);
                // simulate close modal button click event
                let closeModalButton = attendeeContactInfoModal.querySelector('.modal_button');
                let event = {currentTarget: closeModalButton};
                closeContactInfoModal(event);
                jest.runOnlyPendingTimers();
                expect(radioInputs[3].checked).toBe(true);
                expect(document.activeElement).toBe(attendeeInfoButtons[0]);
            })
        })
        
        describe("Tests for hostContactInfo type modals", () => {
            beforeEach(() => {
                // create modal
                let new_modal_container = document.createElement('div');
                document.getElementById('search_events').firstElementChild.before(new_modal_container);
                new_modal_container.classList.add('modal_container');
                new_modal_container.setAttribute('tabindex', '0');
                new_modal_container.setAttribute('style', "display:block;")
                new_modal_container.innerHTML = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_host_contact_info_modal.html', 'utf-8');
                new_modal_container.innerHTML = new_modal_container.firstElementChild.innerHTML;
            })
    
            test('that the modal container for a hostContactInfo type modal no longer exists in the DOM', () => {
                // check modal exists in DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).not.toBe(null);            
                // simulate close modal button click event
                let closeModalButton = hostContactInfoModal.querySelector('.modal_button');
                let event = {currentTarget: closeModalButton};
                closeContactInfoModal(event);
                // check modal has been removed from the DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).toBe(null);
            })
    
            test('that the body scrollbar is no longer hidden', () => {
                // scrollbar is hidden when a modal is open.
                document.body.style.overflowY = 'hidden';
                // check modal exists in DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).not.toBe(null);            
                // simulate close modal button click event
                let closeModalButton = hostContactInfoModal.querySelector('.modal_button');
                let event = {currentTarget: closeModalButton};
                closeContactInfoModal(event);
                // check scrollbar is not hidden
                expect(document.body.hasAttribute('style')).toBe(false);
            })
    
            test('that the related host_info button has focus after the modal is closed', () => {
                // check modal exists in DOM
                hostContactInfoModal = document.getElementById('host_contact_info');
                expect(hostContactInfoModal).not.toBe(null);            
                // simulate close modal button click event
                let closeModalButton = hostContactInfoModal.querySelector('.modal_button');
                let event = {currentTarget: closeModalButton};
                closeContactInfoModal(event);
                jest.runAllTimers();
                expect(radioInputs[1].checked).toBe(true);
                expect(document.activeElement).toBe(hostInfoButtons[0]);
            })
        })
    })
    
    describe('Test that Done modal buttons work (excluding fetch requests)', () => {
        beforeEach(() => {
            // simulate open modal containers
            for (let container of modalContainers) {
                container.style.display = 'block';
            }
            // replacing fetch listeners with mock handlers
            editProfileModalDoneButton.removeEventListener('click', editProfileFormFetchHandler);
            postEventFormDoneButton.removeEventListener('click', postEventFormFetchHandler);
            editProfileModalDoneButton.addEventListener('click', mockFetchEditProfile);
            postEventFormDoneButton.addEventListener('click', mockFetchEvent);
        })
        afterEach(() => {
            // replacing listeners with original fetch handlers
            editProfileModalDoneButton.removeEventListener('click', mockFetchEditProfile);
            postEventFormDoneButton.removeEventListener('click', mockFetchEvent);
            editProfileModalDoneButton.addEventListener('click', editProfileFormFetchHandler);
            postEventFormDoneButton.addEventListener('click', postEventFormFetchHandler);
        })
    
        test('that the modal container is no longer visible', () => {
            for (let button of modalButtons) {
                mockFetchEditProfile.mockClear();
                mockFetchEvent.mockClear();
                if (button.getAttribute('name') === 'Done') {
                    // scrollbar is hidden when a modal is open.
                    document.body.style.overflowY = 'hidden';
                    let buttonModalContainer = button.parentElement.parentElement.parentElement;
                    expect(buttonModalContainer.hasAttribute('style')).toBe(true);
                    button.click();
                    if (button.parentElement.parentElement.id === 'edit_profile_modal') {
                        expect(mockFetchEditProfile).toHaveBeenCalledTimes(1);
                    }
                    else {
                        expect(mockFetchEvent).toHaveBeenCalledTimes(1);
                    }
                    expect(buttonModalContainer.hasAttribute('style')).toBe(false);
                }
            }
        })
    
        test('that the body scrollbar is no longer hidden', () => {
            for (let button of modalButtons) {
                if (button.getAttribute('name') === 'Done') {
                    // scrollbar is hidden when a modal is open.
                    document.body.style.overflowY = 'hidden';
                    button.click();
                    expect(document.body.hasAttribute('style')).toBe(false);
                }
            }    
        })
    
        test('that the open modal button has focus after the modal is closed', () => {
            let openEditProfileButton;
            let openPostEventsButton;
            for (let button of openModalButtons) {
                if (button.getAttribute('aria-controls') === 'edit_profile_modal') {
                    openEditProfileButton = button;
                }
                else if (button.getAttribute('aria-controls') === 'post_events_modal') {
                    openPostEventsButton = button
                }
            }
            // Edit Profile modal done button tests:
    
            // scrollbar is hidden when a modal is open.
            document.body.style.overflowY = 'hidden';
            editProfileModalDoneButton.click();
            jest.runAllTimers();
            expect(document.activeElement).toBe(openEditProfileButton);
    
            // post event modal done button tests:
    
            // scrollbar is hidden when a modal is open.
            document.body.style.overflowY = 'hidden';
            postEventFormDoneButton.click();
            jest.runAllTimers();
            expect(document.activeElement).toBe(openPostEventsButton);
        })
    })
    
    describe("Test that the 'trap focus within open modal' event listeners work", () => {
        test('the modal is given focus when its last button loses focus', () => {
           for (let modal of modals) {
            let modalId = modal.id;
            let querySelector = '#' + modalId + ' button';
            let lastButtonInModal = [...document.querySelectorAll(querySelector)].pop();
            let blurEvent = new Event('blur');
            lastButtonInModal.dispatchEvent(blurEvent);
            expect(document.activeElement).toBe(modal);
           }
        })
        test('the modal is given focus when its modal container gains focus', () => {
            for (let modal of modals) {
             let parentModalContainer = modal.parentElement
             let focusEvent = new Event('focus');
             parentModalContainer.dispatchEvent(focusEvent);
             expect(document.activeElement).toBe(modal);
            }
         })
    })
    
    describe('Test that the cancel modal buttons work', () => {
        beforeEach(() => {
            // simulate open modal containers
            for (let container of modalContainers) {
                container.style.display = 'block';
            }
            for (let button of modalButtons) {
                    if (button.getAttribute('name') === 'Cancel') {
                        // dont want to call restoreForm handler in tests
                        button.removeEventListener('click', restoreForm);
                    }
            }
        })
        afterEach(() => {
            for (let button of modalButtons) {
                    if (button.getAttribute('name') === 'Cancel') {
                        button.addEventListener('click', restoreForm);
                    }
            }
        })
    
        test('that the modal container is no longer visible', () => {
            for (let button of modalButtons) {
                if (button.getAttribute('name') === 'Cancel') {
                    // scrollbar is hidden when a modal is open.
                    document.body.style.overflowY = 'hidden';
                    let buttonModalContainer = button.parentElement.parentElement;
                    button.click();
                    expect(buttonModalContainer.hasAttribute('style')).toBe(false);
                }
            }
        })
    
        test('that the body scrollbar is no longer hidden', () => {
            for (let button of modalButtons) {
                if (button.getAttribute('name') === 'Cancel') {
                    // scrollbar is hidden when a modal is open.
                    document.body.style.overflowY = 'hidden';
                    button.click();
                    expect(document.body.hasAttribute('style')).toBe(false);
                }
            }    
        })
    
        test('that the open modal button has focus after the modal is closed', () => {
            let openEditProfileButton;
            let openPostEventsButton;
            for (let button of openModalButtons) {
                if (button.getAttribute('aria-controls') === 'edit_profile_modal') {
                    openEditProfileButton = button;
                }
                else if (button.getAttribute('aria-controls') === 'post_events_modal') {
                    openPostEventsButton = button
                }
            }
            // Edit Profile modal cancel button tests:
    
            // scrollbar is hidden when a modal is open.
            document.body.style.overflowY = 'hidden';
            editProfileModalDoneButton.nextElementSibling.click();
            setTimeout(() => {expect(document.activeElement).toBe(openEditProfileButton)}, 100);
            
            
            // post event modal cancel button tests:
    
            // scrollbar is hidden when a modal is open.
            document.body.style.overflowY = 'hidden';
            postEventFormDoneButton.nextElementSibling.click();
            setTimeout(() => {expect(document.activeElement).toBe(openPostEventsButton)}, 100);
            
        })
    })
    
    describe('test that the search events section radio input affects the events displayed', () => {
        test('that toggling the selected radio input changes the types of events displayed', () => {
            let interestedOption = radioInputs[0];
            let upcomingOption = radioInputs[1];
            // interested is checked on page load.
            expect(interestedOption.checked).toBe(true);
            for (let event of interestedEvents) {
                expect(event.classList.contains('hidden')).toBe(false);
            }
            for (let event of attendingEvents) {
                expect(event.classList.contains('hidden')).toBe(true);
            }
            upcomingOption.click();
            for (let event of interestedEvents) {
                expect(event.classList.contains('hidden')).toBe(true);
            }
            for (let event of attendingEvents) {
                expect(event.classList.contains('hidden')).toBe(false);
            }
            interestedOption.click();
            for (let event of interestedEvents) {
                expect(event.classList.contains('hidden')).toBe(false);
            }
            for (let event of attendingEvents) {
                expect(event.classList.contains('hidden')).toBe(true);
            }
        })
    })
    
    describe('test that the post events section radio input affects the events displayed', () => {
        test('that toggling the selected radio input changes the types of events displayed', () => {
            let advertsiedOption = radioInputs[2];
            let upcomingOption = radioInputs[3];
            // advertised is checked on page load.
            expect(advertsiedOption.checked).toBe(true);
            for (let event of advertisedEvents) {
                expect(event.classList.contains('hidden')).toBe(false);
            }
            for (let event of upcomingEvents) {
                expect(event.classList.contains('hidden')).toBe(true);
            }
            upcomingOption.click();
            for (let event of advertisedEvents) {
                expect(event.classList.contains('hidden')).toBe(true);
            }
            for (let event of upcomingEvents) {
                expect(event.classList.contains('hidden')).toBe(false);
            }
            advertsiedOption.click();
            for (let event of advertisedEvents) {
                expect(event.classList.contains('hidden')).toBe(false);
            }
            for (let event of upcomingEvents) {
                expect(event.classList.contains('hidden')).toBe(true);
            }
        })
    })
    
    describe('check search adverts button works', () => {
        const originalLocation = window.location;
        beforeEach(() => {
            delete window.location;
            window.location = {
                href: 'home/',
                assign: jest.fn((url) => {
                    return url;
                })
            }
        })
    
        afterEach(() => {
            window.location = originalLocation;
        })
    
        test('that clicking the button redirects the user to the search event adverts page', () => {
            expect(window.location.assign).toHaveBeenCalledTimes(0);
            searchAdvertsButton.click();
            expect(window.location.assign).toHaveBeenCalledTimes(1);
            expect(window.location.assign).toHaveBeenCalledWith('events_and_activities/search_event_adverts/');
        })
    })
})