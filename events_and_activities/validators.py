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
    input_date_object = datetime.strptime(date, "%H:%M, %d/%m/%y")
    if input_date_object < current_date_time_object:
        raise ValidationError('This date and time is in the past.', 'invalid date')