# Eventabase

## UX Design Process

### Strategy

Often people have the problem of wanting to participate in an activity
or attend an event, but lack other people needed or desired to do an activity,
or attend an event with. Additionally many people are interested in activities
on offer in their local area and beyond, that give them the chance to do
something fun or try something new, both whilst socialising and making new friends;
whether it be looking for a hitting partner in tennis, organising a camping
trip, or going paintballing and so on.

The purpose of the eventabase site is to allow registered users to advertise
group-based events or activities, that other users can register their interest
for participation in. The user organising the event/activity can then select who
to invite, and can communicate further information with those invited to attend.

#### User stories

<table>
    <thead>
        <tr>
            <th id="themes" scope="col">Themes</th>
            <th id="epics" scope="col">Epics</th>
            <th id="user_stories" scope="col">User stories</th>
        </tr>
    </thead>
    <tbody>
        <!-- account management theme-->
        <!--account creation/deletion epic-->
        <tr>
            <th id="theme1" rowspan="8" headers="themes" scope="row">account management</th>
            <th id=theme1_epic1 headers="epics theme1" scope="row" rowspan="4">account creation/deletion</th>
            <td headers="user_stories theme1_epic1">As a <strong>site user</strong> I can <strong>easily create an account</strong>, so that <strong>I can post or search for events and activities.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme1_epic1">As a <strong>site user</strong> I can <strong>delete my account</strong>, so that <strong>I no longer have one.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme1_epic1">As a <strong>site admin</strong> I can <strong>delete accounts that breach T & C</strong>, so that <strong>they can no longer use the site.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme1_epic1">As a <strong>site user</strong> I can <strong>reset my password if I forget it</strong>, so that <strong>I can still use my account .</strong></td>
        </tr>
        <!--create/edit profile epic-->
        <tr>
            <th id=theme1_epic2 headers="epics theme1" scope="row" rowspan="4">create/edit profile</th>
            <td headers="user_stories theme1_epic2">As a <strong>site user</strong> I can <strong>add personal information to my profile</strong>, so that <strong>I don't have to keep re-entering my contact and location details etc. repeatedly.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme1_epic2">As a <strong>site user</strong> I can <strong>specify the types of events/activites I like in my profile</strong>, so that <strong>I have a default set of filters when searching.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme1_epic2">As a <strong>site admin</strong> I can <strong>alter the keywords/categories the user can select to characterise events/activites they like</strong>, so that <strong> the search filters can be expanded and improved.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme1_epic2">As a <strong>site user</strong> I can <strong>specify a "willing to travel distance" in my profile</strong>, so that <strong>I have a default distance filter when searching.</strong></td>
        </tr>
        <!--event/activities theme-->
        <!--post new events/activities epic-->
        <tr>
            <th id="theme2" rowspan="11" headers="themes" scope="row">Event/activities management</th>
            <th id=theme2_epic1 headers="epics theme2" scope="row" rowspan="6">post new events/activities</th>
            <td headers="user_stories theme2_epic1">As a <strong>site user</strong> I can <strong>advertise an event/activity</strong>, so that <strong>other users can register
            their interest.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme2_epic1">As a <strong>site user</strong> I can <strong>provide an event/activity description</strong>, so that <strong>
            other users know what the event/activity involves.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic1">As a <strong>site user</strong> I can <strong>specify the number range of people that can attend the event/activity</strong>, so that <strong>
            other users know how many people can attend.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic1">As a <strong>site user</strong> I can <strong>specify a date range for the occurence of the activity/event </strong>, so that <strong>
            other users know whether they are able to attend.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic1">As a <strong>site user</strong> I can <strong>specify a 'closing date'</strong>, so that <strong>
            I have time to decide who to invite for the event/activity.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic1">As a <strong>site user</strong> I can <strong>cancel my advertsied event/activity</strong>, so that <strong>I can cancel it, for example if not enough people are attending.</strong></td>
        </tr>
        <!--search events/activities epic-->
        <tr>
        <th id=theme2_epic2 headers="epics theme2" scope="row" rowspan="5">search events/activities</th>
            <td headers="user_stories theme2_epic2">As a <strong>site user</strong> I can <strong>search for activities/events using optional, default, and no filters</strong>, so that <strong>I can find events/activites that are suitable and desirable.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic2">As a <strong>site admin</strong> I can <strong>automatically remove expired events/activities from the search results</strong>, so that <strong>I don't have to manually update them.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic2">As a <strong>site admin</strong> I can <strong>remove a specific event/activity from the search results</strong>, so that <strong>invalid events/activites can be removed.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme2_epic2">As a <strong>site user</strong> I can <strong>click on an event/activity in the search results</strong>, so that <strong> I can view more information about it.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme2_epic2">As a <strong>site user</strong> I can <strong>add available activities/events to a shortlist</strong>, so that <strong> I can look at them again later.</strong></td>    
        </tr>
        <!--user interaction and feedback theme-->
        <!--user selection epic-->
        <tr>
            <th id="theme3" rowspan="13" headers="themes" scope="row">User Interaction and feedback</th>
            <th id=theme3_epic1 headers="epics theme3" scope="row" rowspan="4">user selection</th>
            <td headers="user_stories theme3_epic1">As a <strong>site user</strong> I can <strong>for my event/activity select who to invite out of those interested, by viewing their profiles and other metrics</strong>, so that <strong>I can choose the people I prefer.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme3_epic1">As a <strong>site user</strong> I can <strong>register my interest in an event/activity</strong>, so that <strong>I have a chance to be invited by the host.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme3_epic1">As a <strong>site user</strong> I can <strong>unregister my interest in an event/activity</strong>, so that <strong>I can change my mind.</strong></td>
        </tr>
        <tr>
            <td headers="user_stories theme3_epic1">As a <strong>site user</strong> I can <strong>have a prefered users list</strong>, so that <strong>I can notify them directly of an event/activity I am hosting.</strong></td>
        </tr>
        <!--notifications epic-->
        <tr>
            <th id=theme3_epic2 headers="epics theme3" scope="row" rowspan="6">notifications</th>
            <td headers="user_stories theme3_epic2">As a <strong>site user</strong> I can <strong>receive notifications when new activities/events I like are posted</strong>, so that <strong>I am informed about events/activities that may be of interest.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic2">As a <strong>site user</strong> I can <strong>receive notifications when users register their interest in my advertised events/activites</strong>, so that <strong>I can keep track of the level of interest and I know when enough people have registered for the activity/event.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic2">As a <strong>site user</strong> I can <strong>receive notifications when I am invited to an event/activity</strong>, so that <strong>I know I can attend.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic2">As a <strong>site user</strong> I can <strong>receive notifications about events/activites I have been invited to attend</strong>, so that <strong>I am aware of any important information.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic2">As a <strong>site user</strong> I can <strong>view a calender of my upcoming events and activities</strong>, so that <strong> I am aware of my schedule.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic2">As a <strong>site user</strong> I can <strong>receive notifications about an upcoming event/activity I am attending</strong>, so that <strong>I don't forget to attend.</strong></td>    
        </tr>
        <!--review/ratings epic-->
        <tr>
            <th id=theme3_epic3 headers="epics theme3" scope="row" rowspan="3">review/ratings</th>
            <td headers="user_stories theme3_epic3">As a <strong>site user</strong> I can <strong>review events/activites and other users</strong>, so that <strong>users have metrics to indicate the quality of their hosting or participation.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic3">As a <strong>site user</strong> I can <strong>report issues with events/activities or other users</strong>, so that <strong>they can be resolved by a site administrator.</strong></td>    
        </tr>
        <tr>
            <td headers="user_stories theme3_epic3">As a <strong>site admin</strong> I can <strong>remove malicious or suspicious reviews </strong>, so that <strong>any user's rating is accurate.</strong></td>    
        </tr>
    </tbody>
</table>

### Scope

#### Requirements
Considering the strategic goals and user needs of the site as expressed in the previous section, the following table dictates a core set of requirements --- each assigned with an importance rating --- for the eventabase site. Time constraints along with the relative importance and feasibility of requirements will determine which requirements are prioritised, and thus fulfilled in the minimal viable product.
<table>
    <thead>
        <tr>
            <th id="requirement_type" scope="col">Requirement type</th>
            <th id="requirement" scope="col">Requirements (importance 1-5)</th>
        </tr>
    </thead>
    <tbody>
         <!--objective requirements-->
        <tr>
            <td headers="requirement type">Objective</td>
            <td>
                <ul>
                    <li>A site user needs to be able to register an account on the landing page, or sign in if already registered. <strong>(5)</strong></li>
                    <li>A registered user needs to be able to advertise events and activities, in order to find other people to participate in them with. <strong>(5)</strong></li>
                    <li>A registered user needs to be able to discover events/activities to do with other people in their selected area. <strong>(5)</strong></li>
                    <li>A registered user needs to be able to communicate with other users information about hosting/attending an activity/event. <strong>(5)</strong></li>
                    <li>Site administrators need administrator accounts to perform administrative duties. <strong>(3)</strong></li>
                </ul>
            </td>
        </tr>
        <!--content requirements-->
        <tr>
            <td headers="requirement type">Content</td>
            <td>
                <ul>
                    <li>The site must present entries from a searchable backend database of user-hosted advertised events and activities. <strong>(5)</strong></li>
                    <li>Expired events/activities are removed from the displayed database entries automatically, either when their closing date has past or when they are cancelled. <strong>(5)</strong></li>
                    <li>Registered users must have an editable profile with information including their personal details, their location, the events/activity types they prefer, specified using either provided or possibly custom keywords; and the distance they are willing to travel. These details will define the default search filters. <strong>(4)</strong></li>
                    <li>A user in their profile should have an optional 'bio' section to describe a bit about themselves. <strong>(1)</strong></li>
                    <li>The site must contain viewable 'Terms and Conditions. <strong>(3)</strong></li>
                    <li>Advertised events/activites must have an event description, and a set of summary keywords to act as filters. In addition they must specify
                    their location, a date or date range for their occurence, and a date to register interest by. <strong>(5)</strong></li>
                    <li>Events/activities, users, and reviews should have a displayed unique identifier primarily for admin purposes. <strong>(3)</strong></li>                    <li>Advertised events/activites need to have the option of having a user uploaded image. <strong>(2)</strong></li>
                    <li>The site must contain observable ratings/reviews of other users indicating their quality as a host or participant. <strong>(4)</strong></li>
                    <li>A viewable, potentially interactive, calendar of upcoming events/activities for a user exits. <strong>(3)</strong></li>
                </ul>
            </td>
        </tr>
        <!--functional requirements-->
        <tr>
            <td headers="requirement type">Functional</td>
            <td>
                <ul>
                    <li>Users that are not registered or not signed in should only be able to view a landing page. <strong>(5)</strong></li>
                    <li>A user must be able to sign up for an account using a unique username, password, and email; the email should be verified. <strong>(5)</strong></li>
                    <li> A user must be able to delete their account. <strong>(1)</strong> </li>
                    <li>A user must be able to reset their password when trying to sign in. They must also have the option of changing their password, username and email when
                    signed in. <strong>(2)</strong></li>
                    <li>A user when searching for events/activities must be able to have the option of using togglable default filters based on their profile, as well as optional filters that categorise the events/activities of the database. <strong>(4)</strong></li>
                    <li>A user must be able to view more information about a displayed event/activity in the search query results. The initial information dislayed should be
                    the title, location, date, closing date, distance away, summary keywords. <strong>(4)</strong></li>
                    <li>A user must be able to register their interest in an advertised event/activity. <strong>(5)</strong></li>
                    <li>A user needs to be able to view a list of events/activites they have registered their interest in, and be able to remove an event/activity from this list. <strong>(4)</strong></li>
                    <li>A user must be able to create a shortlist of events/activities they can view later, before registering their interest. <strong>(2)</strong></li>
                    <li>A user must be able to provide a review and rating out of 5 for a user as a participant, or a user as a host. <strong>(4)</strong></li>
                    <li>A host user of an event/activity must be able to cancel their event or activity. <strong>(5)</strong></li>
                    <li>A host user of an event/activity must be able to select which users to invite, out of those interested in attending their event or activity. <strong>(5)</strong></li>
                    <li>The host should be able to rank users by their participant rating, as well as view the profiles of other users. <strong>(3)</strong></li>
                    <li>A user needs a way of reporting issues with another user, a review, or an issue with their account. <strong>(3)</strong></li>
                    <li>A user has a favourite user list or friends list, and a way of adding, removing users to this list. <strong>(1)</strong></li>
                    <li>A user should receive notifications both on the site and or by email: when new events/activites of interest to them are posted; when a user registers their interest in their activity/event; or a reminder to attend an upcoming event/activity. <strong>(3)</strong></li>
                    <li>A user needs a message dashboard to communicate with other users when invited to an attend an event/activity. <strong>(4)</strong></li>
                    <li>Site admins need to be able to create other administrator accounts. <strong>(2)</strong></li>
                    <li>Site admins need to be able to view and delete accounts, remove malicious user reviews, edit database search filters,
                    remove invalid events and acitivities. <strong>(3)</strong></li>
                    <li>Site admins need to be able to have a message dashboard to receive reported user issues, and to interact with users. <strong>(3)</strong></li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

### Structure

#### Information design

The site will potentially consist of the following pages:

Accessible to all users:
- a generic landing/home page - will act as the first point of contact, and explain the purpose of the site as well as how to use the site. It will need to be attractive
and fairly minimal. Must contain clearly visible sign-up and sign-in options for the user to interact with.
- a sign-up/registration page - must enable validated form input for the user's name, username, email, and password. Upon registering and verifying their account email, the
user should be taken to their home page.
- a T & C page containing the terms and conditions of the site.

Accessible to registered users only:
- a registered user home page - Once registered users have signed in, they should be taken to their home page. This page will contain navigation and button elements that allow the user to view other relevant pages or modals/panels, and thus perform all of the desired functionality on the site. The page should be divided into a profile section; a search/host events and activities section. The latter section will have distinct subsections, including a section for reviewing/rating other users and activities/events.
- search and retrieve events/activities page - This page will display a list of events/activities retrieved from the database, filtered using available filters. Each item in the list will be able to be expanded to view more information about the item.
- registered user message/notifications dashboard page - will feature messages from admins and other users, as well as notifications about new events/activities or when someone registers their interest in an activity/event hosted by the user. Should allow communication between admins and users.


Accessible to site admins only:
- an administrator home page - This page will host all of the functionality necessary to perform administrative duties, such as editing the T & C, viewing user accounts and
events/activities etc.
- admin message dashboard - will feature messages/reports from users. Should allow communication between admins and users.

Accessible to site admins and registered users:
- an account settings page - where a user can change their account email, password, and username; as well as delete their account.

#### Interaction design

A navigation bar common to all registered-user-accessible pages and admin-accessible pages other than the T & C page, will feature a home button link, a sign-out link, a message/notifications indicator/link and a 'more' hamburger icon menu; the hamburger menu featuring an account settings and T & C link. The all-user-accessible landing page will feature a nav bar with only a sign-in/sign-up link, and a T & C link within a hamburger icon menu. The T & C page nav bar will feature a sign-out/sign-in/sign-up link and a home button link.

Modals opened on one of the pages or expandable side panels, will be used frequently to allow functionality such as posting new events/activities, viewing more information about an event/activity etc. These modals or side panels will be opened when labelled buttons, links, or icons are clicked by the user. They will take up most of the page, and will be closable both automatically and manually by the user. 

Most pages will feature content that can be expanded and collapsed, thus decluttering the page while keeping all functionality and content available when needed.

For the pages/modals/panels requiring extended user input --- such as the user profile, or when writing a review --- validated form fields will be used.

#### Planned site structure/connectivity diagrams

The first diagram below shows the possible page, modal, and panel connectivity not using the navigation bar; it assumes all requirements/user stories are fulfilled. The 2nd diagram shows the connectivity between pages using only the navigation bars.

<img src='docs/diagrams/site_structure_connectivity_no_nav.png' alt='diagram showing planned connectivity of site pages, modals and panels, not using page nav bars'>
<img src='docs/diagrams/site_structure_connectivity_nav.png' alt='diagram showing planned connectivity of site pages using page nav bars only'>

### Skeleton

#### Wireframes
Below are links to the mobile wireframes of each page, as well as for the modals; there are no separate desktop wireframes, as the intention is to keep the appearance of
the site as a whole the same across all devices, using only a responsive design as opposed to an adaptive design; this will be achieved in part by allowing vertical scrolling on all pages, modals, and panels where needed.

##### Pages
[Landing page](docs/wireframes/wireframe_landing_page.png)

[User registration page](docs/wireframes/wireframe_registration_page.png)

[Home page for registered users](docs/wireframes/wireframe_home_registered_users.png)

[Home page for admin users](docs/wireframes/wireframe_home_admin_users.png)

[Account settings page](docs/wireframes/wireframe_account_settings.png)

[Terms and conditions page](docs/wireframes/wireframe_terms_conditions.png)

[Search and retrieve events and activities page](docs/wireframes/wireframe_search_events_activities_page.png)

[Notifications/Messages dashboard page](docs/wireframes/wireframe_notifications_messages_page.png)


##### Modals

[Sign-in Modal](docs/wireframes/wireframe_sign_in_modal.png)

[Reset password Modal](docs/wireframes/wireframe_rest_password_modal.png)

[Edit profile Modal](docs/wireframes/wireframe_edit_profile_modal.png)

[Post new event/activity Modal](docs/wireframes/wireframe_post_new_event_activity_modal.png)

[Review user event/activity/user Modal](docs/wireframes/wireframe_review_user_event_activity.png)

[View more information for event/activity Modal](docs/wireframes/wireframe_more_info_event_or_activity.png)

[View interested or invited Modal](docs/wireframes/wireframe_view_interested_or_invited.png)

[View event/activity shortlist Modal](docs/wireframes/wireframe_activities_or_events_shortlist.png)

[Event/Activity calendar Modal](docs/wireframes/wireframe_calendar_modal.png)

[View interested users Modal](docs/wireframes/wireframe_view_interested_users.png)

[Message host/attendees/user Modal](docs/wireframes/wireframe_message_host_or_attendees_or_user.png)

[View user's profile/reviews Modal](docs/wireframes/wireframe_view_user_profiles_reviews_modal.png)

[View own reviews Modal](docs/wireframes/wireframe_own_reviews.png)

[Report issue Modal](docs/wireframes/wireframe_report_issue.png)

[Review user/event/activity Modal](docs/wireframes/wireframe_review_user_event_activity.png)

[Create admin account Modal](docs/wireframes/wireframe_create_admin_account_modal.png)

[Edit T & C Modal](docs/wireframes/wireframe_edit_t_and_c_modal.png)

[Alter keywords Modal](docs/wireframes/wireframe_alter_keywords_modal.png)

[View user's reviews Modal](docs/wireframes/wireframe_users_reviews_modal.png)

[View reviews of user Modal](docs/wireframes/wireframe_view_reviews_of_user_modal.png)

[View user's events/activities Modal](docs/wireframes/wireframe_view_users_events_or_activities.png)

[View user's profile Modal](docs/wireframes/wireframe_view_user_profile_modal.png)

[View review or event/activity Modal](docs/wireframes/wireframe_view_review_or_event_modal.png)



### Surface

'Hover for more info' icons will be used to guide the user in understanding how to use parts of the site, as well as when providing user input or interpreting displayed information. Regular feedback and helper prompts will also be provided to the user where necessary in order to maximise user experience and minimise user effort. 

Icons and other visual aids will also be used where possible to further make using the site simple and more enjoyable; for example a new message/notification counter will
be visible just above the message dashboard icon link in the nav bar. An attempt will be made to dynamically focus the user's attention where it needs to be, throughout performing a specific task; for example changes to background or font colours as well as the use of highlighting/dimming will be used where suitable.

Compulsory form/input fields will be indicated, and missing or invalid inputs will be highlighted to users, with a clarifying explanation message.

Images will be used on the landing page, as well on advertised events/activities where the user uploads an image. An uploaded profile image may also be available
to the user. Likewise some animation/transitions will feature on the landing page, through a slide show of background header images, and a cycling of messages in a bar
below the header, that motivate use of the site, and indicate its purpose to the user.

Finally, in regard to the potential typography and colour schemes employed, the aim will be to maximise the readability and also attractiveness of the site content, by creating 
a clear pattern of use that helps to distinguish content and highlight the most important content. The final choices will be decided through experimentation and manual user feedback, as well as by which fonts and color scheme combinations sufficiently satisfy accessibility requirements.



