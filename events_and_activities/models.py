import re
from datetime import datetime
from django.db import models
from django.core.validators import (RegexValidator,
                                    MaxLengthValidator)
from landing_page.models import CustomUserModel
from home.models import ProfileMixin
from .validators import check_date_has_not_occured

# Create your models here.


class Engagement(models.Model):
    """
    Through model for a many-to-many relationship between the models EventsActivities and CustomUserModel.

    Attributes:
        event_id (foreign key): many-to-one relationship with the EventsActivites model.
        user (foreign key): many-to-one relationship with the CustomUserModel via the username field.
        status (character field): the engagement status of a user with an event/activity. Has one of three values: Interested, attending or attended.
        last_updated (DateTime field): the date and time when the status was last changed.
    """
    event_id = models.ForeignKey('EventsActivities',
                                 on_delete=models.CASCADE,
                                 related_name='engagement',
                                 verbose_name='event ID'
                                 )
    
    user = models.ForeignKey(CustomUserModel,
                             on_delete=models.CASCADE,
                             related_name='engagement',
                             verbose_name='engaged user',
                             to_field='username'
                             )

    INTERESTED = 'In'
    ATTENDING = 'Att'
    ATTENDED = 'Attd'
    STATUS_OPTIONS = [(INTERESTED, 'Interested'),
                      (ATTENDING, 'Attending'),
                      (ATTENDED, 'Attended')]
    status = models.CharField(choices=STATUS_OPTIONS,
                              default=INTERESTED,
                              max_length=4,
                              verbose_name='engagement status')
    
    last_updated = models.DateTimeField(auto_now=True,
                                        verbose_name='last updated')


class ChangeExpiredEvents(models.Manager):
    """
    Exists to filter out and delete or update expired events.
    """
    def delete_expired(self, user=None):
        """
        Deletes events that have already occured.
        """
        current_date_time = datetime.now().strftime("%H:%M, %d/%m/%y")
        current_date_time_object = datetime.strptime(current_date_time, "%H:%M, %d/%m/%y")

        if not user:
            expired_events = self.filter(when__lt=current_date_time_object)
            if len(expired_events):
                return expired_events.delete()
        else:
            expired_events = self.filter(host_user=user, when__lt=current_date_time_object)
            if len(expired_events):
                return expired_events.delete()

    def update_expired(self, user=None):
        """
        Alters the status of events whose closing advert date has expired.
        """
        current_date_time = datetime.now().strftime("%H:%M, %d/%m/%y")
        current_date_time_object = datetime.strptime(current_date_time, "%H:%M, %d/%m/%y")

        if not user:
            expired_events = self.filter(closing_date__lt=current_date_time_object)
            if len(expired_events):
                expired_events.update(status='confirmed')
        else:
            expired_events = self.filter(host_user=user, closing_date__lt=current_date_time_object)
            if len(expired_events):
                expired_events.update(status='confirmed')


class EventsActivities(ProfileMixin):
    """
    Stores all advertsied and organised user events and activities.

    Attributes:
        host_user (foreign key): many-to-one relationship with the CustomUserModel via the username field.
        status (character field): indicates the current status of an event.
        title (character field): title of the event or activity.
        when (datetime field): the scheduled date and time for the event/activity.
        closing date (datetime field): the date and time the advert closes.
        max attendees (integer field): the max number of people that can attend.
        keywords (character field): summary keywords for the event or activity.
        description (text field): description of the event/activity.
        requirements (text field): requirements to attend the event/activity.
        address_line_one (character field): for the event/activity.
        city_or_town (character field): for the event/activity.
        county (character field): for the event/activity.
        postcode (character field): UK postcode for the event/activity.
        attendees (many-to-many field): many-to-many relationship to the CustomUserModel via the engagement model.
    """
    class Meta:
        verbose_name = 'Events and Activities'
        verbose_name_plural = 'Events and Activities'
        ordering = ['-closing_date']

    title = models.CharField(max_length=100,
                             blank=False,
                             validators=[RegexValidator(regex=r"^([a-zA-Z0-9,.!\/;:]+\s{0,1}[a-zA-Z0-9,.!\/;:]+)+\Z",
                                                        message="Must contain only the characters [a-zA-Z0-9,.!/;:], with single spaces between words.",
                                                        flags=re.MULTILINE),
                                         MaxLengthValidator(100)])
                                         
    host_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,
                                  verbose_name='host',
                                  to_field='username',
                                  related_name='events',
                                  db_column='username',
                                  unique_for_date='when')
    STATUS_CHOICES = [('confirmed', 'confirmed'), ('advertised', 'advertised'), ('completed', 'completed')]
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, blank=False, default='advertised')

    when = models.DateTimeField(blank=False,
                                validators=[check_date_has_not_occured])

    closing_date = models.DateTimeField(blank=False, verbose_name='closing date',
                                        validators=[check_date_has_not_occured])

    max_attendees = models.IntegerField(blank=False, verbose_name='max no. of attendees')

    keywords = models.CharField(max_length=75,
                                blank=True,
                                validators=[MaxLengthValidator(75),
                                            RegexValidator(regex=r"^([a-zA-Z0-9\-_]+,?)+$",
                                                           message="Must contain comma separated words containing only the characters [a-z,A-Z,0-9,-,_], with no spaces.")])

    description = models.TextField(blank=False, max_length=500, validators=[MaxLengthValidator(500)])

    requirements = models.TextField(blank=False, max_length=500, validators=[MaxLengthValidator(500)])

    address_line_one = models.CharField(max_length=100, verbose_name='Address line 1',
                                        validators=[RegexValidator(regex=r"^([a-zA-Z0-9]+\s{0,1}[a-zA-Z0-9]+)+\Z",
                                                    message="Must contain only standard alphabetic characters and numbers, with single spaces between words.",
                                                    flags=re.MULTILINE),
                                                    MaxLengthValidator(100)],
                                        blank=False)

    city_or_town = models.CharField(max_length=50, verbose_name='City/Town',
                                    validators=[RegexValidator(regex=r"^([a-zA-Z]+\s{0,1}[a-zA-Z]+)+\Z",
                                                               message="Must contain only standard alphabetic characters, with single spaces between words."),
                                                MaxLengthValidator(50)],
                                    blank=False)

    county = models.CharField(max_length=50, verbose_name='County',
                              validators=[RegexValidator(regex=r"^([a-zA-Z]+\s{0,1}[a-zA-Z]+)+\Z",
                                                         message="Must contain only standard alphabetic characters, with single spaces between words."),
                                          MaxLengthValidator(50)],
                              blank=False)

    # taken from https://stackoverflow.com/questions/164979/regex-for-matching-uk-postcodes/17024047#17024047
    UK_POSTCODE_REGREX_EXPRESSION = r"^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$"

    postcode = models.CharField(max_length=10, verbose_name='Postcode', blank=False,
                                validators=[RegexValidator(regex=UK_POSTCODE_REGREX_EXPRESSION,
                                                           message="Must be a valid postcode format."),
                                            MaxLengthValidator(10)])

    # in future versions the coordinates of the event location will be stored, and along with a user's address coordinates, this will be used to calculate the
    # as the crow flies distance between the addresses. It will be the basis of a distance filter when searching for events.
    # latitude = models.DecimalField(max_digits=8, decimal_places=4,
    #                                blank=False,
    #                                validators=[DecimalValidator(8, 4)])

    # longitude = models.DecimalField(max_digits=8, decimal_places=4,
    #                                 blank=False,
    #                                 validators=[DecimalValidator(8, 4)])
    # Will also include address validation using the Geoapify API as for the address form in the edit profile form.

    attendees = models.ManyToManyField(to=CustomUserModel, through=Engagement, related_name='event')

    def __str__(self):
        return str(self.id)

    objects = models.Manager()
    expired = ChangeExpiredEvents()