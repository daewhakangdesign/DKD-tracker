import datetime
from calendar import monthrange

from google.appengine.ext import ndb


class Person(ndb.Model):
    name = ndb.StringProperty()
    uuid = ndb.StringProperty(indexed=True)

    def add_event(self, event_type):
        event = Event(parent=self.key, event_type=event_type)
        event.put()

    #Below we set up the properties accessible from the google datastore.

    @property
    def event_count(self):

        query = self._query_month(utc_offset=9)
        return query.count()


    @property
    def events_this_month(self):

        query = self._query_month(utc_offset=9)
        keys = query.fetch(keys_only = True)
        events = ndb.get_multi(keys)
        return events


    def get_month_start(self, previous=0):

        now = datetime.datetime.now()
        year = now.year
        month = now.month

        if previous != 0:
            month = month - previous
            if month < 1:
                month = month + 12
                year = year - 1

        return datetime.datetime(year=year, month=month, day=1)

    @property
    def this_month_totals(self):
        return self.get_month_totals()

    @property
    def last_month_totals(self):
        return self.get_month_totals(previous=1)


    def get_month_totals(self, previous=0, utc_offset=9):

        start_of_month = self.get_month_start(previous)


        month = start_of_month.month
        year = start_of_month.year

        day, day_count = monthrange(year, month)

        query = self._query_month(previous=previous, utc_offset=utc_offset)
        keys = query.fetch(keys_only=True)
        events = ndb.get_multi(keys)

        two_hour_array = [0] * (12 * day_count)

        for event in events:

            offset = event.at - start_of_month
            seconds = offset.total_seconds()
            hours = int(seconds/(60 * 60))
            two_hour_period = hours/2

            two_hour_array[two_hour_period] = two_hour_array[two_hour_period] + 1

        return two_hour_array


    @property
    def events_last_month(self):

        query = self._query_month(previous=1, utc_offset=9)
        keys = query.fetch(keys_only=True)
        events = ndb.get_multi(keys)
        return events


    def _query_month(self, previous=0, utc_offset=0):
        """
        Returns a query for this person's events for current month or an earlier one
        """

        now = datetime.datetime.now()
        year = now.year
        month = now.month

        if previous != 0:
            month = month - previous
            if month < 1:
                month = month + 12
                year = year - 1

        start_of_this_month = datetime.datetime(year=year, month=month, day=1)

        if month == 12:
            start_of_next_month = datetime.datetime(year=year + 1, month=1, day=1)
        else:
            start_of_next_month = datetime.datetime(year=year, month=month + 1, day=1)

        time_zone_correction = datetime.timedelta(hours=utc_offset)

        return Event.query(ndb.AND(Event.at >= start_of_this_month - time_zone_correction,
                                   Event.at < start_of_next_month - time_zone_correction), ancestor = self.key)

    def reset(self):
        ndb.delete_multi(Event.query(ancestor=self.key).iter(keys_only=True))


class Event(ndb.Model):
    event_type = ndb.StringProperty()
    at = ndb.DateTimeProperty(auto_now_add=True)

