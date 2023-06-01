class EventClash(Exception):
    """
    Exception for when a user wants to register their interest in an event that occurs on a date that clashes with another event they are involved with.

    Attributes:
        msg (str): A personalised messsage indicating the exact reason a user cannot register their interest in the desired event.

    """
    def __init__(self, event_title, event_id, host=False, interested=False, attending=False):
        super().__init__()
        if host:
            self.msg = f'''Cannot register your interest in this event/activity, as you are due to host or are advertising to host an event/activity,
on the same day as this event/activity is scheduled to occur: you are currently hosting the event/activity (ID:{event_id}) titled {event_title}.'''
        if interested:
            self.msg = f'''Cannot register your interest in this event/activity, as you have registered your interest already in another event/activity
on the same day as this event/activity is scheduled to occur: you are currently interested in (ID:{event_id}) titled {event_title}.'''
        if attending:
            self.msg = f'''Cannot register your interest in this event/activity, as you already attending another event/activity
on the same day as this event/activity is scheduled to occur: you are currently currently attending (ID:{event_id}) titled {event_title}.'''
