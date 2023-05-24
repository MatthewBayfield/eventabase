/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
// Adds rendered home_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_search_adverts_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, uniqueFocusable, helpTextIcons, helpText, expandIcons,
     modalContainers, modals, closeModalButtons, modalButtons, openModalButtons, advertisedEvents, closeModal,
     restoreForm, refreshFormFetchHandler, updateEventFetchHandler, openModalButtonHandler,
     gridContainers} = require('../script.js');
// mock functions
const log = jest.fn();
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
    const click = (event) => {log(event.target)};
    beforeAll(() => {
        for (let element of uniqueFocusable) {
            element.addEventListener('click', click);
        }
        // for (let button of closeModalButtons) {
        //             // dont want to call restoreForm handler in tests
        //             button.firstElementChild.removeEventListener('click', restoreForm);
        //         }
        // for (let button of modalButtons) {
        //         if (button.getAttribute('name') === 'Cancel') {
        //             // dont want to call restoreForm handler in tests
        //             button.removeEventListener('click', restoreForm);
        //     }
        // }
        // // do not need these event listeners in these tests. removed to remove console errors.
        // editProfileModalDoneButton.removeEventListener('click', editProfileFormFetchHandler);
        // postEventFormDoneButton.removeEventListener('click', postEventFormFetchHandler);
        // for (let button of deleteEventButtons) {
        //     button.removeEventListener('click', updateEventFetchHandler);
        // }
        // for ( let button of cancelEventButtons) {
        //     button.removeEventListener('click', updateEventFetchHandler);
        // }

    })
    afterAll(() => {
        for (let element of uniqueFocusable) {
            element.removeEventListener('click', click);
        }
        // for (let button of closeModalButtons) {
        //     button.firstElementChild.addEventListener('click', restoreForm);

        // }
        // for (let button of modalButtons) {
        //     if (button.getAttribute('name') === 'Cancel') {
        //         button.addEventListener('click', restoreForm);
        //     }
        // }
        // editProfileModalDoneButton.addEventListener('click', editProfileFormFetchHandler);
        // postEventFormDoneButton.addEventListener('click', postEventFormFetchHandler);
        // for (let button of deleteEventButtons) {
        //     button.addEventListener('click', updateEventFetchHandler);
        // }
        // for ( let button of cancelEventButtons) {
        //     button.addEventListener('click', updateEventFetchHandler);
        // }
        log.mockClear();
    })

    test('when a focusable element has focus and the enter key is pressed, the element is clicked', () => {
        let event;
        let nonClickableElements = [...document.getElementsByClassName('event_container')];
        for (let element of uniqueFocusable) {
            if (!nonClickableElements.includes(element)) {
                event = new KeyboardEvent('keyup', {key: 'Enter'} );
                log.mockClear();
                element.dispatchEvent(event);
                expect(log).toHaveBeenCalledWith(element);
                log.mockClear();
                event = new KeyboardEvent('keyup', {key: 'Tab'});
                element.dispatchEvent(event);
                expect(log).not.toHaveBeenCalledWith(element);
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

test('that the grid containers, containing the event advert data are visible on loading', () => {
    for (let container of gridContainers) {
        expect(container.style.display).toBe('grid')
    }
})

// describe('Test that the open modal buttons work', () => {
//     beforeEach(() => {
//         for (let container of modalContainers) {
//             container.style.display = 'none';
//         }
//         for (let button of openModalButtons) {
//             button.removeEventListener('click', openModalButtonHandler);
//             button.addEventListener('click', openModalButtonMockHandler);
//         }  
//     })
//     afterEach(() => {
//         for (let button of openModalButtons) {
//             button.removeEventListener('click', openModalButtonMockHandler);
//             button.addEventListener('click', openModalButtonHandler);
//         }
//         Element.prototype.scrollTo.mockClear();
//     })

//     test('that the container becomes visible, the modal gains focus, and background scrollbar is hidden', () => {
//         for (let i=0; i < modalContainers.length; i++) {
//             expect(window.getComputedStyle(modalContainers[i]).getPropertyValue('display')).toBe('none');
//             openModalButtons[i].click();
//             expect(window.getComputedStyle(modalContainers[i]).getPropertyValue('display')).toBe('block');
//             expect(document.activeElement).toBe(modals[i]);
//             expect(document.body.style.overflowY).toBe('hidden');
//         }
//     })
    
//     test('that the modal is scrolled to the top when opened', () => {
//         for (let i=0; i < modalContainers.length; i++) {
//             // open the modal
//             openModalButtons[i].click();
//             expect(Element.prototype.scrollTo).toHaveBeenCalledTimes(i + 1);
//             expect(Element.prototype.scrollTo).toHaveBeenLastCalledWith({
//                 top: 0,
//                 behaviour: 'instant'
//             });
//         }  
//     })
// })

// describe('Test that the close modal buttons work (excluding fetch request)', () => {
//     beforeEach(() => {
//         // simulate open modal containers
//         for (let container of modalContainers) {
//             container.style.display = 'block';
//         }
//     })  
//     beforeAll(() => {
//         for (let button of closeModalButtons) {
//             // dont want to call restoreForm handler in tests
//             button.firstElementChild.removeEventListener('click', restoreForm);
//         }
//     })
//     afterAll(() => {
//         for (let button of closeModalButtons) {
//             button.firstElementChild.addEventListener('click', restoreForm);
//         }
//     })

//     test('that the modal container is no longer visible', () => {
//         for (let button of closeModalButtons) {
//             // scrollbar is hidden when a modal is open.
//             document.body.style.overflowY = 'hidden';
//             let buttonsModalContainer = button.parentElement.parentElement.parentElement;
//             let clickableButtonRegion = button.firstElementChild;
//             clickableButtonRegion.click();
//             expect(buttonsModalContainer.hasAttribute('style')).toBe(false);
//         }
//     })

//     test('that the body scrollbar is no longer hidden', () => {
//         for (let button of closeModalButtons) {
//             // scrollbar is hidden when a modal is open.
//             document.body.style.overflowY = 'hidden';
//             let clickableButtonRegion = button.firstElementChild;
//             clickableButtonRegion.click();
//             expect(document.body.hasAttribute('style')).toBe(false);
//         }
//     })

//     test('that the open modal button has focus after the modal is closed', () => {
//         for (let button of openModalButtons) {
//             // scrollbar is hidden when a modal is open.
//             document.body.style.overflowY = 'hidden';
//             if (button.getAttribute('aria-controls') === 'edit_profile_modal') {
//                 let closeButton = editProfileModal.firstElementChild.firstElementChild.firstElementChild;
//                 closeButton.click();
//                 expect(document.activeElement).toBe(document.querySelector(".open_modal_button[aria-controls='edit_profile_modal']"));
//             }
//             else if (button.getAttribute('aria-controls') === 'post_events_modal') {
//                 let closeButton = postEventModal.firstElementChild.firstElementChild.firstElementChild;
//                 closeButton.click();
//                 expect(document.activeElement).toBe(document.querySelector(".open_modal_button[aria-controls='post_events_modal']"));
//             }
//         }
//     })
// })


// describe("Test that the 'trap focus within open modal' event listeners work", () => {
//     test('the modal is given focus when its last button loses focus', () => {
//        for (let modal of modals) {
//         let modalId = modal.id;
//         let querySelector = '#' + modalId + ' button';
//         let lastButtonInModal = [...document.querySelectorAll(querySelector)].pop();
//         let blurEvent = new Event('blur');
//         lastButtonInModal.dispatchEvent(blurEvent);
//         expect(document.activeElement).toBe(modal);
//        }
//     })
//     test('the modal is given focus when its modal container gains focus', () => {
//         for (let modal of modals) {
//          let parentModalContainer = modal.parentElement
//          let focusEvent = new Event('focus');
//          parentModalContainer.dispatchEvent(focusEvent);
//          expect(document.activeElement).toBe(modal);
//         }
//      })
// })

// describe('Test that the cancel modal buttons work', () => {
//     beforeEach(() => {
//         // simulate open modal containers
//         for (let container of modalContainers) {
//             container.style.display = 'block';
//         }
//     })
//     beforeAll(() => {
//         for (let button of modalButtons) {
//                 if (button.getAttribute('name') === 'Cancel') {
//                     // dont want to call restoreForm handler in tests
//                     button.removeEventListener('click', restoreForm);
//                 }
//         }
//     })
//     afterAll(() => {
//         for (let button of modalButtons) {
//                 if (button.getAttribute('name') === 'Cancel') {
//                     button.addEventListener('click', restoreForm);
//                 }
//         }
//     })

//     test('that the modal container is no longer visible', () => {
//         for (let button of modalButtons) {
//             if (button.getAttribute('name') === 'Cancel') {
//                 // scrollbar is hidden when a modal is open.
//                 document.body.style.overflowY = 'hidden';
//                 let buttonModalContainer = button.parentElement.parentElement;
//                 button.click();
//                 expect(buttonModalContainer.hasAttribute('style')).toBe(false);
//             }
//         }
//     })

//     test('that the body scrollbar is no longer hidden', () => {
//         for (let button of modalButtons) {
//             if (button.getAttribute('name') === 'Cancel') {
//                 // scrollbar is hidden when a modal is open.
//                 document.body.style.overflowY = 'hidden';
//                 button.click();
//                 expect(document.body.hasAttribute('style')).toBe(false);
//             }
//         }    
//     })

//     test('that the open modal button has focus after the modal is closed', () => {
//         let openEditProfileButton;
//         let openPostEventsButton;
//         for (let button of openModalButtons) {
//             if (button.getAttribute('aria-controls') === 'edit_profile_modal') {
//                 openEditProfileButton = button;
//             }
//             else if (button.getAttribute('aria-controls') === 'post_events_modal') {
//                 openPostEventsButton = button
//             }
//         }
//         // Edit Profile modal cancel button tests:

//         // scrollbar is hidden when a modal is open.
//         document.body.style.overflowY = 'hidden';
//         editProfileModalDoneButton.nextElementSibling.click();
//         expect(document.activeElement).toBe(openEditProfileButton);
        
//         // post event modal cancel button tests:

//         // scrollbar is hidden when a modal is open.
//         document.body.style.overflowY = 'hidden';
//         postEventFormDoneButton.nextElementSibling.click();
//         expect(document.activeElement).toBe(openPostEventsButton);
//     })
// })
