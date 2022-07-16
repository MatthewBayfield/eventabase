# Eventabase

## Design Process

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
            <td headers="user_stories theme1_epic1">As a <strong>site admin</strong> I can <strong>delete accounts that breach T & C's</strong>, so that <strong>they can no longer use the site.</strong></td>
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
            <th id="theme3" rowspan="11" headers="themes" scope="row">User Interaction and feedback</th>
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
            <th id=theme3_epic2 headers="epics theme3" scope="row" rowspan="4">notifications</th>
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
Considering the strategic goals and user needs of the site as expressed in the previous section, the following table dictates a concise set of requirements for the eventabase site:
<table>
    <thead>
        <tr>
            <th id="requirement_type" scope="col">Requirement type</th>
            <th id="requirement" scope="col">Requirements</th>
        </tr>
    </thead>
    <tbody>
         <!--objective requirements-->
        <tr>
            <td headers="requirement type">Objective</td>
            <td>
                <ul>
                    <li>A site user needs to be able to register an account on the landing page, or sign in if already registered.</li>
                    <li>A registered user needs to be able to advertise events and activities, in order to find other people to participate in them with.</li>
                    <li>A registered user needs to be able to discover events/activities to do with other people in their selected area.</li>
                    <li>A registered user needs to be able to communicate with other users information about hosting/attending an activity/event.</li>
                    <li>One or more site administrators need administrator accounts in order to delete accounts, remove malicious reviews, edit database search filters,
                    remove invalid events and acitivities.</li>
                </ul>
            </td>
        </tr>
        <!--content requirements-->
        <tr>
            <td headers="requirement type">Content</td>
            <td>
                <ul>
                    <li>The site must contain a searchable database of user-hosted advertised events and activities.</li>
                    <li>Registered users must have an editable profile with information including their personal details, their location, the events/activity types they prefer, specified using keywords; and the distance they are willing to travel.</li>
                    <li>A user in their profile should have an optional 'bio' section to describe a bit about themselves.</li>
                    <li>The site must contain 'Terms and Conditions.</li>
                    <li>Advertised events/activites must have an event description, and a set of summary keywords to act as filters. In addition they must specify
                    their location, a date or date range for their occurence, and a date to register interest by.</li>
                    <li>Advertised events/activites need to have the option of having a user uploaded image.</li>
                </ul>
            </td>
        </tr>
        <!--functional requirements-->
        <tr>
            <td headers="requirement type">Functional</td>
            <td>
                <ul>
                    <li>A user must be able to sign up for an account using a unique username, password, and email; the email should be verified.</li>
                    <li>A user must be able to reset their password when trying to sign in. They must also have the option of changing their password, username and email when
                    signed in.
                    <li>A user when searching for events/activities must be able to have the option of using default filters based on their profile, as well as optional filters that categorise the events/activities of the database.</li>
                    <li>A user must be able to view more information about a displayed event/activity in the search query results. The initial information dislayed should be
                    the title, location, date, closing date, distance away, summary keywords.</li>
                    <li>A user must be able to create a shortlist of events/activities they can view later, before registering their interest.</li>
                    <li>A user must be able to provide a review and rating out of 5 for a user as a participant, or a user as a host.</li>
                    <li>A host user of an event/activity must be able to select which users to invite, out of those interested in attending their event or activity. The host should be able to rank users by their participant rating, as well as view the profiles of other users.</li>
                    <li>A user should receive notifications both on the site and by email: when new events/activites of interest to them are posted; when a user registers their interest in their activity/event.</li>
                    <li>A user needs a message dashboard to communicate with other users when invited to an attend an event/activity.</li>
                    <li>A user needs to be able to view a list of events/activites they have registered their interest in, and be able to an event/activity from this list.</li>
                    <li>Site administrators need to be able to create other administrator accounts.</li>
                    <li>Site administrators need to be able to have a message dashboard to receive reported user issues, and to interact with users.</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

