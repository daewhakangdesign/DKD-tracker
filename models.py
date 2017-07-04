from google.appengine.ext import ndb


class Person(ndb.Model):
    name = ndb.StringProperty()
    uuid = ndb.StringProperty(indexed=True)

    def add_event(self, event_type):
        event = Event(parent=self.key, event_type=event_type)
        event.put()

    @property
    def event_count(self):
        return Event.query(ancestor=self.key).count()


    def reset(self):
        ndb.delete_multi(Event.query(ancestor=self.key).iter(keys_only=True))


class Event(ndb.Model):
    event_type = ndb.StringProperty()
    at = ndb.DateTimeProperty(auto_now_add=True)