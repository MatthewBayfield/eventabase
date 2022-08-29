/**
* @jest-environment jsdom
*/

jest.useFakeTimers();
// Adds rendered landing_page template HTML content to the JSDOM
let fs = require('fs');
let fileContents = fs.readFileSync('static/js/html_content_for_js_tests/rendered_landing_page.html', 'utf-8');
document.documentElement.innerHTML = fileContents;
let {moreMenu, moreMenuContainer, moreMenuButtons, openMenu, closeMenu} = require('./script.js');

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
                for (item of menuItems) {
                    let event = new Event('mouseenter');
                    item.dispatchEvent(event);
                    expect(item.classList.contains('active')).toBe(true);
                    event = new Event('mouseleave');
                    item.dispatchEvent(event);
                    expect(item.classList.contains('active')).toBe(false);
                }
        })
        test("when clicked/pressed the menu item background and font colour changes temporarily", () => {
            for (item of menuItems) {
                let event = new Event('mousedown');
                item.dispatchEvent(event);
                expect(item.classList.contains('clicked')).toBe(true);
                event = new Event('mouseup');
                item.dispatchEvent(event);
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
    
        test('clicking anywhere not on the menu closes it', () => {
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
        })
    })    
})

describe('Test that the image slideshow functions as expected', () => {
    afterEach(() => {
       jest.runOnlyPendingTimers();
    })

    const slideshowImages = [...document.getElementsByClassName('slideshow_images')];
    let image_number;
    for (let index = 0; index < slideshowImages.length; index++) {
        image_number = index + 1;
        test((`check image ${image_number} is now the visible (incl for screen readers) image`), () => {
            const elementsWithClassCurrentImage = [...document.getElementsByClassName('current_image')];
            expect(elementsWithClassCurrentImage[0]).toBe(slideshowImages[index]);
            expect(elementsWithClassCurrentImage.length).toBe(1);
            expect(elementsWithClassCurrentImage[0].getAttribute('aria-hidden')).toBe('false');
            expect(document.querySelectorAll('[aria-hidden="false"]').length).toBe(1);
        })
    }
    test((`check image 1 is now the visible image again`), () => {
        const elementsWithClassCurrentImage = [...document.getElementsByClassName('current_image')];
        expect(elementsWithClassCurrentImage[0]).toBe(slideshowImages[0]);
        expect(elementsWithClassCurrentImage.length).toBe(1);
        expect(elementsWithClassCurrentImage[0].getAttribute('aria-hidden')).toBe('false');
        expect(document.querySelectorAll('[aria-hidden="false"]').length).toBe(1);
    })
})
