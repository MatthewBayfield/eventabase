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
     editProfileFormFetchHandler, addEditProfileModalDonebuttonListeners} = require('../script.js');
// mock functions
const get = jest.fn()
global.Cookies = {'get': get};
global.Request = jest.fn();
let json_data;
global.fetch = jest.fn(() => Promise.resolve({
    json: () => Promise.resolve(json_data)
}));
global.alert = jest.fn();

let initialProfile = editProfileModal.parentElement.previousElementSibling.innerHTML;
let profile = `<div class="left_column top_row">
    <h3 class="profile_display">Personal Info</h3>

    
        <div class="profile_display">
            <span>First Name :</span>
            <span>matthewq</span>
        </div>
    

    
        <div class="profile_display">
            <span>Last Name :</span>
            <span>bayfield</span>
        </div>
    

    
        <div class="profile_display">
            <span>Date Of Birth :</span>
            <span>19/11/1993</span>
        </div>
    

    
        <div class="profile_display">
            <span>Sex :</span>
            <span>male</span>
        </div>
    

    
        <div class="profile_display">
            <span>Bio :</span>
            <span>I like to have fun.</span>
        </div>
    

</div>
<div class="right_column top_row">
    <h3 class="profile_display">Address</h3>

    <div class="profile_display">
        <span>Address Line 1 :</span>
        <span>11 rise park boulevard</span>
    </div>

    <div class="profile_display">
        <span>City/Town :</span>
        <span>romford</span>
    </div>

    <div class="profile_display">
        <span>County :</span>
        <span>essex</span>
    </div>

    <div class="profile_display">
        <span>Postcode :</span>
        <span>rm14pp</span>
    </div>

</div>
<div id="profile_flex" class="bottom_row">
    
        <div id="edit" role="button" aria-label="edit profile" aria-controls="edit_profile_modal" tabindex="0">
            <span>Edit <i class="fa-solid fa-pen-to-square"></i></span>
        </div>
    
    <div id="report_issue">
        <div>
            <button type="button" name="report_issue">Report Issue</button>
            <span data-icon-type="help" class="material-symbols-outlined" aria-hidden="true">help</span>
        </div>
        <div class="help_text">
            Report any issues, about the site, your account etc.
        </div>
    </div> 
</div>`;

let profile_after_error = `
    <div class="left_column top_row">
        <h3 class="profile_display">Personal Info</h3>
    
        
            <div class="profile_display">
                <span>First Name :</span>
                <span>matthew</span>
            </div>
        
    
        
            <div class="profile_display">
                <span>Last Name :</span>
                <span>bayfield</span>
            </div>
        
    
        
            <div class="profile_display">
                <span>Date Of Birth :</span>
                <span>19/11/1993</span>
            </div>
        
    
        
            <div class="profile_display">
                <span>Sex :</span>
                <span>male</span>
            </div>
        
    
        
            <div class="profile_display">
                <span>Bio :</span>
                <span>I like to have fun sometimes.</span>
            </div>
        
    
    </div>
    <div class="right_column top_row">
        <h3 class="profile_display">Address</h3>
    
        <div class="profile_display">
            <span>Address Line 1 :</span>
            <span>11 rise park boulevard</span>
        </div>
    
        <div class="profile_display">
            <span>City/Town :</span>
            <span>romford</span>
        </div>
    
        <div class="profile_display">
            <span>County :</span>
            <span>essex</span>
        </div>
    
        <div class="profile_display">
            <span>Postcode :</span>
            <span>rm14pp</span>
        </div>
    
    </div>
    <div id="profile_flex" class="bottom_row">
        
            <div id="edit" role="button" aria-label="edit profile" aria-controls="edit_profile_modal" tabindex="0">
                <span>Edit <i class="fa-solid fa-pen-to-square"></i></span>
            </div>
        
        <div id="report_issue">
            <div>
                <button type="button" name="report_issue">Report Issue</button>
                <span data-icon-type="help" class="material-symbols-outlined" aria-hidden="true">help</span>
            </div>
            <div class="help_text">
                Report any issues, about the site, your account etc.
            </div>
        </div> 
    </div>`


describe('test the ProfileFormView fetch request works', () => {
    beforeEach(() => {
        editProfileModal.style.display = 'block';
    })
    afterEach(() => {
        Request.mockClear();
        fetch.mockClear();
        alert.mockClear();
        editProfileModal.parentElement.previousElementSibling.innerHTML = initialProfile;
    })

    test('only two requests are made if the submitted forms are invalid, and the profile content does not change', async () => {
        json_data = {'valid': 'false', 'profile': profile}
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML.replace(/[\r\n\s]+/gm, "")).not.toBe(profile.replace(/[\r\n\s]+/gm, ""));
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(2);
        expect(fetch).toHaveBeenCalledTimes(2);
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML.replace(/[\r\n\s]+/gm, "")).not.toBe(profile.replace(/[\r\n\s]+/gm, ""));
    })


    test('four requests are made if the submitted forms are valid, and the profile content is updated', async () => {
        json_data = {'valid': 'true', 'profile': profile}
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML.replace(/[\r\n\s]+/gm, "")).not.toBe(profile.replace(/[\r\n\s]+/gm, ""));
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(4);
        expect(fetch).toHaveBeenCalledTimes(4);
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML.replace(/[\r\n\s]+/gm, "")).toBe(profile.replace(/[\s\r\n]+/gm, ""));
    })

    test('that an alert is raised when the related python exception occurs', async () => {
        json_data = {'valid': 'true', 'profile': profile_after_error, 'error': 'true'}
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(4);
        expect(fetch).toHaveBeenCalledTimes(4);
        expect(alert).toHaveBeenCalledTimes(1);
        errMsg = `There was a problem processing your submitted address, please check that the address information you entered
    is valid and try again; If the address is valid, try another address; if the problem persists, try again later.`;
        expect(alert).toHaveBeenCalledWith(errMsg);
        
    })        

    test('that the profile is updated as expected when the error occurs', async () => {
        json_data = {'valid': 'true', 'profile': profile_after_error, 'error': 'true'}
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML.replace(/[\r\n\s]+/gm, "")).not.toBe(profile_after_error.replace(/[\r\n\s]+/gm, ""));
        await editProfileFormFetchHandler();
        expect(Request).toHaveBeenCalledTimes(4);
        expect(fetch).toHaveBeenCalledTimes(4);
        expect(editProfileModal.parentElement.previousElementSibling.innerHTML.replace(/[\r\n\s]+/gm, "")).toBe(profile_after_error.replace(/[\s\r\n]+/gm, ""));
    })
})