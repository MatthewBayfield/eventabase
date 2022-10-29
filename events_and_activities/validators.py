from datetime import datetime
from django.core.exceptions import ValidationError


def check_date_has_not_occured(date):
    """
    Datetime field validator to check that a datetime input is not in the past.

    Args:
        date (str): a datetime formatted string
    
    Raises:
        ValidationError('This date and time is in the past.', 'invalid date') if datetime is in the past.
    """
    current_date_time = datetime.now().strftime("%H:%M, %d/%m/%y")
    current_date_time_object = datetime.strptime(current_date_time, "%H:%M, %d/%m/%y")
    if date < current_date_time_object:
        raise ValidationError('This date and time is in the past.', 'invalid date')


def compare_dates(closing_date, when):
    """
    Compares event advert closing date with its occurence datetime.

    Raises:
        if 'closing_data' > 'when' raises a validation error.
    """
    if closing_date > when:
        raise ValidationError('The closing advert date and time cannot be after when the event occurs.',
                              'invalid datetime-pair')
