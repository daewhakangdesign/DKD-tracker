import datetime

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