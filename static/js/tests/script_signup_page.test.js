/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
// Adds rendered signup_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_signup_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, openMenu, closeMenu, slideshowImages, uniqueFocusable, helpTextIcons, helpText, matchingIcons} = require('../script.js');
// mock functions
clickSpy = jest.spyOn(HTMLElement.prototype, 'click');

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
        beforeEach(() => {
            clickSpy.mockClear();
        })
    
        test('when a focusable element has focus and the enter key is pressed, the element is clicked', () => {
            let event;
            for (let element of uniqueFocusable) {
                clickSpy.mockClear();
                event = new KeyboardEvent('keyup', {key: 'Enter'} );
                element.dispatchEvent(event);
                if (element.tagName !== 'BUTTON' && element.tagName !== 'A') {
                    expect(clickSpy).toHaveBeenCalledTimes(1);
                }
                else {
                    expect(clickSpy).toHaveBeenCalledTimes(0);
                }
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

describe('Test the functionality of the typed/retyped input field pair event listeners', () => {
    beforeEach(() => {
        const noMatchIcons = [...document.getElementsByClassName('no_match_icon')];
        // inline styles used to set initial display of matching/no-match icons
        for (let icon of matchingIcons) {
            icon.style.display = 'inline';
        }
        for (let icon of noMatchIcons) {
            icon.style.display = 'none';
        }
        // set initial input field values
        for (let matchingIcon of matchingIcons) {
            let secondField = matchingIcon.parentElement.firstElementChild.children[1];
            let firstField = matchingIcon.parentElement.previousElementSibling.firstElementChild.children[1];
            firstField.value, secondField.value = '';
        }
    })

    test('that the correct icon displays in response to field input value changes', () => {
        function inner(firstField, secondField, firstFieldValue, secondFieldValue) {
            firstFieldValue ? firstField.value = firstFieldValue : '';
            secondFieldValue ? secondField.value = secondFieldValue : '';
            const inputEvent = new Event('input');
            firstFieldValue ? firstField.dispatchEvent(inputEvent) : secondField.dispatchEvent(inputEvent);
        }

        for (let matchingIcon of matchingIcons) {
            let noMatchIcon = matchingIcon.nextElementSibling;
            let secondField = matchingIcon.parentElement.firstElementChild.children[1];
            let firstField = matchingIcon.parentElement.previousElementSibling.firstElementChild.children[1];
            // fields empty and thus matching
            inner(firstField, secondField, '', '');
            expect(matchingIcon.style.display).toBe('inline');
            expect(noMatchIcon.style.display).toBe('none');
            // change first field value only: no match
            inner(firstField, secondField, 'f', '');
            expect(matchingIcon.style.display).toBe('none');
            expect(noMatchIcon.style.display).toBe('inline');
            // change second field value only to match again
            inner(firstField, secondField, '', 'f');
            expect(matchingIcon.hasAttribute('style')).toBe(false);
            expect(noMatchIcon.hasAttribute('style')).toBe(false);
            // change second field value only: no match
            inner(firstField, secondField, '', 'g');
            expect(matchingIcon.style.display).toBe('none');
            expect(noMatchIcon.style.display).toBe('inline');
            //change first field value only to match again
            inner(firstField, secondField, 'g', '');
            expect(matchingIcon.hasAttribute('style')).toBe(false);
            expect(noMatchIcon.hasAttribute('style')).toBe(false);           
        }
    })
})