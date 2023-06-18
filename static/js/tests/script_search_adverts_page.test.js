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
clickSpy = jest.spyOn(HTMLElement.prototype, 'click');
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
    beforeAll(() => {
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
    })
    afterAll(() => {
        for (let button of closeModalButtons) {
            button.firstElementChild.addEventListener('click', restoreForm);

        }
        for (let button of modalButtons) {
            if (button.getAttribute('name') === 'Cancel') {
                button.addEventListener('click', restoreForm);
            }
        }
        clickSpy.mockClear();
    })

    beforeEach(() => {
        clickSpy.mockClear();
    })

    test('when a focusable element has focus and the enter key is pressed, the element is clicked', () => {
        let event;
        let nonClickableElements = [...document.getElementsByClassName('event_container')];
        for (let element of uniqueFocusable) {
            if (!nonClickableElements.includes(element)) {
                event = new KeyboardEvent('keyup', {key: 'Enter'} );
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

test('that the grid containers, containing the event advert data are visible on loading', () => {
    for (let container of gridContainers) {
        expect(container.style.display).toBe('grid')
    }
})