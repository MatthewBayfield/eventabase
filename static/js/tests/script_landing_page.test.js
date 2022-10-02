/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
// Adds rendered landing_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/tests/html_content_for_js_tests/rendered_landing_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, openMenu, closeMenu, slideshowImages, uniqueFocusable} = require('../script.js');
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

describe('Test that the image slideshow functions as expected', () => {
    let imagesInToSlideshow = 1;
    let imagesNotYetDisplayed = [...slideshowImages];
    let lastImageDisplayed;
    for (let index = 1; index <= slideshowImages.length; index++) {
        test(`check after ${imagesInToSlideshow} images in to slideshow, the next image due becomes visible (incl for screen readers)`, () => {
            const elementsWithClassCurrentImage = [...document.getElementsByClassName('current_image')];
            const arrayLength = elementsWithClassCurrentImage.length;
            const currentImageIndex = slideshowImages.indexOf(elementsWithClassCurrentImage[arrayLength - 1]);
            nextImageIndex = currentImageIndex === slideshowImages.length - 1 ? 0 : currentImageIndex + 1;
            jest.runOnlyPendingTimers();
            expect(slideshowImages[nextImageIndex].classList.contains('current_image'));
            expect(arrayLength).toBe(1);
            expect(slideshowImages[nextImageIndex].getAttribute('aria-hidden')).toBe('false');
            expect(document.querySelectorAll('[aria-hidden="false"]').length).toBe(1);
            expect(imagesNotYetDisplayed).toContain(slideshowImages[nextImageIndex]);
            lastImageDisplayed = imagesNotYetDisplayed.splice(imagesNotYetDisplayed.indexOf(slideshowImages[nextImageIndex]), 1);
        })
        imagesInToSlideshow += 1;
    }
    test('slideshow restarts after last image in a cycle displays', () => {
        const elementsWithClassCurrentImage = [...document.getElementsByClassName('current_image')];
        const arrayLength = elementsWithClassCurrentImage.length;
        let currentImageIndex = slideshowImages.indexOf(lastImageDisplayed[0]);
        let nextImageIndex = currentImageIndex === slideshowImages.length - 1 ? 0 : currentImageIndex + 1;
        jest.runOnlyPendingTimers();
        expect(slideshowImages[nextImageIndex].classList.contains('current_image'));
        expect(arrayLength).toBe(1);
        expect(slideshowImages[nextImageIndex].getAttribute('aria-hidden')).toBe('false');
        expect(document.querySelectorAll('[aria-hidden="false"]').length).toBe(1);
    })
})
