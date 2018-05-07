import unittest
import uuid
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from models import Person


class TaskWorkerTest(unittest.TestCase):


    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()

        # self.policy = testbed.datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_app_identity_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()


    def test_add_event(self):
        person = Person(name="paul", uuid=str(uuid.uuid4()))
        person.put()

        person.add_event("test")
        self.assertTrue(person.event_count == 1)

        this_totals = person.this_month_totals
        last_totals = person.last_month_totals


        print(this_totals)
        print(last_totals)
