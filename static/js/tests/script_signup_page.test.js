/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
const { expect } = require('expect');
// Adds rendered signup_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_signup_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, openMenu, closeMenu, slideshowImages, uniqueFocusable, helpTextIcons, helpText} = require('../script.js');
// mock functions
const log = jest.fn();

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
        for (let element of uniqueFocusable) {
            let event = new Event('mousedown');
            element.dispatchEvent(event);
            expect(element.classList.contains('clicked')).toBe(true);
            event = new Event('mouseup');
            element.dispatchEvent(event);
            jest.runOnlyPendingTimers();
            expect(element.classList.contains('clicked')).toBe(false);
        }
    })
    
    describe("check that the 'enter key' event listeners work", () => {
        const click = (event) => {log(event.target)};
        beforeAll(() => {
            for (let element of uniqueFocusable) {
                element.addEventListener('click', click);
            }
        })
        afterAll(() => {
            for (let element of uniqueFocusable) {
                element.removeEventListener('click', click);
            }
            log.mockClear();
        })
    
        test('when a focusable element has focus and the enter key is pressed, the element is clicked', () => {
            let event;
            for (let element of uniqueFocusable) {
                event = new KeyboardEvent('keyup', {key: 'Enter'} );
                log.mockClear();
                element.dispatchEvent(event);
                expect(log).toHaveBeenCalledWith(element);
                log.mockClear();
                event = new KeyboardEvent('keyup', {key: 'Tab'});
                element.dispatchEvent(event);
                expect(log).not.toHaveBeenCalledWith(element);

            }
        })
    
        test('feedback is given when the enter key is pressed on a focused element', () => {
            let event;
            for (let element of uniqueFocusable) {
                event = new KeyboardEvent('keydown', {key: 'Tab'});
                element.dispatchEvent(event);
                expect(element.classList.contains('clicked')).toBe(false);
                event = new KeyboardEvent('keydown', {key: 'Enter'} );    
                element.dispatchEvent(event);
                expect(element.classList.contains('clicked')).toBe(true);
                                    
            }
            for (let element of uniqueFocusable) {
                event = new KeyboardEvent('keyup', {key: 'Tab'});
                element.dispatchEvent(event);
                expect(element.classList.contains('clicked')).toBe(true);
                event = new KeyboardEvent('keyup', {key: 'Enter'} );   
                element.dispatchEvent(event);
                expect(element.classList.contains('clicked')).toBe(false);                  
            }
        })
    })
})

describe('Test the functionality of the help text icon event listeners', ( () => {
    beforeEach(() => {
        // inline styles used to set initial display of help text elements (jsdom initial element display is always 'block')
        for (let text of helpText) {
            text.style.setProperty('display', 'none');
        }
        // inline styles used to set initial help icon css properties
        for (let icon of helpTextIcons) {
            icon.style.setProperty('align-self', 'end')
        }
    })

    test('that the field help text displays as expected, only when the mouse hovers over the icon', () => {
        const mouseEnterEvent =  new Event('mouseenter');
        const mouseLeaveEvent = new Event('mouseleave');
        for (let icon of helpTextIcons) {
            expect(icon.style.getPropertyValue('align-self')).toBe('end')
            let helpTextIndex = helpTextIcons.indexOf(icon);
            expect(helpText[helpTextIndex].style.display).toBe('none');
            icon.dispatchEvent(mouseEnterEvent);
            expect(helpText[helpTextIndex].style.display).toBe('block');
            expect(icon.style.getPropertyValue('align-self')).toBe('start');
            // for testing purposes, use inline style to set display: inline
            helpText[helpTextIndex].style.display = 'inline';
            icon.dispatchEvent(mouseLeaveEvent);
            // Expect to be left with jsdom default display: 'block'
            expect(window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display')).toBe('block');
            // expecting style attribute to have been removed
            expect(icon.hasAttribute('style')).toBe(false);
        }
    })

    test('that the touchstart event listeners work', () => {
        for (let icon of helpTextIcons) {
            const touchstartEvent = new Event('touchstart');
            let helpTextIndex = helpTextIcons.indexOf(icon);
            expect(icon.style.getPropertyValue('align-self')).toBe('end')
            expect(helpText[helpTextIndex].style.display).toBe('none');
            icon.dispatchEvent(touchstartEvent);
            expect(icon.style.getPropertyValue('align-self')).toBe('start');
            expect(helpText[helpTextIndex].style.display).toBe('block');
            // for testing purposes, use inline style to set display: inline
            helpText[helpTextIndex].style.display = 'inline';
            // testing event handler else path
            icon.dispatchEvent(touchstartEvent);
            expect(helpText[helpTextIndex].style.display).toBe('inline');
            // testing setTimeout statement of event handler
            jest.advanceTimersByTime(7000);
            expect(icon.style.getPropertyValue('align-self')).toBe('start');
            expect(window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display')).toBe('inline');
            jest.advanceTimersByTime(1000);
            // expecting style attribute to have been removed
            expect(icon.hasAttribute('style')).toBe(false);
            // Expect to be left with jsdom default display: 'block'
            expect(window.getComputedStyle(helpText[helpTextIndex]).getPropertyValue('display')).toBe('block');
        }
    })
}))